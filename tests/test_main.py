# stdlib
import tempfile
from typing import List

# 3rd party
import pytest
from coincidence.regressions import check_file_regression
from consolekit.testing import CliRunner, Result, click_version
from domdf_python_tools.paths import in_directory
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import octocheese
from octocheese.__main__ import main


def run_test(
		file_regression: FileRegressionFixture,
		exit_code: int,
		*args: str,
		extension: str = ".txt",
		) -> None:
	__tracebackhide__ = False

	with tempfile.TemporaryDirectory() as tmpdir:
		with in_directory(tmpdir):
			runner = CliRunner()
			result: Result = runner.invoke(main, catch_exceptions=False, args=args)

			assert result.exit_code == exit_code
			check_file_regression(result.stdout.rstrip(), file_regression, extension=extension)


dash_r = pytest.mark.parametrize(
		"dash_r",
		[
				["-r", "https://github.com/github/choosealicense.com.git"],
				["-r", "https://github.com/github/choosealicense.com"],
				["-r", "github/choosealicense.com"],
				["-rhttps://github.com/github/choosealicense.com.git"],
				["-rhttps://github.com/github/choosealicense.com"],
				["-rgithub/choosealicense.com"],
				["--repo", "https://github.com/github/choosealicense.com.git"],
				["--repo", "https://github.com/github/choosealicense.com"],
				["--repo", "github/choosealicense.com"],
				],
		)

_click_84_param = pytest.mark.parametrize(
		"click_version",
		[
				pytest.param(
						"pre_84",
						marks=pytest.mark.skipif(click_version >= (8, 4), reason="Output differs on click 8.4"),
						),
				pytest.param(
						"84",
						marks=pytest.mark.skipif(click_version < (8, 4), reason="Output differs on click 8.4"),
						),
				],
		)


@_click_84_param
def test_main_no_args(
		click_version: str,
		file_regression: FileRegressionFixture,
		):
	run_test(file_regression, 2)


@pytest.mark.parametrize("args", [["-h"], ["--help"]])
def test_main_help(args: List[str], file_regression: FileRegressionFixture):
	run_test(file_regression, 0, *args)


def test_main_version(file_regression: FileRegressionFixture, monkeypatch):
	monkeypatch.setattr(octocheese, "__version__", "0.2.1")
	run_test(file_regression, 0, "--version")


@_click_84_param
def test_main_missing_token(
		click_version: str,
		file_regression: FileRegressionFixture,
		):
	run_test(file_regression, 2, "octocat/hello_world")


@pytest.mark.usefixtures("fake_token")
@pytest.mark.parametrize("dash_t", [["-t", "1234"], ["-t1234"], ["--token", "1234"]])
@_click_84_param
@dash_r
def test_main_invalid_credentials(
		click_version: str,
		dash_t: str,
		dash_r: str,
		file_regression: FileRegressionFixture,
		):
	run_test(file_regression, 2, "octocat/hello_world", *dash_t, *dash_r, extension="._t_r.txt")
	run_test(file_regression, 2, "octocat/hello_world", *dash_r, *dash_t, extension="._r_t.txt")


@pytest.mark.usefixtures("fake_token")
@_click_84_param
@dash_r
def test_main_invalid_credentials_env(
		click_version: str,
		dash_r: str,
		file_regression: FileRegressionFixture,
		):
	run_test(file_regression, 2, "octocat/hello_world", *dash_r)


@pytest.mark.usefixtures("fake_token")
@_click_84_param
def test_main_not_git_repo(click_version: str, file_regression: FileRegressionFixture):
	run_test(file_regression, 2, "octocat/hello_world")

# stdlib
import tempfile

# 3rd party
import pytest
from click.testing import CliRunner, Result
from domdf_python_tools.paths import in_directory
from domdf_python_tools.testing import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from octocheese.__main__ import main


def run_test(file_regression: FileRegressionFixture, exit_code: int, *args: str, extension: str = ".txt"):
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
				]
		)


def test_main_no_args(file_regression: FileRegressionFixture):
	run_test(file_regression, 2)


@pytest.mark.parametrize("args", [["-h"], ["--help"]])
def test_main_help(args, file_regression: FileRegressionFixture):
	run_test(file_regression, 0, *args)


def test_main_missing_token(file_regression: FileRegressionFixture):
	run_test(file_regression, 2, "octocat/hello_world")


@pytest.mark.usefixtures("fake_token")
@pytest.mark.parametrize("pypi_name", ["hello_world"])
@pytest.mark.parametrize("dash_t", [["-t", "1234"], ["-t1234"], ["--token", "1234"]])
@dash_r
def test_main_invalid_credentials(pypi_name, dash_t, dash_r, file_regression: FileRegressionFixture):
	run_test(file_regression, 2, "octocat/hello_world", *dash_t, *dash_r, extension="._t_r.txt")
	run_test(file_regression, 2, "octocat/hello_world", *dash_r, *dash_t, extension="._r_t.txt")


@pytest.mark.usefixtures("fake_token")
@pytest.mark.parametrize("pypi_name", ["hello_world"])
@dash_r
def test_main_invalid_credentials_env(pypi_name: str, dash_r, file_regression: FileRegressionFixture):
	run_test(file_regression, 2, "octocat/hello_world", *dash_r)


@pytest.mark.usefixtures("fake_token")
@pytest.mark.parametrize("pypi_name", ["hello_world"])
def test_main_not_git_repo(pypi_name: str, file_regression: FileRegressionFixture):
	run_test(file_regression, 2, "octocat/hello_world")

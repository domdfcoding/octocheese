# 3rd party
import pytest

# this package
from octocheese.__main__ import main


def test_main(monkeypatch, tmpdir, capsys):
	monkeypatch.chdir(str(tmpdir))

	with pytest.raises(SystemExit):
		main([])

	captured = capsys.readouterr()

	assert captured.out.splitlines() == []
	assert captured.err.splitlines() == [
			"usage: octocheese [-h] [-t TOKEN] [-r REPO] pypi_name",
			"octocheese: error: the following arguments are required: pypi_name",
			]

	with pytest.raises(SystemExit):
		main(["-h"])

	captured = capsys.readouterr()

	assert captured.out.splitlines() == [
			"usage: octocheese [-h] [-t TOKEN] [-r REPO] pypi_name",
			'',
			"positional arguments:",
			"  pypi_name             The project name on PyPI.",
			'',
			"optional arguments:",
			"  -h, --help            show this help message and exit",
			"  -t TOKEN, --token TOKEN",
			"                        The token to authenticate with the GitHub API. Can",
			"                        also be provided via the 'GITHUB_TOKEN' environment",
			"                        variable.",
			"  -r REPO, --repo REPO  The repository name (in the format",
			"                        <username>/<repository>) or the complete GitHub URL."
			]
	assert captured.err.splitlines() == []

	with pytest.raises(SystemExit):
		main(["hello_world"])

	captured = capsys.readouterr()

	assert captured.out.splitlines() == []
	assert captured.err.splitlines() == [
			"usage: octocheese [-h] [-t TOKEN] [-r REPO] pypi_name",
			"octocheese: error: Please supply a GitHub token with the '-t' / '--token' argument, "
			"or via the environment variable 'GITHUB_TOKEN'."
			]


@pytest.mark.parametrize("pypi_name", ["hello_world"])
@pytest.mark.parametrize("dash_t", [
		["-t", "1234"],
		["-t1234"],
		["--token", "1234"],
		])
@pytest.mark.parametrize(
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
def test_main_invalid_credentials(monkeypatch, tmpdir, capsys, pypi_name, dash_t, dash_r):
	argv = ["hello_world", *dash_t, *dash_r]
	monkeypatch.chdir(str(tmpdir))

	with pytest.raises(SystemExit):
		main(argv)

	captured = capsys.readouterr()

	assert captured.out.splitlines() == ['Running for repo github/choosealicense.com']
	assert captured.err.splitlines() == [
			'usage: octocheese [-h] [-t TOKEN] [-r REPO] pypi_name',
			'octocheese: error: Invalid credentials for GitHub REST API.'
			]

	with pytest.raises(SystemExit):
		main(["hello_world", *dash_r, *dash_t])

	captured = capsys.readouterr()

	assert captured.out.splitlines() == ['Running for repo github/choosealicense.com']
	assert captured.err.splitlines() == [
			'usage: octocheese [-h] [-t TOKEN] [-r REPO] pypi_name',
			'octocheese: error: Invalid credentials for GitHub REST API.'
			]


@pytest.mark.parametrize("pypi_name", ["hello_world"])
@pytest.mark.parametrize(
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
def test_main_invalid_credentials_env(monkeypatch, tmpdir, capsys, pypi_name, dash_r):
	argv = ["hello_world", *dash_r]
	monkeypatch.chdir(str(tmpdir))
	monkeypatch.setenv("GITHUB_TOKEN", "1234")

	with pytest.raises(SystemExit):
		main(argv)

	captured = capsys.readouterr()

	assert captured.out.splitlines() == ['Running for repo github/choosealicense.com']
	assert captured.err.splitlines() == [
			'usage: octocheese [-h] [-t TOKEN] [-r REPO] pypi_name',
			'octocheese: error: Invalid credentials for GitHub REST API.'
			]


@pytest.mark.parametrize("pypi_name", ["hello_world"])
def test_main_not_git_repo(monkeypatch, tmpdir, capsys, pypi_name):
	argv = ["hello_world"]
	monkeypatch.chdir(str(tmpdir))
	monkeypatch.setenv("GITHUB_TOKEN", "1234")

	with pytest.raises(SystemExit):
		main(argv)

	captured = capsys.readouterr()

	assert captured.out.splitlines() == []
	assert captured.err.splitlines() == [
			'usage: octocheese [-h] [-t TOKEN] [-r REPO] pypi_name',
			'octocheese: error: No git repository was found at .'
			]

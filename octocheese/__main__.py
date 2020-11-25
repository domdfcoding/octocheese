#!/usr/bin/env python3
#
#  __main__.py
"""
Entry points when running as a script.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# stdlib
import sys
from typing import Union

# 3rd party
import click
import github
from apeye import URL
from consolekit import click_command
from domdf_python_tools.secrets import Secret

# this package
from octocheese.core import copy_pypi_2_github

__all__ = ["main", "run", "token_var"]

token_var = "GITHUB_TOKEN"


@click.argument("pypi_name", type=click.STRING)
@click.option(
		"-t",
		"--token",
		type=click.STRING,
		help=(
				"The token to authenticate with the GitHub API. "
				f"Can also be provided via the '{token_var}' environment variable."
				),
		envvar=token_var,
		required=True,
		)
@click.option(
		"-r",
		"--repo",
		type=click.STRING,
		default=None,
		help="The repository name (in the format <username>/<repository>) or the complete GitHub URL.",
		)
@click.option(
		"--no-self-promotion",
		is_flag=True,
		default=False,
		help="Don't show information about OctoCheese at the bottom of the release message.",
		show_default=True,
		)
@click_command()
def main(
		pypi_name: str,
		token: str,
		repo: Union[str, URL, None] = None,
		no_self_promotion: bool = False,
		):
	"""
	Copy PyPI Packages to GitHub Releases.
	"""

	# 3rd party
	import click
	import dulwich.errors
	from consolekit.utils import abort
	from dulwich.repo import Repo
	from github.GithubException import BadCredentialsException

	gh_token = Secret(token)

	if repo is None:
		try:
			config = Repo('.').get_config()
			repo = URL(config.get(("remote", "origin"), "url").decode("UTF-8"))
		except dulwich.errors.NotGitRepository as e:
			raise click.UsageError(str(e))
	else:
		repo = URL(repo)

	if repo.suffix == ".git":
		repo = repo.with_suffix('')

	repo_name = repo.name

	# first case is for full url, second for github/hello_world
	github_username = repo.parent.name or repo.domain.domain

	try:
		run(gh_token, github_username, repo_name, pypi_name, self_promotion=not no_self_promotion)
	except BadCredentialsException:
		raise click.UsageError("Invalid credentials for GitHub REST API.")
	except Exception as e:
		raise abort(f"An error occurred: {e}")


def run(
		github_token: Secret,
		github_username: str,
		repo_name: str,
		pypi_name: str,
		self_promotion=True,
		):
	"""
	Helper function for when running as script or action.

	:param github_token: The token to authenticate with the GitHub API with.
		See https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
		for instructions on generating a token.
	:param github_username: The username of the GitHub account that owns the repository.
	:param repo_name: The name of the GitHub repository.
	:param pypi_name: The name of the package on PyPI.
	:param self_promotion: Show information about OctoCheese at the bottom of the release message.

	.. versionchanged:: 0.1.0

		Added the ``self_promotion`` option.
	"""

	g = github.Github(github_token.value)

	click.echo(f"Running for repo {github_username}/{repo_name}")

	rate = g.get_rate_limit()
	remaining_requests = rate.core.remaining
	click.echo(f"{remaining_requests} requests available.")

	copy_pypi_2_github(g, repo_name, github_username, pypi_name=pypi_name, self_promotion=self_promotion)

	rate = g.get_rate_limit()
	used_requests = remaining_requests - rate.core.remaining
	click.echo(f"Used {used_requests} requests. {rate.core.remaining} remaining. Resets at {rate.core.reset}")


if __name__ == "__main__":
	sys.exit(main())

#!/usr/bin/env python3
#
#  __main__.py
"""
Entry points when running as a script.
"""
#
#  Copyright (c) 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# stdlib
import sys
from typing import Union

# 3rd party
import click
from apeye import URL
from click import Context, Option
from consolekit import click_command
from consolekit.options import auto_default_option, flag_option, version_option
from domdf_python_tools.secrets import Secret
from github3_utils.click import token_option

__all__ = ["main", "run", "token_var"]

token_var = "GITHUB_TOKEN"


def _version_callback(ctx: Context, param: Option, value: int):
	# this package
	from octocheese import __version__

	if not value or ctx.resilient_parsing:
		return

	print(f"octocheese version {__version__}")
	sys.exit(0)


@version_option(_version_callback)
@flag_option(
		"--no-self-promotion",
		help="Don't show information about OctoCheese at the bottom of the release message.",
		)
@flag_option("-T", "--traceback", help="Show the full traceback on error.")
@auto_default_option(
		"-n",
		"--max-tags",
		type=click.INT,
		help="The maximum number of tags to process, starting with the most recent.",
		show_default=True,
		)
@auto_default_option(
		"-r",
		"--repo",
		type=click.STRING,
		help="The repository name (in the format <username>/<repository>) or the complete GitHub URL.",
		)
@token_option(token_var)
@click.argument("pypi_name", type=click.STRING)
@click_command()
def main(
		pypi_name: str,
		token: str,
		repo: Union[str, URL, None] = None,
		no_self_promotion: bool = False,
		max_tags: int = -1,
		traceback: bool = False,
		):
	"""
	Copy PyPI Packages to GitHub Releases.
	"""

	# 3rd party
	import click
	import dulwich.errors
	from consolekit.utils import abort
	from dulwich.repo import Repo
	from github3.exceptions import AuthenticationFailed

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
		run(
				gh_token,
				github_username,
				repo_name,
				pypi_name,
				self_promotion=not no_self_promotion,
				max_tags=max_tags
				)
	except AuthenticationFailed:
		raise click.UsageError("Invalid credentials for GitHub REST API.")
	except Exception as e:  # pragma: no cover
		if traceback:
			raise
		else:
			raise abort(f"An error occurred: {e}")


def run(
		github_token: Secret,
		github_username: str,
		repo_name: str,
		pypi_name: str,
		self_promotion=True,
		max_tags: int = -1,
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
	:param max_tags: The maximum number of tags to process, starting with the most recent.
		Set to ``-1`` to process all tags.

	.. versionchanged:: 0.1.0

		Added the ``self_promotion`` option.

	.. versionchanged:: 0.3.0

		Added the ``max_tags`` option.
	"""

	# 3rd party
	from github3 import GitHub
	from github3_utils import echo_rate_limit

	# this package
	from octocheese.core import copy_pypi_2_github

	g = GitHub(token=github_token.value)

	click.echo(f"Running for repo {github_username}/{repo_name}")

	with echo_rate_limit(g, True):
		copy_pypi_2_github(
				g,
				repo_name,
				github_username,
				pypi_name=pypi_name,
				self_promotion=self_promotion,
				max_tags=max_tags,
				)


if __name__ == "__main__":
	sys.exit(main())

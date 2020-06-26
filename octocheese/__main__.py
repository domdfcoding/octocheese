#!/usr/bin/env python3
#
#  __main__.py
"""
Entry points when running as a script
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
import argparse
import os
import pathlib
import sys
from typing import Optional, Sequence

# 3rd party
import github
from dulwich.repo import Repo  # type: ignore

# this package
from octocheese.core import Secret, copy_pypi_2_github


def main(argv: Optional[Sequence[str]] = None) -> int:
	"""
	Entry point for ``copy_pypi_2_github``.

	:rtype: int
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument("pypi_name", type=str, help="The project name on PyPI.")
	parser.add_argument(
			"-t",
			"--token",
			type=str,
			default=None,
			help=(
					"The token to authenticate with the GitHub API. "
					"Can also be provided via the `GITHUB_TOKEN` environment variable."
					),
			)
	parser.add_argument(
			"-r",
			"--repo",
			type=pathlib.Path,
			default=None,
			help="The repository name (in the format <username>/<repository>) or the complete GitHub URL.",
			)
	args = parser.parse_args(argv)

	if args.token is None:
		if "GITHUB_TOKEN" in os.environ:
			gh_token = Secret(os.environ["GITHUB_TOKEN"])
		else:
			sys.stdout.flush()
			print(
					"Please supply a GitHub token with the `-t` / `--token` argument, "
					"or via the environment variable `GITHUB_TOKEN`.",
					file=sys.stderr,
					)
			sys.stderr.flush()
			return 1
	else:
		gh_token = Secret(args.token)

	repo = args.repo

	if repo is None:
		config = Repo('.').get_config()
		repo = pathlib.Path(config.get(("remote", "origin"), "url").decode("UTF-8"))

	if repo.suffix == ".git":
		repo = repo.with_suffix('')

	repo_name = repo.name
	github_username = repo.parent.name

	run(gh_token, github_username, repo_name, args.pypi_name)

	return 0


def run(github_token: Secret, github_username: str, repo_name: str, pypi_name: str) -> None:
	"""
	Helper function for when running as script or action.

	:param github_token: The token to authenticate with the GitHub API with.
		See https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
		for instructions on generating a token.
	:param github_username: The username of the GitHub account that owns the repository.
	:param repo_name: The name of the GitHub repository.
	:param pypi_name: The name of the package on PyPI.
	"""

	g = github.Github(github_token.value)

	print(f"Running for repo {github_username}/{repo_name}")

	rate = g.get_rate_limit()
	remaining_requests = rate.core.remaining
	print(f"{remaining_requests} requests available.")

	copy_pypi_2_github(g, repo_name, github_username, pypi_name=pypi_name)

	rate = g.get_rate_limit()
	used_requests = remaining_requests - rate.core.remaining
	print(f"Used {used_requests} requests. {rate.core.remaining} remaining. Resets at {rate.core.reset}")


if __name__ == "__main__":
	sys.exit(main())

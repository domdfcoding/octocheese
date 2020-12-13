#!/usr/bin/env python3
#
#  action.py
"""
GitHub Actions entry point.

All the GitHub-specific setup is performed here.
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
import os
import sys

# 3rd party
from domdf_python_tools.secrets import Secret

# this package
from octocheese.__main__ import run

if __name__ == "__main__":
	print("[octocheese] Starting octocheese.")

	gh_token = Secret(os.environ["GITHUB_TOKEN"])
	github_username, repo_name = os.environ["GITHUB_REPOSITORY"].split('/')
	pypi_name = os.environ["INPUT_PYPI_NAME"]

	run(gh_token, github_username, repo_name, pypi_name)

	sys.exit(0)

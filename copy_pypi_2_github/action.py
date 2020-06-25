#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  action.py
"""
GitHub Actions entry point.

All the GitHub specific setup is performed here to make it easy to test the
action code in isolation.
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

# 3rd party
import github

# this package
from copy_pypi_2_github.core import copy_pypi_2_github

if __name__ == "__main__":
    print("[copy_pypi_2_github] Starting copy_pypi_2_github.")

    github_username = os.environ["GITHUB_ACTOR"]
    gh_token = os.environ["GITHUB_TOKEN"]
    repo_name = os.environ["GITHUB_REPOSITORY"].split("/")[1]
    pypi_name = os.environ["INPUT_PYPI_NAME"]
    g = github.Github(gh_token)

    rate = g.get_rate_limit()
    remaining_requests = rate.core.remaining
    print(rate)

    copy_pypi_2_github(g, repo_name, github_username, pypi_name=pypi_name)

    rate = g.get_rate_limit()
    used_requests = remaining_requests - rate.core.remaining
    print(f"Used {used_requests} requests. {rate.core.remaining} remaining. Resets at {rate.core.reset}")

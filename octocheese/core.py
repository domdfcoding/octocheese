#!/usr/bin/env python3
#
#  core.py
"""
The main logic of octocheese
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

# stdlib
import json
import os
import pathlib
import tempfile
import urllib.parse
from typing import Dict, List, Optional, Tuple

# 3rd party
import github
import github.GitRelease
import github.Repository
import requests

# this package
from .colours import error, success, warning


class Secret(str):
	"""
	Subclass of :py:class:`str`: that guards against accidentally printing a secret to the terminal.

	The actual value of the secret is accessed via the ``.value`` attribute.
	"""

	def __new__(cls, value):
		cls = super().__new__(cls, value)
		cls.value = str(value)
		return cls

	def __str__(self) -> str:
		return "<SECRET>"

	def __repr__(self) -> str:
		return "<SECRET>"


def get_pypi_releases(pypi_name: str) -> Dict[str, List[str]]:
	"""
	Returns a dictionary mapping PyPI release versions to download URLs.

	:param pypi_name: The name of the project on PyPI.
	:type pypi_name: str
	"""

	pypi_releases = {}

	# Parse PyPI data
	r = requests.get(f"https://pypi.org/pypi/{pypi_name}/json")
	if r.status_code != 200:
		error(f"Unable to get package data from PyPI for '{pypi_name}'")

	else:
		pkg_info = json.loads(r.content)

		for release, release_data in pkg_info["releases"].items():

			release_urls: List[str] = []

			for file in release_data:
				release_urls.append(file["url"])
			pypi_releases[release] = release_urls

	return pypi_releases


def update_github_release(
		repo: github.Repository.Repository,
		tag_name: str,
		release_name: str,
		release_message: str,
		) -> Tuple[github.GitRelease.GitRelease, List[str]]:
	"""

	:param repo:
	:param tag_name:
	:type tag_name: str
	:param release_name:
	:type release_name: str
	:param release_message:
	:type release_message: str

	:return: The release, and a list of URLs for the current assets.
	"""

	current_assets = []

	try:
		release = repo.get_release(tag_name)

		# Update existing release
		release.update_release(name=release_name, message=release_message)

		# Get list of current assets for release
		for asset in release.get_assets():
			current_assets.append(asset.name)

	except github.UnknownObjectException:

		# Create the release
		release = repo.create_git_release(tag=tag_name, name=release_name, message=release_message)

	return release, current_assets


def get_file_from_pypi(url: str, tmpdir: pathlib.Path) -> bool:
	"""
	Download the file with the given URL into the given (temporary) directory.

	:param url: The URL to download the file from.
	:type url: str
	:param tmpdir: The (temporary) directory to store the downloaded file in.

	:return: Whether the file was downloaded successfully.
	:rtype: bool
	"""

	filename = pathlib.PosixPath(urllib.parse.urlparse(url).path).name

	r = requests.get(url)
	if r.status_code != 200:
		error(f"Unable to download '{filename}' from PyPI. Skipping.")
		return False

	(tmpdir / filename).write_bytes(r.content)

	return True


def copy_pypi_2_github(
		g: github.Github,
		repo_name: str,
		github_username: str,
		*,
		release_message: str = '',
		pypi_name: Optional[str] = None,
		) -> None:
	"""
	The main function for ``octocheese``.

	:param g:
	:param repo_name: The name of the GitHub repository.
	:type repo_name: str
	:param github_username: The username of the GitHub account that owns the repository.
	:type github_username: str
	:param release_message:
	:type release_message: str
	:param pypi_name: The name of the project on PyPI.
	:type pypi_name: str, optional
	"""

	repo_name = str(repo_name)
	github_username = str(github_username)

	if not pypi_name:
		pypi_name = repo_name
	pypi_name = str(pypi_name)

	pypi_releases = get_pypi_releases(pypi_name)

	repo = g.get_repo(f"{github_username}/{repo_name}")

	with tempfile.TemporaryDirectory() as tmpdir:
		for tag in repo.get_tags():
			version = tag.name.lstrip("v")
			if version not in pypi_releases:
				warning(f"No PyPI release found for tag '{tag.name}'. Skipping.")
				continue

			print(f"Processing release for {version}")
			release_name = f"Version {version}"
			release_message += f"""
Automatically copied from PyPI.
https://pypi.org/project/{pypi_name}/{version}
"""

			release, current_assets = update_github_release(repo, tag.name, release_name, release_message)

			# pprint(pypi_releases[version])
			# Copy the files from PyPI

			for pypi_url in pypi_releases[version]:
				filename = pathlib.PosixPath(urllib.parse.urlparse(pypi_url).path).name
				# print(filename)

				if filename in current_assets:
					warning(f"File '{filename}' already exists for release '{tag.name}'. " f"Skipping.")
					continue

				if get_file_from_pypi(pypi_url, pathlib.Path(tmpdir)):
					success(f"Copying {filename} from PyPi to GitHub Releases.")
					release.upload_asset(os.path.join(tmpdir, filename))
				else:
					continue

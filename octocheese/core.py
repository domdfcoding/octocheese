#!/usr/bin/env python3
#
#  core.py
"""
The main logic of octocheese.
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
import datetime
import functools
from contextlib import suppress
from functools import partial
from typing import Iterable, Optional, Union

# 3rd party
import click
from apeye import URL
from domdf_python_tools.paths import PathPlus, TemporaryPathPlus
from domdf_python_tools.stringlist import StringList
from github3 import GitHub
from github3.exceptions import NotFoundError
from github3.repos import Repository
from github3.repos.release import Release
from github3_utils.apps import make_footer_links
from packaging.version import InvalidVersion, Version
from pypi_json import FileURL, PyPIJSON
from shippinglabel.checksum import check_sha256_hash
from typing_extensions import Literal

# this package
from octocheese.colours import error, success, warning

__all__ = ["update_github_release", "copy_pypi_2_github", "make_release_message"]


def update_github_release(
		repo: Repository,
		tag_name: str,
		pypi_name: str,
		changelog: str = '',
		self_promotion: bool = True,
		file_urls: Union[Iterable[str], Iterable[FileURL]] = (),
		traceback: bool = False,
		) -> Release:
	"""
	Update the given release on GitHub with the new name, message, and files.

	:param repo:
	:param tag_name:
	:param pypi_name: The name of the project on PyPI.
	:param changelog: The changelog entry for the release.
	:param self_promotion: Show information about OctoCheese at the bottom of the release message.
	:param file_urls: The files to download from PyPI and add to the release.
		Either the files URLs themselves, or mappings giving the URL and its sha256 checksum.
	:param traceback: Show the full traceback on error.

	:return: The release, and a list of URLs for the current assets.

	.. versionchanged:: 0.3.0

		Now takes a very different set of parameters to the previous version.
		Please read the current documentation carefully.
	"""

	version = tag_name.lstrip('v')
	release_name = f"Version {version}"

	message_maker = partial(
			make_release_message,
			pypi_name,
			version,
			changelog=changelog,
			self_promotion=self_promotion,
			)

	prerelease: bool = False
	with suppress(InvalidVersion):
		prerelease = Version(tag_name).is_prerelease

	current_assets = []

	# TODO: List checksums in release message.

	try:
		release: Release = repo.release_from_tag(tag_name)

		# Check if and when last updated.
		created_at: datetime.datetime = release.created_at.astimezone(datetime.timezone.utc)
		# last_updated = UTCDateTime.strptime(release.last_modified, "%a, %d %b %Y %H:%M:%S %Z")

		if (UTCDateTime.utcnow() - datetime.timedelta(days=7)) > created_at:
			# Don't update release message if created more than 7 days ago.
			click.echo(f"Skipping tag {tag_name} as it is more than 7 days old.")
			return release

		# Update existing release
		release.edit(
				name=release_name,
				body=message_maker(release_date=created_at),
				prerelease=prerelease,
				)

		# Get list of current assets for release
		for asset in release.assets():
			current_assets.append(asset.name)

	except NotFoundError:
		# Create the release
		release = repo.create_release(
				tag_name=tag_name,
				name=release_name,
				body=message_maker(release_date=datetime.date.today()),
				prerelease=prerelease,
				)

	if not file_urls:
		return release

	with TemporaryPathPlus() as tmpdir:

		for pypi_url in file_urls:
			if isinstance(pypi_url, dict):
				checksum: Optional[str] = pypi_url["digest"]
				pypi_url = pypi_url["url"]
			else:
				checksum = None

			filename = URL(pypi_url).name

			if filename in current_assets:
				warning(f"File '{filename}' already exists for release '{tag_name}'. Skipping.")
				continue

			try:

				with PyPIJSON() as client:
					response = client.download_file(pypi_url)

				if response.status_code != 200:  # pragma: no cover
					raise OSError(f"Unable to download '{filename}' from PyPI.")

				downloaded_file = tmpdir / filename
				downloaded_file.write_bytes(response.content)

				if checksum is not None and not check_sha256_hash(downloaded_file, checksum):
					raise ValueError(f"The checksums for {filename} do not match!")

				success(f"Copying {filename} from PyPI to GitHub Releases.")
				release.upload_asset(
						content_type="application/binary",
						name=filename,
						asset=(PathPlus(tmpdir) / filename).read_bytes()
						)

			except OSError as e:
				if traceback:
					raise
				else:
					error(f"{e} Skipping.")
					continue

	return release


def copy_pypi_2_github(
		g: GitHub,
		repo_name: str,
		github_username: str,
		*,
		changelog: str = '',
		pypi_name: Optional[str] = None,
		self_promotion=True,
		max_tags: int = -1,
		traceback: bool = False,
		):
	"""
	The main function for ``OctoCheese``.

	:param g:
	:param repo_name: The name of the GitHub repository.
	:param github_username: The username of the GitHub account that owns the repository.
	:param changelog:
	:param pypi_name: The name of the project on PyPI.
	:default pypi_name: The value of ``repo_name``.
	:param self_promotion: Show information about OctoCheese at the bottom of the release message.
	:param max_tags: The maximum number of tags to process, starting with the most recent.
		Set to ``-1`` to process all tags.
	:param traceback: Show the full traceback on error.

	.. versionchanged:: 0.1.0

		Added the ``self_promotion`` option.

	.. versionchanged:: 0.3.0

		* Added the optional ``max_tags`` option.
		* Added the optional ``traceback`` parameter.
	"""

	repo_name = str(repo_name)
	github_username = str(github_username)

	if not pypi_name:
		pypi_name = repo_name

	pypi_name = str(pypi_name)

	with PyPIJSON() as client:
		pypi_releases = client.get_metadata(pypi_name).get_releases_with_digests()

	repo: Repository = g.repository(github_username, repo_name)

	for tag in repo.tags(max_tags):
		version = tag.name.lstrip('v')
		if version not in pypi_releases:
			warning(f"No PyPI release found for tag '{tag.name}'. Skipping.")
			continue

		click.echo(f"Processing release for {version}")

		update_github_release(
				repo=repo,
				tag_name=tag.name,
				pypi_name=pypi_name,
				changelog=changelog,
				self_promotion=self_promotion,
				file_urls=pypi_releases[version],
				traceback=traceback
				)


def make_release_message(
		name: str,
		version: Union[str, float],
		release_date: datetime.date,
		changelog: str = '',
		self_promotion=True,
		) -> str:
	"""
	Create a release message.

	:param name: The name of the software.
	:param version: The version number of the new release.
	:param release_date: The date of the release.
	:param changelog: Optional block of text detailing changes made since the previous release.
	:no-default changelog:
	:param self_promotion: Show information about OctoCheese at the bottom of the release message.

	:return: The release message.

	.. versionchanged:: 0.1.0

		Added the ``self_promotion`` option.
	"""

	buf = StringList()

	if changelog:
		buf.extend(("### Changelog", changelog))
		buf.blankline(ensure_single=True)

	buf.append(f"Automatically copied from [PyPI](https://pypi.org/project/{name}/{version}).")
	buf.blankline(ensure_single=True)

	if self_promotion:
		footer_links = make_footer_links(
				"domdfcoding",
				"octocheese",
				event_date=release_date,
				docs_url="https://octocheese.readthedocs.io",
				)

		buf.extend(["---", '', "Powered by OctoCheese\\", footer_links])
		buf.blankline(ensure_single=True)

	buf.append(f"<!-- Octocheese: Last Updated {today()} -->")
	buf.blankline(ensure_single=True)

	return '\n'.join(buf)


#: Under normal circumstances returns :meth:`datetime.date.today`.
TODAY: datetime.date = datetime.date.today()


def today() -> str:
	return TODAY.strftime("%Y-%m-%d")


_FooterType = Literal["marketplace", "app"]


class UTCDateTime(datetime.datetime):  # pragma: no cover

	@functools.wraps(datetime.datetime.__new__)
	def __new__(cls, *args, **kwargs):
		d = datetime.datetime(*args, **kwargs)
		return d.astimezone(datetime.timezone.utc)

	@classmethod
	def strptime(cls, date_string, format):  # noqa: A002  # pylint: disable=redefined-builtin
		return datetime.datetime.strptime(date_string, format).astimezone(datetime.timezone.utc)

	@classmethod
	def utcnow(cls):
		return datetime.datetime.now().astimezone(datetime.timezone.utc)

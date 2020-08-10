# stdlib
import gzip
import pathlib
import tarfile
import tempfile
import zipfile
from urllib.parse import urlparse

# 3rd party
import pytest
from domdf_python_tools.words import get_words_list

# this package
from octocheese import Secret, get_file_from_pypi, get_pypi_releases


@pytest.mark.parametrize("value", get_words_list())
def test_secret(value):
	the_secret = Secret(value)
	assert isinstance(the_secret, str)
	assert isinstance(the_secret.value, str)
	assert the_secret.value == value
	assert the_secret == value
	assert str(the_secret) == "<SECRET>"
	assert repr(the_secret) == "'<SECRET>'"
	assert str([the_secret]) == "['<SECRET>']"
	assert str((the_secret, )) == "('<SECRET>',)"
	assert str({
			the_secret,
			}) == "{'<SECRET>'}"
	assert str({"token": the_secret}) == "{'token': '<SECRET>'}"
	assert hash(the_secret) == hash(value)


def uri_validator(x):
	# Based on https://stackoverflow.com/a/38020041/3092681
	# By https://stackoverflow.com/users/1668293/alemol and https://stackoverflow.com/users/953553/andilabs
	result = urlparse(x)
	return all([result.scheme, result.netloc, result.path])


def test_get_pypi_releases():
	releases = get_pypi_releases("octocheese")
	assert isinstance(releases, dict)

	release_url_list = releases["0.0.2"]
	assert isinstance(release_url_list, list)

	for url in release_url_list:
		print(url)
		assert isinstance(url, str)
		assert uri_validator(url)


def test_get_file_from_pypi():
	with tempfile.TemporaryDirectory() as tmpdir_:
		tmpdir = pathlib.Path(tmpdir_)

		url = (
				"https://files.pythonhosted.org/packages/fa/fb"
				"/d301018af3f22bdbf34b624037e851561914c244a26add8278e4e7273578/octocheese-0.0.2.tar.gz"
				)

		assert get_file_from_pypi(url, tmpdir)

		the_file = tmpdir / "octocheese-0.0.2.tar.gz"
		assert the_file.is_file()

		# Check it isn't a wheel or Windows-built sdist
		assert not zipfile.is_zipfile(the_file)

		with gzip.open(the_file, 'r'):
			# Check can be opened as gzip file
			assert True

		with tarfile.open(the_file, "r:gz") as tar:
			assert {f.name
					for f in tar.getmembers()} == {
							"octocheese-0.0.2",  # top level directory
							"octocheese-0.0.2/octocheese",  # module
							"octocheese-0.0.2/octocheese/__init__.py",
							"octocheese-0.0.2/octocheese/__main__.py",
							"octocheese-0.0.2/octocheese/action.py",
							"octocheese-0.0.2/octocheese/colours.py",
							"octocheese-0.0.2/octocheese/core.py",
							"octocheese-0.0.2/octocheese.egg-info",  # egg-info
							"octocheese-0.0.2/octocheese.egg-info/dependency_links.txt",
							"octocheese-0.0.2/octocheese.egg-info/entry_points.txt",
							"octocheese-0.0.2/octocheese.egg-info/not-zip-safe",
							"octocheese-0.0.2/octocheese.egg-info/PKG-INFO",
							"octocheese-0.0.2/octocheese.egg-info/requires.txt",
							"octocheese-0.0.2/octocheese.egg-info/SOURCES.txt",
							"octocheese-0.0.2/octocheese.egg-info/top_level.txt",
							"octocheese-0.0.2/__pkginfo__.py",  # metadata
							"octocheese-0.0.2/LICENSE",
							"octocheese-0.0.2/MANIFEST.in",
							"octocheese-0.0.2/PKG-INFO",
							"octocheese-0.0.2/README.rst",
							"octocheese-0.0.2/requirements.txt",
							"octocheese-0.0.2/setup.cfg",
							"octocheese-0.0.2/setup.py",
							}

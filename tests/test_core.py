# stdlib
import gzip
import pathlib
import tarfile
import tempfile
import zipfile
from datetime import date

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from shippinglabel.pypi import get_file_from_pypi

# this package
import octocheese.core


def test_get_file_from_pypi(advanced_data_regression: AdvancedDataRegressionFixture):
	with tempfile.TemporaryDirectory() as tmpdir_:
		tmpdir = pathlib.Path(tmpdir_)

		url = (
				"https://files.pythonhosted.org/packages/fa/fb"
				"/d301018af3f22bdbf34b624037e851561914c244a26add8278e4e7273578/octocheese-0.0.2.tar.gz"
				)

		get_file_from_pypi(url, tmpdir)

		the_file = tmpdir / "octocheese-0.0.2.tar.gz"
		assert the_file.is_file()

		# Check it isn't a wheel or Windows-built sdist
		assert not zipfile.is_zipfile(the_file)

		with gzip.open(the_file, 'r'):
			# Check can be opened as gzip file
			assert True

		listing = {
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

		with tarfile.open(the_file, "r:gz") as tar:
			assert {f.name for f in tar.getmembers()} == listing
			data_regression.check(sorted({f.name for f in tar.getmembers()}))


changelog = """\
* Added something
* Something was removed
* Something got deprecated
* It now works!
* Now encrypts data with [1024-bit RSA](https://www.bbc.co.uk/news/technology-55475433)
"""


@pytest.mark.parametrize("changelog", ['', pytest.param(changelog, id="content")])
@pytest.mark.parametrize("self_promotion", [True, False])
def test_make_release_message(
		advanced_data_regression: AdvancedFileRegressionFixture,
		self_promotion: bool,
		monkeypatch,
		changelog: str,
		):
	monkeypatch.setattr(octocheese.core, "TODAY", date(2020, 7, 4))

	release_message = octocheese.core.make_release_message(
			"octocat",
			"1.2.3",
			date(2020, 7, 4),
			changelog=changelog,
			self_promotion=self_promotion,
			)

	advanced_data_regression.check(release_message, extension=".md")

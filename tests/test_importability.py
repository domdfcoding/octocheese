# 3rd party
import pytest


@pytest.mark.parametrize(
		"module_or_package",
		[
				"octocheese",
				"octocheese.__main__",
				"octocheese.__init__",
				"octocheese.action",
				"octocheese.colours",
				"octocheese.core",
				]
		)
def test_importability(module_or_package):
	assert __import__(module_or_package)

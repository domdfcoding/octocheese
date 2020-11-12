# stdlib
import sys

# 3rd party
import pytest
from _pytest.mark import MarkDecorator
from domdf_python_tools.testing import not_windows


def not_mac(reason: str = "Not required on Windows.", ) -> MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current platform is macOS.

	:param reason: The reason to display when skipping.

	:rtype:

	.. versionadded:: 0.9.0
	"""  # noqa D400

	return pytest.mark.skipif(condition=sys.platform == "darwin", reason=reason)


@not_mac(reason="Docker does not work correctly on macOS.")
@not_windows(reason="Docker does not work correctly on Windows.")
def test_building(repo_root, docker_client):
	if not (repo_root / "Dockerfile").is_file():
		pytest.skip("Dockerfile not found.")

	print("Building Docker image")

	image, logs = docker_client.images.build(rm=True, path=str(repo_root))
	for line in logs:
		if "stream" in line:
			print(line["stream"], end='')
		sys.stdout.flush()

	print()

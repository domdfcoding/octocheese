# stdlib
import sys

# 3rd party
import pytest
from coincidence.selectors import not_docker, not_macos, not_windows


@not_docker(reason="Can't run if already in Docker.")
@not_macos(reason="Docker does not work correctly on macOS.")
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

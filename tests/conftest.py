# stdlib
import os
from pathlib import Path

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

pytest_plugins = ("pytest_docker_tools", "domdf_python_tools.testing")


@pytest.fixture()
def original_datadir(request):
	# Work around pycharm confusing datadir with test file.
	return Path(os.path.splitext(request.module.__file__)[0] + '_')


@pytest.fixture()
def fake_token(monkeypatch):
	monkeypatch.setenv("GITHUB_TOKEN", "1234")


@pytest.fixture()
def repo_root():
	return PathPlus(__file__).parent.parent

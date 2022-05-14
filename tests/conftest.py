# stdlib
from typing import Tuple

# 3rd party
import pytest
from betamax import Betamax  # type: ignore
from domdf_python_tools.paths import PathPlus

try:
	# 3rd party
	import pytest_docker_tools  # type: ignore
	pytest_plugins: Tuple[str, ...] = ("pytest_docker_tools", "coincidence", "github3_utils.testing")
except ImportError:
	pytest_plugins = ("coincidence", "github3_utils.testing")

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"


@pytest.fixture()
def fake_token(monkeypatch):
	monkeypatch.setenv("GITHUB_TOKEN", "1234")


@pytest.fixture()
def repo_root():
	return PathPlus(__file__).parent.parent

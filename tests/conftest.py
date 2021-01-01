# 3rd party
import pytest
from _pytest.fixtures import FixtureRequest
from betamax import Betamax
from domdf_python_tools.paths import PathPlus
from github3 import GitHub

pytest_plugins = ("pytest_docker_tools", "domdf_python_tools.testing")

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"


@pytest.fixture()
def fake_token(monkeypatch):
	monkeypatch.setenv("GITHUB_TOKEN", "1234")


@pytest.fixture()
def repo_root():
	return PathPlus(__file__).parent.parent


@pytest.fixture()
def github_client() -> GitHub:
	return GitHub(token="FAKE_TOKEN")  # nosec: B106


@pytest.fixture()
def cassette(request: FixtureRequest, github_client):
	with Betamax(github_client.session) as vcr:
		vcr.use_cassette(request.node.name, record="none")

		yield github_client


@pytest.fixture()
def module_cassette(request: FixtureRequest, github_client):
	cassette_name = request.module.__name__

	with Betamax(github_client.session) as vcr:
		vcr.use_cassette(cassette_name, record="none")
		# print(f"Using cassette {cassette_name!r}")

		yield github_client

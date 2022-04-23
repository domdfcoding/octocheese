# Test that the whole process works

# stdlib
import datetime
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

# 3rd party
import pytest
from coincidence import check_file_regression, with_fixed_datetime

# this package
from octocheese import copy_pypi_2_github


@pytest.mark.parametrize("pypi_name", [None, "sphinx-toolbox"])
def test_operation(module_cassette, github_client, file_regression, pypi_name):
	captured_out = StringIO()

	with redirect_stderr(captured_out):
		with redirect_stdout(captured_out):

			copy_pypi_2_github(
					github_client,
					"sphinx-toolbox",
					"sphinx-toolbox",
					pypi_name=pypi_name,
					self_promotion=True,
					)

	check_file_regression(captured_out.getvalue(), file_regression)


@pytest.mark.parametrize("max_tags", [1, 5, 10, 20])
def test_operation_max_tags(cassette, github_client, file_regression, max_tags):
	captured_out = StringIO()

	with redirect_stderr(captured_out):
		with redirect_stdout(captured_out):
			with with_fixed_datetime(datetime.datetime(2020, 1, 1)):

				copy_pypi_2_github(
						github_client,
						"sphinx-toolbox",
						"sphinx-toolbox",
						pypi_name="sphinx-toolbox",
						self_promotion=True,
						max_tags=max_tags,
						)

	check_file_regression(captured_out.getvalue(), file_regression)


def test_operation_prerelease(cassette, github_client, file_regression):
	captured_out = StringIO()

	with redirect_stderr(captured_out):
		with redirect_stdout(captured_out):

			copy_pypi_2_github(
					github_client,
					"octocheese-demo",
					"domdfcoding",
					pypi_name="sphinx-toolbox",
					self_promotion=True,
					)

	check_file_regression(captured_out.getvalue(), file_regression)

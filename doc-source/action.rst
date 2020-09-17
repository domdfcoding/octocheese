======================
GitHub Actions Usage
======================

In a GitHub Workflow:

.. code-block:: yaml

	name: "Copy PyPI to Releases"
	on:
	- push

	jobs:
	  releases:
		runs-on: ubuntu-latest
		steps:
		- uses: domdfcoding/octocheese@v0.0.2
		  with:
			pypi_name: "domdf_python_tools"
		  env:
			GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}


Configuration
----------------

.. confval:: pypi_name
	:type: str
	:required: True

	The name of the project on PyPI.

The ``GITHUB_TOKEN`` must also be supplied otherwise the action will fail.

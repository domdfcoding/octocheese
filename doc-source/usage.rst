======================
Script Usage
======================

Invoke using the ``octocheese`` command or ``python3 -m octocheese``.

.. prompt:: bash

	octocheese [-h] [-t TOKEN] [-r REPO] pypi_name

Positional Arguments
----------------------

.. cli-arg:: pypi_name
	:type: string

	The project name on PyPI.


Optional Arguments
--------------------

.. cli-arg:: -h --help

	Show the help text and exit.

.. cli-arg:: -t --token
	:type: string
	:metavar: TOKEN

	The token to authenticate with the GitHub API. Can also be provided via the ``GITHUB_TOKEN`` environment variable.

.. cli-arg:: -r --repo
	:type: string
	:metavar: REPO

	The repository name (in the format ``<username>/<repository>``) or the complete GitHub URL.

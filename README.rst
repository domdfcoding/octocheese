#############
OctoCheese
#############

.. start short_desc

**🐙 🧀 – Copy PyPI Packages to GitHub Releases**

.. end short_desc

This is a GitHub action, Python package and command line script that copies distribution files from PyPI ("The Cheese Shop") and adds them to the relevant tag in GitHub Releases.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/octocheese/latest?logo=read-the-docs
	:target: https://octocheese.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/octocheese/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/octocheese/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/octocheese/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/octocheese/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/octocheese/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/octocheese/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.herokuapp.com/github/domdfcoding/octocheese/badge.svg
	:target: https://dependency-dash.herokuapp.com/github/domdfcoding/octocheese/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/octocheese/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/octocheese?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/octocheese?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/octocheese
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/octocheese
	:target: https://pypi.org/project/octocheese/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/octocheese?logo=python&logoColor=white
	:target: https://pypi.org/project/octocheese/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/octocheese
	:target: https://pypi.org/project/octocheese/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/octocheese
	:target: https://pypi.org/project/octocheese/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/octocheese
	:target: https://github.com/domdfcoding/octocheese/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/octocheese
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/octocheese/v0.5.0
	:target: https://github.com/domdfcoding/octocheese/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/octocheese
	:target: https://github.com/domdfcoding/octocheese/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/octocheese
	:target: https://pypi.org/project/octocheese/
	:alt: PyPI - Downloads

.. end shields

|

GitHub Actions Usage
---------------------

In a GitHub Workflow:

.. code-block:: yaml

    name: "Copy PyPI to Releases"
    on:
    - push

    jobs:
      releases:
        runs-on: ubuntu-latest
        steps:
        - uses: domdfcoding/octocheese@master
          with:
            pypi_name: "domdf_python_tools"
          env:
            GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}


Installing as a Python package and script
------------------------------------------

.. start installation

``OctoCheese`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install octocheese

.. end installation

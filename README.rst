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
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/octocheese/latest?logo=read-the-docs
	:target: https://octocheese.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/octocheese/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://github.com/domdfcoding/octocheese/workflows/Linux%20Tests/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22Linux+Tests%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/octocheese/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/octocheese/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/octocheese/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Test Status

.. |requires| image:: https://requires.io/github/domdfcoding/octocheese/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/octocheese/requirements/?branch=master
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/octocheese/v0.2.1
	:target: https://github.com/domdfcoding/octocheese/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/octocheese
	:target: https://github.com/domdfcoding/octocheese/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/octocheese/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/octocheese/master
	:alt: pre-commit.ci status

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

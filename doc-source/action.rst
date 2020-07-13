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
        - uses: domdfcoding/octocheese@master
          with:
            pypi_name: "domdf_python_tools"
          env:
            GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}


There is only one configuration value, ``pypi_name``, which is the name of the project on PyPI.

The ``GITHUB_TOKEN`` must also be supplied otherwise the action will fail.

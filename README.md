# Copy PyPI Packages to GitHub Releases

[![Build Status](https://travis-ci.org/domdfcoding/copy_pypi_2_github.svg?branch=master)](https://travis-ci.org/domdfcoding/copy_pypi_2_github)
[![Test Coverage](https://codecov.io/gh/domdfcoding/copy_pypi_2_github/branch/master/graph/badge.svg)](https://codecov.io/gh/domdfcoding/copy_pypi_2_github)


This is a GitHub action that copies package files from PyPI and adds them to the relevant tag in GitHub Releases.

## How to use

Create a workflow for the action, for example:

```yaml
name: "Copy PyPI to Releases"
on: 
- push

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: domdfcoding/copy_pypi_2_github@master
```


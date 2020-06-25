FROM sphinxdoc/sphinx:2.4.4

LABEL "maintainer"="Dominic Davis-Foster <dominic@davis-foster.co.uk>"

ADD entrypoint.py /entrypoint.py
ADD copy_pypi_2_github /copy_pypi_2_github

ENTRYPOINT ["/entrypoint.py"]

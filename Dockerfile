FROM python:slim
LABEL "maintainer"="Dominic Davis-Foster <dominic@davis-foster.co.uk>"

ADD copy_pypi_2_github /copy_pypi_2_github
ADD requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt

ENTRYPOINT ["/copy_pypi_2_github/action.py"]

FROM python:3.8-slim
LABEL "maintainer"="Dominic Davis-Foster <dominic@davis-foster.co.uk>"

ADD . /octocheese
RUN python3 -m pip install /octocheese --prefer-binary
ENV GITHUB_TOKEN $GITHUB_TOKEN

ENTRYPOINT ["/octocheese/octocheese/action.py"]

#!/usr/bin/env python3
import os
import json
from copy_pypi_2_github import action

# This is the entrypoint called by GitHub when our action is run. All the
# GitHub specific setup is done here to make it easy to test the action code
# in isolation.
if __name__ == "__main__":
    print("[copy_pypi_2_github] Starting copy_pypi_2_github build.")

    if "INPUT_PRE-BUILD-COMMAND" in os.environ:
        pre_command = os.environ["INPUT_PRE-BUILD-COMMAND"]
        print("Running: {}".format(pre_command))
        os.system(pre_command)

    github_env = action.GithubEnvironment(
        build_command=os.environ.get("INPUT_BUILD-COMMAND"),
    )

    # We build the doc folder passed in the inputs.
    action.build_all_docs(github_env, [os.environ.get("INPUT_DOCS-FOLDER")])

# Pre-requisites: 

## Setup

Ensure you complete setup following [this guide](https://ploomber-contributing.readthedocs.io/en/latest/contributing/setup.html) 

## Review how to edit the content in this repository

To get familiar with additional dependencies and the format in this repository, follow [this guide](https://ploomber-contributing.readthedocs.io/en/latest/documentation/notebooks.html).

# Contributing content to this repository

Once you have completed the pre-requisites, you can pick one topic of the topics listed in the [README](https://github.com/ploomber/sql/blob/main/README.md). 

**Note** A place holder markdown (.md) file has already been created for each topic -> you can find them under the directory `course-material/`.

0. Fork this repository
1. Create a branch under your fork
2. Make and save changes on the selected .md file on your local computer
3. You can build the files locally via the command `jupyter-book build course-material/` (run from the repository root directory)
4. Take a look at the built webpage by navigating on your file browser under `sql/course-material/_build/html`
5. Create a pull request (base `ploomber/sql:main` from `<your_github_id>/sql:your-branch-name`)
6. Request to initialize the review process
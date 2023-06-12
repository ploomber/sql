# Pre-requisites: 

## Setup
0. Install Git
- First install Git if you do not have it on your computer. You can find [installation instructions here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
1. Clone this repository 
- Click on the "<>Code" green button found at the main GitHub page and copy the link under HTTPS. Then on your local computer, navigate to where you want this repository to be and run `git clone https://github.com/ploomber/sql.git`. This should all be run in your operating system's command line.
2. Run the conda environment for this repository
- Step 1: Install miniconda with `conda install`. Documentation on miniconda found here.
- Step 2: Navigate to the home directory of this repository (`/sql`) on your local machine's terminal
- Step 3: Run `conda env create -f environment.yml` in the terminal to create your environment with the default name "sql-course"
- Step 4: Activate your environment by running `conda activate sql-course`. You can also run `conda info --envs` and check if the asterisk symbol is at the "sql-course" environment.

## Review how to edit the content in this repository

To get familiar with additional dependencies and the format in this repository, follow [this guide](https://ploomber-contributing.readthedocs.io/en/latest/documentation/notebooks.html).

# Contributing content to this repository

Once you have completed the pre-requisites, you can pick one topic of the topics listed in the [README](https://github.com/ploomber/sql/blob/main/README.md). 

**Note** A place holder markdown (.md) file has already been created for each topic -> you can find them under the directory `course-material/`.

0. Fork this repository
1. Clone your fork into your local computer
2. Create a branch under your fork
3. Make and save changes on the selected .md file on your local computer
4. You can build the files locally via the command `jupyter-book build course-material/` (run from the repository root directory)
5. Take a look at the built webpage by navigating on your file browser under `sql/course-material/_build/html`
6. Create a pull request (base `ploomber/sql:main` from `<your_github_id>/sql:your-branch-name`)
7. Request to initialize the review process

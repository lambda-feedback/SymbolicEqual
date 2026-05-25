# Grading Script Template Repository

This template repository contains the boilerplate code needed in order to create an AWS Lambda function that can be written by any tutor to grade a response area in any way they like.

This version is specifically for python, however the ultimate goal is to make similar boilerplate repositories in any language, allowing tutors the freedom to code in what they feel most comfortable with.

## Deployment
[![Create Release Request](https://img.shields.io/badge/Create%20Release%20Request-blue?style=for-the-badge)](https://github.com/lambda-feedback/{SymbolicEqual}/issues/new?template=release-request.yml)
To deploy to production, update the README button above to point to the correct repository.

## Table of Contents

- [Repository Structure](#repository-structure)
- [How it works](#how-it-works)
  - [Docker & Amazon Web Services (AWS)](#docker-&-amazon-web-services-aws)
  - [Middleware Functions](#middleware-functions)
  - [GitHub Actions](#github-actions)
- [Pre-requisites](#pre-requisites)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [Best Practises](#best-practises)
  - [Coding](#coding)
  - [Testing](#testing)
  - [Deployement](#deployment)
- [Contact](#contact)

## Repository Structure

```bash
app/
    __init__.py
    algorithm.py # script to grade answers
    schema.json # schema to check the data is well structured
    requirements.txt # list of packages needed for algorithm.py

    tools/ # folder of middleware functions (for testing only)
        __init__.py
        app.py # main parsing, handling functions
        validate.py # script for validating request body using schema.json
        healthcheck.py # script for running tests in a JSON-encodable format

        Dockerfile # for building the base image
        tools_requirements.txt # packages needed by tools/

    tests/ # folder of scripts to check the algorithm and schema work
        __init__.py
        handling.py # for checking functions in tools/ work
        validation.py # for checking schema.json works
        grading.py # for checking algorithm.py works

    Dockerfile # for building whole image to deploy to AWS

.github/
    workflows/
        build-base-image.yml # for redeploying the base image to Docker Hub
        test-and-deploy.yml # for testing and deploying grading scripts to AWS

.gitignore
```

## How it works

### Docker & Amazon Web Services (AWS)

The grading scripts are hosted AWS Lambda, using containers to run a docker image of the app. Docker is a popular tool in software development that allows programs to be hosted on any machine by bundling all its requirements and dependencies into a single file called an **image**.

Images are run within **containers** on AWS, which give us a lot of flexibility over what programming language and packages/libraries can be used. For more information on Docker, read this [introduction to containerisation](https://www.freecodecamp.org/news/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b/). To learn more about AWS Lambda, click [here](https://geekflare.com/aws-lambda-for-beginners/).

### Middleware Functions

In order to run the algorithm and schema on AWS Lambda, some middleware functions have been provided to handle, validate and return the data so all you need to worry about is the grading script and schema.

The code needed to build the image using all the middleware functions are available in the repo under `tools/` as this allows you to test your code locally. Note, it is not possible to alter the middleware functions for your own grading script, as the final image deployed to AWS pulls the middleware functions from a base image stored on the Docker Hub.

### GitHub Actions

Whenever a commit is made to the GitHub repository, the new code will go through a pipeline, where it will be tested for syntax errors and code coverage. The pipeline used is called **GitHub Actions** and the scripts for these can be found in `.github/workflows/`.

On top of that, when starting a new grading script, you will have to complete a set of unit test scripts, which not only make sure your code is reliable, but also helps you to build a _specification_ for how the code should function before you start programming.

Once the code passes all these tests, it will then be uploaded to AWS and will be deployed and ready to go in only a few minutes.

## Pre-requisites

Although all programming can be done through the GitHub interface, it is recommended you do this locally on your machine. To do this, you must have installed:

- Python 3.8 or higher.

- GitHub Desktop or the `git` CLI.

- A code editor such as Atom, VS Code, or Sublime.

Copy this template over by clicking **Use this template** button found in the repository on GitHub. Save it to the `lambda-feedback` Organisation.

## Usage

### Getting Started

Begin by downloading the repository to your computer. This can be done either through GitHub Desktop or using the command:

```bash
git clone git@github.com:lambda-feedback/Grading-Script-Boilerplate.git
```

Navigate into the repository folder and open `algorithm.py`. Inside is a boilerplate function called `evaluation_function()` which is called when a grading request is made.

Next, open `tests/grading.py` and `tests/validation.py`. These scripts are used for building unit tests that check your algorithm and schema work as they should using a library called _unittest_.

Another unit test file is available called `handling.py`, however this is to test that the middleware functions work as they should so you shouldn't need to modify it.

An example unit test is in each file and for more information on using _unittest_, click [here](https://docs.python.org/3/library/unittest.html) to read the docs.

### Best Practises

### Coding

#### `algorithm.py`

#### `schema.json`

### Testing

#### `tests/grading.py`

#### `tests/validation.py`

### Deployment

## Contact

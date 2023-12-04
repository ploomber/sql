---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
---

# Deploying with Ploomber Cloud

## Introduction

Deploying artificial intelligence and machine learning applications can be a daunting task, especially when it comes to managing the underlying infrastructure. With Ploomber Cloud, you can enjoya  platform where AI/ML applications can be deployed with minimal hassle. Here's a comprehensive guide to getting started with Ploomber Cloud and leveraging its deployment capabilities, including its CLI and integration with GitHub for continuous deployment.

## Getting Started with Ploomber Cloud

1. Sign Up

First, head to the [Ploomber Cloud sign-up page](https://platform.ploomber.io/register) and create a free account using your email and a password.

2. Confirm Your Email

After signing up, check your inbox (and spam folder, just in case) for a confirmation email. Click the provided link to activate your account.

3. Sign In

Now, return to Ploomber Cloud and sign in with your credentials.

4. Deploy Your First App

Congratulations, you're all set! Next, explore how to deploy your first application.

## Acquiring an API Key
To interact with Ploomber Cloud, you'll need an [API key](https://docs.cloud.ploomber.io/en/latest/quickstart/apikey.html). After signing up, navigate to your account section and copy the API key.

## Deploying Applications via Command-Line Interface

Install the Ploomber Cloud package using `pip`:

```bash
pip install ploomber-cloud
```

Next, set your API key as an environment variable:

```bash
ploomber-cloud key YOURKEY
```

Initialize a New App

```bash
ploomber-cloud init
```

This will create a `ploomber-cloud.json` file in the directory where you ran the command. This file contains the configuration for your project. You can edit this file to customize your project's configuration. This is what it looks like:

```python
{
    "id": "APP_ID",
    "type": "APP_TYPE"
}
```

Where your `APP_ID` is a unique identifier created when you run the  `init` command and `APP_TYPE` is the type of application you're deploying (docker, streamlit, etc.)


After initialization, deploy your app using:

```bash
ploomber-cloud deploy
```

The deploy command provides a URL for tracking your deployment's progress.

## Integration with GitHub

Start by storing your API key as a GitHub secret in your repository. This is crucial for GitHub Actions to deploy your projects securely.

Configure GitHub Actions:

Add a YAML file in ``.github/workflows/ploomber-cloud.yaml`` to your repository. This file will contain the workflow configuration.

Sample Workflow Configuration (assumes you have set up a GitHub secret variable for GitHub actions called `ploomber-cloud-key` with your Ploomber API key):

```yaml
name: Ploomber cloud deploy,en

on:
  schedule:
    - cron: '0 0 * * *' 

jobs:

  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
          cd mini-projects/end-to-end/
          pip install ploomber-cloud
    - name: Set up credentials
      run: |
          ploomber-cloud key ${{ secrets.ploomber-cloud-key }}
    - name: Deploy to Ploomber cloud
      run: |
          ploomber-cloud deploy
```

The workflow configuration above will deploy your project every day at midnight. You can customize the schedule to suit your needs.

## Conclusion

Ploomber Cloud simplifies the deployment of AI/ML applications, eliminating the need for complex infrastructure management. With its easy setup, API key access, and seamless integration with GitHub Actions, deploying and updating your applications has never been easier. To get a hands-on experience, check out a complete sample project in the next blog. 



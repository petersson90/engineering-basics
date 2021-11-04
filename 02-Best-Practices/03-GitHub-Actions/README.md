
# Github Actions

Github Actions are a general way to execute any command in reaction to an event on your Github repository. A few details to consider:
- An event is any git action (push, new branch) but also Github-specific events (e.g. a new Pull Request is created)
- Only events on your remote Github repository will be considered; if you commit on your local machine but do not push, nothing will be triggered
- An action can be, really, anything: any shell command, another Github Action, etc.

A few examples of use cases:
- Send a Slack message when a new PR is created
- Run your project's tests and upload the tests outputs to S3
- Create a package of your project automatically after each push, so that your application is ready to deploy
- Deploy your project to production if we are merging a PR into the main branch and if all of the above succeeded!

:bulb: All these actions will be run on a server called a runner. The runner can be self-hosted, or one can be provided by Github.

:warning: Each job in a workflow will run on a separate runner. You can't have a job setup the environment and a second one running your tests as the second job will not be run on the previously prepared environment but on a new one. However this can be achieved in multiple steps within a single job.

# A first workflow

Let's write our first workflow. A workflow is defined in a YAML file by one or more events on which it should be triggered, and one or more jobs that will be run when the workflow is triggered. A job is defined by a series of steps, and each step can be either a shell command or another Github Action, imported either from the same repository or from another. If one step exits abnormally (i.e. the status code is different than 0) the whole workflow is stopped and the subsequent steps / jobs are not run.

:bulb: Github provides a marketplace of Actions that can be reused. They are provided either by Github itself (see https://github.com/actions) or by the community.

First, create a new empty project on your Github account and clone it. Don't create a new branch for now, we will push directly to the `master` branch. 

Then we need to create a special folder at the root of your project, that will be recognized by Github:

```bash
mkdir -p .github/workflows
```

Now let's create our workflow's file. It needs to be located in the `.github/workflows` directory, which will be detected by Github.

```bash
touch .github/workflows/first-workflow.yml
```

Add this to `first-workflow.yml`

```yaml
name: first-workflow
on: [push]
jobs:
  check-python-version:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: |
          python --version
```

Let's see line by line what we're doing:

```yaml
name: first-workflow
```

This is the name that will be displayed on the Github Action interface that we will use a bit later on.

```yaml
on: [push]
```

A list of events on which this workflow will be triggered. Here we're listening for git pushes only, meaning that this workflow will be automatically run when we `git push` this repository to Github.

```yaml
jobs:
```

A list of jobs, defined by the indentation. Here we have only one job, check-python-version.

```yaml
runs-on: ubuntu-latest
```

Our runner. Here we define that Github should provide us with a server running the latest version of Ubuntu.

```yaml
steps:
```

A list of steps for the current job. All these steps will be run one by one in the same environment.

```yaml
- uses: actions/checkout@v2
```

The first step. This will almost always be exactly this one. "uses" indicates that we are using another Github Action. "actions" here actually means the "actions" Github workspace, and "actions/checkout" the Github repository https://github.com/actions/checkout on which the action is hosted. This action checks-out your repository on the commit that triggered the workflow.

```yaml
- uses: actions/setup-python@v2
```

Second step. Same here, we're using the external [setup-python](https://github.com/actions/setup-python) Action. It will download and install Python for the current job.

```yaml
with:
        python-version: '3.9'
```

"with" indicates that we are providing parameters to the external Action being used (here actions/setup-python). We indicate that we want a Python 3.9 version.

```yaml
- run: |
      python --version
```

Here we're not using `uses` but `run` which indicates we will run some shell commands. The pipe `|` indicates that the script can be multi-line. It's not the case here but we could have added another command below, or we could have simply written `- run: python --version`.

Let's try it! Add, commit and push the file to your remote repository.

Once you pushed it, go to the Github interface, on your project page, and click on the "Actions" tab. After a few seconds you should see your workflow appear on the left side, below "All workflows", and you should see an instance of your workflow currently running.

<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/gh_action_workflow_home.jpg?raw=true" width="900"></p>

Click on the workflow run to access this run's page:

<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/gh_action_workflow_progress.jpg?raw=true" width="900"></p>

Here we have only one job, python-check-version. Click on it to have more details:

<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/gh_action_workflow_details.jpg?raw=true" width="750"></p>

You can toggle any step to get its output:

<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/gh_action_python_version.jpg?raw=true" width="300"></p>


:bulb: You can see that two more steps were run after `python --version`. `Post Run actions/checkout@v2` was automatically added at the end of your workflow by our first step `actions/checkout@v2`. Click on it to see what it does! Basically it unsets git settings to make sure they will never be accessible again. Mainly useful when we set up authentication credentials. `Complete job` is added by Github for internal operations.

# Exercises

:bulb: In the following exercises, keep in mind that there is a [marketplace](https://github.com/marketplace?type=actions) with many ready-to-use actions!

For the purpose of the exercise we will install the following dependencies:

```bash
pipenv --python 3.9
pipenv install nose pylint --dev
```

We can commit this:

```bash
git add Pipfile* && git commit -m "add python dependencies"
```

Let's also add a test file. Create a `app/tests` directory:

```bash
mkdir -p app/tests && touch app/__init__.py && touch app/tests/test_example.py
```

And add this `test_example.py` file:

```python
# tests/test_example.py
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

from unittest import TestCase
import pylint

class TestExample(TestCase):

    def test_example(self):
        self.assertIsNotNone(pylint)
```

Commit!
```bash
git add app && git commit -m "add first app files"
```

## Exercise 1

Create a new workflow that will:
- React on push and pull requests (have a look at the [documentation](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows)!)
- Have one job with the following steps:
    - Checkout the branch
    - Install the dependencies (hint: have a look at the [setup-python](https://github.com/actions/setup-python) workflow)
    - Run the linter on the `app` directory
    - Run the tests

:bulb: Remember that in order to test your workflow, you have to commit & push it to Github.

<details><summary markdown="span">View solution
</summary>


```yaml
name: Python Linter & Tests

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
        pipenv install --dev
    - name: Lint with pylint
      run: |
        pipenv run pylint app
    - name: Test with nose
      run: |
        pipenv run nosetests
```
</details>


:tada: Congratulations! You have set up a first CI pipeline on your project :tada:

## Going further before exercise 2
### Context

Github provides context variables that can be used to retrieve many internal pieces of information (current run number, the workflow name, the git branch name, etc.). Unlike environment variables, context variables are re-evaluated between each step and become hard-coded values at execution time.

For example, `github.event_name` contains the name of the event that triggered the workflow run. In order to access the value, use the expression syntax: `${{ github.event_name }}`

:bulb: See [contexts](https://docs.github.com/en/actions/learn-github-actions/contexts) for all available context variables and [expressions](https://docs.github.com/en/actions/learn-github-actions/expressions) for the expression syntax.

### Secrets

One of the available context variables is `secrets`, which allows you to access special variables that are used for authentication purposes. You can define them yourself (for instance by creating one from the Github interface in your account by going to Settings => Secrets) but one is made available by Github during the workflow execution: `${{ secrets.GITHUB_TOKEN }}`. 

At the start of each workflow run, Github automatically creates a unique `GITHUB_TOKEN` secret and makes it accessible to the workflow. This token can be used to authenticate and bring changes to the repository for which it is currently running; for example add a comment, create a Pull Request, add a reviewer, etc.

### Conditions

You can conditionally execute a step or a job with the "if" syntax. For instance, if you want to run a step or a job only if the current event is triggered on the "master" branch, we can add the following at the step (or job) level:

```yaml
if: ${{ github.ref == 'refs/heads/master' }}
```

You can set a condition at a job level or at a step level.

## Exercise 2

:warning: **Do not commit your changes to `master` directly.** Create a branch first with e.g.:

```bash
git checkout -b test_workflow
```

Let's go! Add another job to the workflow from exercise 1 (**work on the same file, don't create another one!**) which will create a pull request (PR) with the following requirements:
- The new job will be named `review` 
- The PR should be created only if we are **not** on the `master` branch
- The PR title should have the following format: `Awesome PR by <actor>` where `<actor>` is the Github username of the person who triggered the workflow
- This new job should only be executed if the previous `build` job that we created above succeeded

<details><summary markdown="span">Hints (only read them after at least a first try!)
</summary>

- You can use the [pull-request](https://github.com/marketplace/actions/github-pull-request-action) workflow. Look at its documentation to know how to use it.
- You can use the `needs` keyword at the job level in order to define dependencies between jobs. For instance, a job with `needs: job1` will run only when `job1` has run and has succeeded.

</details>


<details><summary markdown="span">Solution (only look if you tried very hard!)
</summary>

Complete YAML file:

```yaml
name: Python Linter & Tests

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
        pipenv install --dev
    - name: Lint with pylint
      run: |
        pipenv run pylint app
    - name: Test with nose
      run: |
        pipenv run nosetests

  review:
    runs-on: ubuntu-latest
    needs: build
    if: ${{ github.ref != 'refs/heads/master' }}
    steps:
      - uses: actions/checkout@v2
      - name: Create Pull Request
        uses: repo-sync/pull-request@v2
        with:
          source_branch: ""
          destination_branch: "master"
          github_token: ${{ secrets.GITHUB_TOKEN }}
          pr_title: "Awesome PR by ${{ github.actor }}"
```

</details>


## I'm done!

Before you jump to the next exercise, let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/engineering-basics
cd 02-Best-Practices/03-GitHub-Actions
touch DONE.md
git add DONE.md && git commit -m "02-Best-Practices/03-GitHub-Actions done"
git push origin master
```

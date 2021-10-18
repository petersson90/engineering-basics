# Sum of Three

Let's start with a very simple exercise to understand how these exercises are going to work.

## Getting started

```bash
cd ~/code/<user.github_nickname>/reboot-python
git pull upstream master # Retrieve the latest version of the exercise

cd 01-OOP/01-Sum-Of-Three
subl . # Open the folder in Sublime Text
```

## Procedure

Your goal is to implement the method `sum3` in the `sum_of_three.py` file. Before you actually try to do it, run the **tests** that we prepared:

```bash
nosetests
```

You should get three failing tests. Read the error (especially the `AssertionError`) to understand what is wrong and try implementing the `sum3` method. When you are done, run the command above once again.

Repeat until all tests turn pass (i.e. `0 FAILED`)

Then check your style with:

```bash
pipenv run pylint sum_of_three.py
```

If you get style errors, fix them, save and re-run the command above.

## Conclusion

The goal of this exercise was to show you how to run the tests to automatically evaluate your code (both style & content) and introduce you to this tight feedback loop.

## (Optional) PowerShell

If you work in a Windows environment, you will benefit from learning [**Powershell**](https://docs.microsoft.com/powershell/), and you can actually use it on macOS and Linux too.

Let's write our very first PowerShell script. Open the `hello.ps1` file in Sublime Text and copy-paste the following [`Write-Output`](https://docs.microsoft.com/powershell/module/microsoft.powershell.utility/write-output) instruction:

```powershell
Write-Output "Hello World"
```

Then you can run the script from Git Bash with:

```bash
powershell -ExecutionPolicy bypass ./hello.ps1
```

You should get a `Hello World` output! If you don't, ask a TA.

You may not have administrative rights on the computer you are working on, that's why the `-ExecutionPolicy bypass` flag is needed. On a computer you are administrator on, you can set up the policy to `RemoteSigned` by [reading the documentation](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-6). It will override a Registry key.

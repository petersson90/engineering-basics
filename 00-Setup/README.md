
:bulb: **Tip**: if you can see this tip your Github account is correctly linked, you can go on with the setup!

## GitHub

We will use your personal public `github.com` account. If you are reading this, it means that you have one and are logged in with it!

First, ensure to have this repository forked to your own personal github account

We need to create a SSH key on your computer and link it to your GitHub account. At the end of the week, don't forget to remove this key from your GitHub account as this is not your computer. Protecting your key with a strong **passphrase** will guarantee security during the week.

GitHub has handy tutorials. Follow them:

1. [Generate a new SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-windows)
1. [Add this key to your GitHub account](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-windows)

To check if this step is done, run:

```bash
ssh -T git@github.com
```

If it says "Permission denied", call a teacher to help you. If it says "Hi <github_nickname>", all good!

At last, we need to configure the local `git` command to tell it who you are when you make a commit:

```bash
git config --global user.email "your_github_email@domain.com"
git config --global user.name "Your Full Name"
```

It's important to use the same email as the one you use on [GitHub](https://github.com/settings/emails) so that [commits are linked to your profile](https://help.github.com/articles/why-are-my-commits-linked-to-the-wrong-user/#commits-are-not-linked-to-any-user).


## Exercises

The repository which you just forked contains all the exercises for the week. To work on them, clone them on your laptop. Still in Git Bash, run:

```bash
mkdir -p ~/code/<user.github_nickname> && cd $_
git clone git@github.com:<user.github_nickname>/reboot-python.git
cd reboot-python
git remote add upstream git@github.com:lewagon/reboot-python.git

pwd # This is your exercise repository!
```

This repository has a `Pipfile`. You now can easily install dependencies with the following command:

```bash
pipenv install --dev # to install `packages` **and** `dev-packages`
```

It will create the Virtualenv for this folder, using Python 3.8 as [specified](https://github.com/lewagon/reboot-python/blob/master/Pipfile#L15-L16)

## Getting the green dot

For each challenge, we encourage you to **commit** and **push** your progression. Let's start now with:

```bash
cd 00-Setup
touch READY
git add READY
git commit -m "I am ready"
git push origin master
```

You should get a green dot in the left to track your progression. Cheers!
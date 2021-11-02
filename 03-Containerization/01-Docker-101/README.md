# Docker 101

🎯 The purpose of this exercise is to:

* validate the Docker Desktop installation
* guide you through common Docker commands, using the `docker` CLI,
* while giving some details about them and the associated Docker concepts

---

## 0. Installation validation ✅
### 0.a. Is Docker Desktop already installed ? 🐳

You should already have Docker Desktop installed on your computer - as part of the **"Before your training"** section on Learn.


👀 If you see a whale icon in the status bar stays steady, **Docker Desktop** is up-and-running, and is accessible from any terminal window. You are good to go ✅
<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/status-bar.png?raw=true" width="250"></p>

👀 If you don't see this whale icon, but already have **Docker Desktop** installed on your machine, simply sart it ! Wait for the whale icon to be steady and you are good to go ✅
<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/docker-desktop.png?raw=true" width="400"></p>


👀 If you do not have **Docker Desktop** installed :point_right: please check out the **"Before your training"** section (here, on Learn) and follow the installation steps.

---

Let's now make sure that everything is fine, and get familiar with the concepts introduced in lecture.

### 0.b. Docker Hub 💻

##### Sign up
Docker Hub is a hosted repository service provided by Docker for finding and sharing container images with your team. Once you create a Docker ID (a user), you will be able to pull and push images to the Hub.

Create a personal account 👉  [here](https://hub.docker.com/signup).

##### Login 🔑

Open a terminal and type:
```bash
docker login
```

You will be prompted for your username and password:
<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/docker-login.png?raw=true" width="700"></p>

When successful, your terminal should tell you "Login Succeeded" 🙌!

---

### 0.c. Hello-World ! 👋

Let's validate our Docker installation by running our first container: `hello-world`. To do so, run the following in your terminal:

```bash
docker run hello-world
```

Since you do not have any docker images on your host (as you just installed docker),

* it will first pull the `hello-world` image from the Hub
* then run a container from this image (this one _only_ prints a message)

You should end up with something like this:
<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/hello-world.png?raw=true" width="700"></p>


##### To see the containers you have running on your host 👀:

```
docker ps
```

You don't see any 🤔 ? That's normal !
Your `hello-world` container is not running anymore: it exited as soon as it was done. Its job was simply to print a message.

In fact, the `docker ps` command can take arguments: the documentation can retrieved [here](https://docs.docker.com/engine/reference/commandline/ps/), or you could ask for the command usage with `docker ps --help`.

##### To view all containers (even non-running ones), run:
```
docker ps -a
```

You should see a container here. What is its name ? Which image was used to run it ? What is its state ?

##### To view images on your host:
```
docker images
```

You should see your `hello-world` image, freshly pulled. You also have access to other details such as

* the image ID,
* the image tag (used to convey important information about the image. By default, the tag is "latest". You can have a look at [this list of tags](https://hub.docker.com/_/python): do you understand what they are here for ?),
* the image size

---

## 1. Common Docker commands

### 1.a. Run a container

The [**`docker run`**](https://docs.docker.com/engine/reference/run/) command is used to run a container from an image: you should pass the image name to it, like `docker run <SOME_IMAGE>`.
<br>
👉 For instance, run a container from the `postgres` image. You can see [here](https://hub.docker.com/_/postgres) that the postgres image is available on the Hub !

<details><summary markdown='span'>View solution</summary>

```bash
docker run postgres
```

</details>

It will run an instance of the postgres database (that you know from previous exercise: we used it for our Twitter API). How 🤔 ?

- Docker will use the image from the host (your machine) if it exists
- If the image is not present on the host, it will go to the Docker Hub and pull the image for you 👌!

Note that for the subsequent executions, the same image will be re-used. Your machine won't have to pull the image over and over.

But notice that when you ran `docker run postgres`, it actually did not work ! Why ?


<details><summary markdown='span'>View solution</summary>

```bash
Error: Database is uninitialized and superuser password is not specified.
   You must specify POSTGRES_PASSWORD to a non-empty value for the
   superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".
```
Well, it looks like the postgres image is expecting something on `docker run`!

</details>

👉 Try to fix it !

<details><summary markdown='span'>View solution</summary>

Well let's just do what `docker run` asks for:

```bash
docker run -e POSTGRES_PASSWORD=password postgres
```

</details>

🍾 That's it! No need for a complex installer, no conflicts on your laptop, no long hours scrolling tech forums to fix your problem : you have a running database in a single command.


The `-e` flag in `docker run -e ...` stands for environment variable. Here, we just created a password for the database superuser, and passed it to the `docker run` command. Ideally a password should be more complex and we should not provide it from the command line, but here we'll do it this way for simplicity's sake.


Now, you should see an output in your terminal: it looks like your database is initialized and ready to accept connections!

<details><summary markdown='span'>View solution</summary>

Your terminal output should look like this:

```bash
...
PostgreSQL init process complete; ready for start up.

2020-11-19 19:00:28.075 UTC [1] LOG:  starting PostgreSQL 13.1 (Debian 13.1-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
2020-11-19 19:00:28.076 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2020-11-19 19:00:28.076 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2020-11-19 19:00:28.079 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2020-11-19 19:00:28.084 UTC [56] LOG:  database system was shut down at 2020-11-19 19:00:27 UTC
2020-11-19 19:00:28.091 UTC [1] LOG:  database system is ready to accept connections
```

</details>


👉 Stop the container by hitting CTRL-C.

---

### 1.b. Run a container in the background

One other thing you can do, is run a container in the background (using the "detached" mode). This way, your terminal prompt will be available.

👉 Try run a new postgres container in detached mode, and give it a name: `pg`.

<details><summary markdown='span'>Hint</summary>

If you are not sure about the syntax and available options: ask for them !
```bash
docker run --help
```

</details>

<details><summary markdown='span'>View solution</summary>

```bash
docker run -d -e POSTGRES_PASSWORD=password --name=pg postgres
```

</details>


What happens if we do not give it a name ?
👉 Run another postgres container without giving it a name: what name has it been assigned ?

<details><summary markdown='span'>Hint</summary>

Do you remember how to list all running containers ?

</details>
<details><summary markdown='span'>View solution</summary>

```bash
docker run -d -e POSTGRES_PASSWORD=password postgres
docker ps
```

Well Docker generates some names for us if we do not pass any.

</details>

---

### 1.c. Access the Postgres database

Now that your container is running, you might want to run a SQL query.
Let's first get a bash shell in the container:

👉 Run ```docker exec -it pg /bin/bash```

What have we done here 🤔 ? We have asked Docker to run a command (`/bin/bash`: to get a bash shell) in the container, passing the flag `-i` and `-t` together:

* the `-i` flag stands for "interactive" mode: it gets us a standard input **stdin** (by default, a container runs in a non-interactive mode: it does not listen for input from your side). To provide an input, you need to pass this `-i` flag.
* the `-t` flag stands for "tty", and is a Unix-like operating system command: with this flag, you will get a "prompt"

So the combination of these two flags give us access to a "terminal", in the container 🎉 !

We can now access our DB using the `psql` CLI:

👉 Run ```psql -U postgres```

It gives you access to the Postgresql command line, where you could write SQL.

<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/psql-docker.png?raw=true" width="500"></p>

👉 Exit the `psql` prompt: `\q` + **Enter**
👉 Exit the container bash shell: `exit` + **Enter**


That is typically what developers do locally when they work on a webapp project (like you did for the Twitter API): they dockerize the webserver application, and the database. This way their setup is standardized, and they can easily share it !

---

### 1.d. Clean up

#### stop & remove containers

To stop a container, use the [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop/) command. You will need to pass the container ID, or the container name.

👉 Stop your `pg` container, and check the list of running containers, and the list of non-running containers.


<details><summary markdown='span'>View solution</summary>

Stop the container:
```bash
docker stop pg
```

And list running and exited containers:
```bash
docker ps
docker ps --filter "status=exited"
```
</details>

You should see that your container changed state, from `running` to `exited`, but it is still here ! To remove it from your host, run the `docker rm` command.

👉 Remove your postgres container

<details><summary markdown='span'>Hint</summary>

```bash
docker rm --help
```

</details>
<details><summary markdown='span'>View solution</summary>

```bash
docker rm pg
```

</details>

#### remove an image

So you have stopped and removed your postgres container, but how about the postgres image that your host initially pulled from the Docker Hub.

👉 Do you remember how to list docker images ?

<details><summary markdown='span'>View solution</summary>

```bash
docker images
```

</details>

👉 Try to remove the `postgres` image using [`docker rmi`](https://docs.docker.com/engine/reference/commandline/rmi/) and double check it worked

<details><summary markdown='span'>View solution</summary>

```bash
docker rmi postgres
docker images
```

If you have other containers on your host using the `postgres` image, you will not be able to remove the image... Get rid of the containers first ! You already know how to do so !

</details>

---

### 1.e. Dockerfile, docker build, docker push

Let's recap what we just did:

* we ran a `pg` container from the `postgres` image
* we stopped it
* we removed it from the host
* we also removed its image

That was convenient because we wanted to play with the Postgres image - already available on the Hub.

🤔 But what if we wanted to create our own image ? And put it on the Hub to make it available for other projects, other developers ?

Well, we would have to:

* ➡️ write a `Dockerfile`,
* ➡️ build our Docker container,
* ➡️ push it onto the Docker Hub !

💪 **Let's do this !**


We will play with the `docker/whalesay` image, and create a custom image out of it.

👉 Pull the `docker/whalesay` image from the Hub


<details><summary markdown='span'>Hint</summary>

You already know how to pull an image ! If you don't remember, run

```bash
docker pull --help
```

</details>
<details><summary markdown='span'>View solution</summary>

```bash
docker pull docker/whalesay
```

</details>

👉 Run a container from this image (please check [how to use this image](https://hub.docker.com/r/docker/whalesay/))

<details><summary markdown='span'>View solution</summary>

```bash
docker run docker/whalesay cowsay "This whale is speaking ..."
```

</details>


From there, we would like to modify this image, such that the whale automatically "says" something (randomly generated).

We would like to run something like: ```docker run <YOUR DOCKER ID>/custom-whale``` that generates a famous quote.

So we need different things here:
* build a new image from the `docker/whalesay` image: you already know we will have to write a [Dockerfile](https://docs.docker.com/engine/reference/builder/)
* be able to generate random quotes: we will be using [Unix Fortune](https://en.wikipedia.org/wiki/Fortune_(Unix))
* push this built image to your personal Docker Hub repository


👉 Create a file named Dockerfile in this challenge folder

```bash
cd ~/code/<user.github_nickname>/engineering-basics
cd 03-API-and-Back-End/04-Docker-101
touch Dockerfile
```

👉 Copy and paste the following text in it

```dockerfile
FROM docker/whalesay:latest
RUN apt-get -y update && apt-get install -y fortunes
CMD /usr/games/fortune -a | cowsay
```

What does it do ?

---

```dockerfile
FROM docker/whalesay:latest
```

> The **FROM** instruction initializes a new build stage and sets the Base Image for subsequent instructions. Here, we make use of the `docker/whalesay` image (its `latest` version) and build our custom image out of it.

```dockerfile
RUN apt-get -y update && apt-get install -y fortunes
```

> The **RUN** instruction will execute any commands in a new layer on top of the current image and commit the results. Each line of Dockerfile represents a "layer" of the full image.
Here, the command updates the list of available packages and their versions, and install the `fortune` program for random quote generation.

```dockerfile
CMD /usr/games/fortune -a | cowsay
```

> There can only be one **CMD** instruction in a Dockerfile. The main purpose of a **CMD** is to provide defaults for an executing container.
Here, the trick is to make use of the "pipe" (`|`) that will first generate a random quote (using `/usr/games/fortune -a`) and pass it to the [`cowsay`](https://en.wikipedia.org/wiki/Cowsay) command.

---

👉 It's now time to build your image: ```docker build -t $DOCKER_ID/custom-whale .```  - which will read instructions from the Dockerfile. Do not forget to replace `$DOCKER_ID` with your actual docker ID ⚠️ !

<details><summary markdown='span'>You should see that it has been built layer by layer.</summary>

```bash
Sending build context to Docker daemon  2.048kB
Step 1/3 : FROM docker/whalesay:latest
 ---> 6b362a9f73eb
Step 2/3 : RUN apt-get -y update && apt-get install -y fortunes
 ---> Running in 4112a9cbddcd
...
...
Removing intermediate container 4112a9cbddcd
 ---> b02c2255a8e6
Step 3/3 : CMD /usr/games/fortune -a | cowsay
 ---> Running in 3e2cd7673b16
Removing intermediate container 3e2cd7673b16
 ---> 23e6cedd0cfe
Successfully built 23e6cedd0cfe
Successfully tagged $DOCKER_ID/custom-whale:latest
```

</details>


👉 Run it to see what it does

<details><summary markdown='span'>View solution</summary>

```bash
docker run $DOCKER_ID/custom-whale
```

</details>

👉 Run it again ! It should generate different quotes each time - as they are randomized

👉 You can now push your image to your own repository on the Docker Hub. Make sure you are logged in:
```docker login``` and run the following:

```bash
docker push $DOCKER_ID/custom-whale
```

This way, since it is public, anyone would be able to pull it and run it as a container.

👉 Same as what we saw for the Postgres image, you can see it listed [here](https://hub.docker.com/)

👉 Some people went even further ... Try this one: ```docker run -it --rm danielkraic/asciiquarium``` !

---

## I'm done! 🎉

That's it for this challenge ! Congratulations, you have seen how to:
- pull an image (`docker pull $IMAGE_NAME`)
- run a container from an image (`docker run $IMAGE_NAME`)
- run a command in a running container (`docker exec -it $CONTAINER_NAME $SOME_COMMAND`)
- list your containers and images (`docker ps`, `docker ps -a`, `docker images`)
- stop and remove a container (`docker stop $CONTAINER_NAME`, `docker rm $CONTAINER_NAME`)
- remove an image (`docker rmi $IMAGE_NAME`)
- write a Dockerfile
- build an image from a Dockerfile and tag it (`docker build -t $SOME_NAME .`)
- push an image to the Docker Hub (`docker push $YOUR_IMAGE`)

So you already know all the base commands to interact with images and containers !

Before you jump to the next challenge (Twitter-API), let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/engineering-basics
cd 03-API-and-Back-End/04-Docker-101
touch DONE.md
git add DONE.md && git commit -m "03-API-and-Back-End/04-Docker-101"
git push origin master
```

<!--
  @author: adibarra (Alec Ibarra)
  @description: This is the README page for the project.
-->

# QueryQuest

<h3 align="center"><strong>QueryQuest - A trivia game</strong></h3>

<h3 align="center">
  <a href="#tooling">Tooling</a> •
  <a href="#environment-setup">Environment Setup</a> •
  <a href="#run-project">Run Project</a> •
  <a href="#license">License</a>
</h3>

## Overview

This is our group project for CS 4347 Database Systems. Our goal is to create a trivia game that allows users to compete against each other for the highest score on the leaderboard. The game will have a variety of categories and questions that are randomly selected for each game. The game will be built using a full-stack web application with a PostgreSQL database for storing user data and game information. The backend will be built using Python and FastAPI, while the frontend will be built using Vue.js.

There is a live demo of the project which deploys the latest changes from the `main` branch. You can access the demo [here](https://queryquest.adibarra.com).

## Tooling

#### VSCode

VSCode is **highly recommended**, the repo is currently set up to take advantage of devcontainers which automatically set up all dependencies for you. This is the easiest way to get the project up and running. Instructions for installing VSCode can be found [here](https://code.visualstudio.com/download).

#### Docker

If you want to take advantage of the devcontainer then docker is **required**. If you are planning on setting up the environment manually then it is not needed. Instructions for installing Docker can be found [here](https://www.docker.com/products/docker-desktop/).

## Environment Setup

This is a one-time setup. If you have already done this, you can skip to the next section.

1.  Open Docker Desktop. Make sure it is updated and running before continuing.
2.  Open VSCode and install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
3.  In VSCode, press `Ctrl+Shift+P` and type `Git: Clone`.
4.  You may be prompted to login to your GitHub account. Sign in.
5.  Type `adibarra/queryquest`. Select it.
6.  If prompted, select the `main` branch.
7.  Once cloned, you should see a popup in the bottom right corner of the screen. Click `Reopen in Container`.
8.  Let the container build. This will take **2-5 minutes** depending on your machine (only the first time).
9.  Once the build is complete, you can begin development.
10. Make sure to fill out the `.env` files with the appropriate values.

<details>
<summary>Manual Environment Setup</summary>
The devcontainer does all of this for you.

1. Install [Python3](https://www.python.org/downloads/) for your platform.
2. Install [nvm](https://github.com/nvm-sh/nvm) for your platform.
3. Git clone the repository.
4. Run the following commands:

```bash
  $ nvm use || nvm install --lts
  $ corepack enable
  $ corepack install
  $ cp --no-clobber .env.example .env.production
  $ cp --no-clobber .env.example .env.development
```

5. Additionally, make sure to fill out the `.env` files with the appropriate values.
</details>

## Reconnect to Environment (devcontainer)

You can re-attach the devcontainer by doing the following from a new VSCode window:

1. Click the `Remote Explorer` tab.
2. Select `Dev Containers` in the dropdown menu.
3. Find the `queryquest` container.
4. Click the `→` button to re-attach the container.
5. You can now continue development.

## Run Project

Make sure you are in the repo's root directory before running these commands.

```bash
  # # # # # # # # # # # # # # # # # # # # # # # #
  # Start the development environment           #
  # Access the app here: http://localhost:3333  #
  # # # # # # # # # # # # # # # # # # # # # # # #
  $ pnpm dev

  # --- OR ---

  # # # # # # # # # # # # # # # # # # # # # # # #
  # Build and run for production (preview mode) #
  # Access the app here: http://localhost:3000  #
  # # # # # # # # # # # # # # # # # # # # # # # #
  $ pnpm preview
```

## Project Scripts

| Scripts        | Description                                        |
| -------------- | -------------------------------------------------- |
| pnpm install   | installs dependencies for entire project           |
| pnpm dev       | runs development environment                       |
| pnpm clean     | removes build artifacts                            |
| pnpm clean:all | removes build artifacts and dependencies           |
| pnpm lint      | prints warnings about code formatting              |
| pnpm lint:fix  | auto-fixes the code formatting                     |
| pnpm typecheck | checks for type errors in the code                 |
| pnpm build     | builds the app for production                      |
| pnpm preview   | runs the full built app in production preview mode |

## License

All rights reserved.

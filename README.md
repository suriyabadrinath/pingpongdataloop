# Ping-Pong Game with FastAPI

This project implements a ping-pong game using two FastAPI servers that send "ping" and "pong" requests back and forth. The game is controlled via a command-line interface (CLI) which allows starting, pausing, resuming, and stopping the game.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Servers](#running-the-servers)
- [Usage](#usage)
- [CLI Commands](#cli-commands)
- [Pushing to GitHub](#pushing-to-github)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Project Overview

This project simulates a ping-pong game between two servers using HTTP requests. The game runs with two FastAPI servers exchanging "ping" and "pong" messages. The game can be started, paused, resumed, and stopped using a CLI tool.

- Server 1 starts by sending a "ping" to Server 2.
- Server 2 responds with "pong" and sends a "ping" back to Server 1 after a configurable delay.
- The game continues as long as it is not paused or stopped.

## Architecture

- **FastAPI Servers**: Two FastAPI servers (`server.py`) that communicate by sending "ping" and "pong" requests back and forth.
- **CLI Tool**: A command-line tool (`pong_cli.py`) that allows starting, pausing, resuming, and stopping the game.

## Requirements

- Python 3.x
- FastAPI
- Uvicorn
- Requests (for sending HTTP requests)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/suriyabadrinath/pingpongdataloop.git
   cd pingpongdataloop

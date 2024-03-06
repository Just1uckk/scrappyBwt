# Scrapy BWT Test Project

This is a test project based on real situations.

The task was:
- Collect information about businesses based on links from the site’s sitemap.
- Collect detailed information of each business.
- Recheck the collected information and export it to a csv table and provide it to the user

## Features

- Python 3.6+
- [Poetry](https://github.com/python-poetry/poetry) for dependency management
- SQLAlchemy ORM with alembic migrations
- RabbitMQ integrated via [pika](https://github.com/pika/pika/)
- configuration via ENV variables and/or `.env` file
- single file for each class
- code generation scripts for classes: spiders, pipelines, etc. (see [this section](#code-generation))
- [Black](https://github.com/psf/black) to ensure codestyle consistency (see [here](#black))
- PM2-ready (see [here](#pm2))
- supports single-IP/rotating proxy config out of the box (see [here](#proxy-middleware))

## Installation

To install this project, you need to:

1. Clone the repository.
2. Go to src/python/src folder
3. Use "poetry install"
4. Then use "poetry shell" to enable virtual environment
5. Create and populate a file .env in the project root
6. Perfect. Project installed.

## Usage

To use the project, we recommend:
1. Go to the project root.
2. Go to the PM2 folder "cd pm2"
3. "pm2 start pm2.config.js"
4. To stop all process - use "pm2 stop all"
5. To export all results - use "scrapy business_exporter_command" from poetry shell.

## Configuration

In root directory you can find file ".env.example". You must create a ".env" file which based on example.
Fill all rows and only then you can start the project.
This file contain all settings for:
- Databases
- Logging
- Middlewares
- RabbitMQ
- And others...

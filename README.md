# Cookiecutter Base Django Template

A Cookiecutter template for quickly creating Django projects with best practices and
minimal setup. This template is designed to help you kickstart a Django project with
a clean and organized structure.

## Features

- **Django and Python version**: Pre-configured with Django 4.2 and Python 3.12.
- **Structured Project Layout**: Organized directory structure for easy maintenance and scalability.
- **Docker Support**: Includes `Dockerfile` and `docker-compose` for easy development and deployment.
- **Custom Base Model with Soft Deleting**: This project includes a custom base model that implements soft deleting functionality. Rather than permanently deleting records from the database, soft deleting marks them as deleted without removing them, allowing for easier data recovery or auditing.
  - A `deleted_at` field is added to models to indicate if a record is soft deleted.
  - Soft-deleted records excluded from queries by default, but you can explicitly include them for recovery purposes.
- **Custom User Model**: Includes a custom user model implementation for flexibility.
- **Swagger API Documentation**: The project includes Swagger integration for easy-to-navigate, interactive API documentation. Developers can view and interact with the API endpoints directly through the Swagger UI.
- **Environment Configuration**: Ready-to-use `.env` file setup for environment-specific settings.
- **Deployment Mode**: Designed to support deployment modes, including **development (local)** and **production**. Each mode has its own set of configurations, including settings, requirements, Dockerfiles, and Docker Compose files. This setup allows for easy switching between different environments.


## Usage

Let's pretend you want to create a Django project called "MyProject". Rather than using `django-admin startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten
until the worst possible moment, get cookiecutter to do all the work.

First, get Cookiecutter.

```
pip install cookiecutter
```

Now run it against this repo:

```
cookiecutter https://git.irdpk.ir/open_data/django_base.git
```

You'll be prompted for some values. Provide them, then a Django project will be created for you.

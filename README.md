# Book Management

Book management system using Django and MongoDB

The backend code is located inside the **backend** folder.


## Table of Contents

> * Requirements:
>   * [Libraries](#libraries)
>   * [Technical Requirements](#technical-requirements-to-run-the-backend)
> * Model
>   * [Diagram](#model)
> * Configuration
>   * [Project](#configuration)
>   * [Commands](#configuration)
> * Testing
>   * [Pytest](#testing)


### Libraries

* [Docker: ](https://docs.docker.com/install "View documentation") Install Docker for different operating systems.
* [Docker Compose: ](https://docs.docker.com/compose/install/ "View documentation") Install Docker Compose for macOS, Windows, and Linux.
* [Python 3.10: ](https://www.python.org/ "View documentation") Programming language.
* [Django: ](https://www.djangoproject.com/ "View documentation") Django requirement packages are listed in the requirements.txt file.
* [Pytest: ](https://docs.pytest.org// "View documentation") A Python framework that simplifies writing and executing unit and integration tests
* [MongoDB: ](https://www.postgresql.org/ "View documentation") User credentials are stored in the environment variable file named .env.


### Technical Requirements to Run the Backend
- Docker must be installed on the machine where the project will be executed.
- Configure the environment variables.

### Model

![model](docs/img/arq.png?raw=true "Arquitectura")

### Configuration

- [Project](docs/config.md)
- [Commands](docs/commands.md)

### Testing

- [Pytest](docs/pytest.md)
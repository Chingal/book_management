**Project Configuration**
---------------------
In the root of the project, there is a file called **env.template**
This file contains our environment variables with default values, and you can change them to any values you prefer


#### Contents of env.template
```bash
#======================== Django ========================
DJANGO_SETTINGS_MODULE=backend.settings.dev
PROJECT_NAME=backend
ENVIRONMENT=development
SECRET_KEY=XXXXXXXX123123123
PREFIX_URL=
USERNAME_TEST=
PASSWORD_TEST=

#======================== MongoDB =======================
MONGO_INITDB_DATABASE=
MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
MONGO_URI=
MONGO_DB_PORT=

#======================== CELERY ========================
REDIS_HOST=
CELERY_BROKER_URL=
```

To make the backend work, you must create a copy of the file using the following command:

`cp env.template .env`

Once the file is copied, you can proceed with building the Docker image and then starting it. To do so, you can use the following command:

`docker-compose up -d --build`

![Docker Build](./img/docker-build.png?raw=true "Docker build")

After running that command, you will see something similar to this:

![Docker Up](./img/docker-up.png?raw=true "Docker Up")


If everything goes well, we can visit [http://0.0.0.0:3016/](http://0.0.0.0:3016/ "http://0.0.0.0:3016/") where our app is hosted, and we will be able to see the API documentation.

If we want to stop our image, we can do so with the following command:

`docker-compose stop`

If we want to bring our application back up again, we can use the following command:

`docker-compose up -d`

If we want to restart all the containers, we can use the following command:

`docker-compose restart`

If we want to restart a specific container, we can use the following command:

`docker-compose restart <<container_name>>`
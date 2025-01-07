**Commands**
---------------------
The following are the commands that can be used:

Migrate to MongoDB

```bash
$ docker-compose exec app python manage.py migrate_mongo
```

![Migrations](../img/migrate_mongo.png?raw=true "Migrations")


Populate Users

```bash
$ docker-compose exec app python manage.py populate_users
```

![Populate-users](../img/populate_users.png?raw=true "Populate-users")
![List-users](../img/list-users.png?raw=true "List-users")



Populate Books

```bash
$ docker-compose exec app python manage.py populate_books
```

![Populate-books](../img/populate_books.png?raw=true "Populate-books")
![List-books](../img/list-books.png?raw=true "List-books")
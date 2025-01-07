**Pytest**
---------------------
Tests can be run as follows:

Todos los test en la app:
```bash
$ docker-compose exec app python -m pytest -s
```
![Pytest](./img/pytest.png?raw=true "Pytest")


Con Coverage:
```bash
$ docker-compose exec app python -m pytest --cov="."
```
![Coverage](./img/coverage.png?raw=true "Pytest")
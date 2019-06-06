# aiohttp-auth

Asyncio Python utilizing the following libraries:
* aiohttp: async web framework
* aiopg: async Postgres driver with SQLAlchemy support
* attrs: easy creation and validation of usecase-layer objects
* alembic: database migration and schema management with SQLAlchemy support
 
Local DB Migrations:

```
$ alembic upgrade head
$ alembic -x db=aiohttp_auth_test upgrade head
```
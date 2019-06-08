# aiohttp-auth

Asyncio Python utilizing the following libraries:
* aiohttp: async web framework
* aiohttp-session: cookie and session management for aiohttp
* aiopg: async Postgres driver with SQLAlchemy support
* attrs: easy creation and validation of usecase-layer objects
* alembic: database migration and schema management with SQLAlchemy support
 
Local DB Migrations:

```
# Run migrations on main database, configured in alembic/env.py
$ alembic upgrade head
# Run migrations on test db
$ alembic -x db=aiohttp_auth_test upgrade head
```
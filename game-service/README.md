# The game-service
## Why ?
The game service is designed as the core of our project, everything goes through it, it listens MQTT messages, treats them, and stores results in PostgreSQL
The game service makes sure no false data is posted, stores the game state reads MQTT data and translates it, and owns the business logic of our program and serves as a validator for any user related input.

## Notes concerning development
### Virtual environment
To avoid the installation of unnecessary requirements on the host machine, a venv file is used, thus making changes only local
To add a module
```
$> source bin/activate
$> pip install [some_module]
$> pip freeze > requirements.txt
$> deactivate
```
Running the app from this point will make it so the new module gets installed

### Alembic
This project runs using Alembic for database migrations
Alembic is like git for databases
To generate the file 
> alembic revision --autogenerate -m "init"
To publish the file to the database
> alembic upgrade head
[This documentation is incomplete]
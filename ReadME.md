# Fin-Banker  REST API Service



## Usage

first thing is to set up your virtual environment. 

By way of illustration I will provide snippets to help you setup.

Ps. All commands below are terminal commands.



creating a virtualenv via venv
```
python3 -m venv {name of your env}
```

To activate your venv

```
source {name of your venv}/bin/activate
```



Please create a dotenv file for your environment variables. An example environment variable is provided. This file is called ```.example.env```.

Installing Requirements can be done by using this command.


```
pip install -r requirements.txt

```

Migrating DB with Alembic

```
alembic upgrade heads
```

Starting your Server

```
uvicorn src.app.main:app --reload

```

## PostMan Collection.

I create a postman collection that can be forked for testing. here -> https://documenter.getpostman.com/view/17138168/2s93RUuBx8




### Docker Support added.
what does this means? 

we can skip creating Virtualenvs and work directly with docker.



The start up code is 
```
docker-compose up


```


tear down

```
docker-compose down

```


to carry out db migrations we use

```

docker-compose exec web alembic upgrade heads

```
# TODOS
Infos:
* author: Eloi Démolis
* API port: 5123
* Vue port: 8080

## Features
All features required (Back, Front, JWT, Swagger and Unitests). However Unitests were only implemented to test the API. Logging was not implemented, but the Back is built to support it (see `formated_response` in `app/services/status.py`).

## Commands
To launch:
```sh
docker-compose run -d --build
```

To test the API (you should read uniTests.py before), first set `MOCK_BDD` to `True` in `app/config.py`, then:
```sh
python -m pip install -r requirements.txt
python api.py &
pytest uniTests.py
```

# TODOS
author: Eloi Démolis
API port: 5123
Vue port: 8080

## Commands
To launch:
```sh
docker-compose run -d --build
```

To test the API (you should read uniTests.py before):
```sh
python -m pip install -r requirements.txt
python api.py &
pytest uniTests.py
```

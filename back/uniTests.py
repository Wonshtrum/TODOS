import requests
from api import config
from app.services.status import STATUS


# IMPORTANT!
# TO USE:
# - set MOCK_BDD to True in app/config.py
# - start the API
# - launch pytest uniTests.py
# - restart the Flask server EACH TIME (to reset the MOCK BDD)


def has_status(response, status):
	"""
	SUCCESS      
	NOT_LOGIN    
	MISSING_PARAM
	BAD_REQUEST  
	USERNAME_USED
	BAD_LOGIN    
	BAD_LIST_ID  
	BAD_TODO_ID  
	"""
	assert response['status'] == status.code
def is_similar(json, **kwargs):
	assert all(json.get(key) == value if value is not any else key in json for key, value in kwargs.items())
def has_members(json, *args):
	assert all(key in json for key in args)

def std_request(method, endpoint, *args, **kwargs):
	kwargs['headers'] = HEADERS
	return requests.__getattribute__(method)(URL+endpoint, *args, **kwargs).json()
def sec_request(method, endpoint, *args, **kwargs):
	res = requests.__getattribute__(method)(URL+endpoint, *args, **kwargs).json()
	has_status(res, STATUS.NOT_LOGIN)
	kwargs['headers'] = HEADERS
	res = requests.__getattribute__(method)(URL+endpoint, *args, **kwargs).json()
	has_status(res, STATUS.SUCCESS)
	return res


URL = f'http://127.0.0.1:{config.PORT}/api/'
USER = {'user':'admin', 'pwd':'admin'}
HEADERS = {'jwt':None}


# -----------------------------------------------------------------------------------
# /api/login
# /api/account
def test_fail_login():
	res = requests.post(URL+'login', data=USER).json()
	has_status(res, STATUS.BAD_LOGIN)

def test_account():
	res = requests.post(URL+'account', data=USER).json()
	has_status(res, STATUS.SUCCESS)

def test_login():
	res = requests.post(URL+'login', data=USER).json()
	has_status(res, STATUS.SUCCESS)
	has_members(res['data'], 'token')
	HEADERS['jwt'] = res['data']['token']

def test_fail_account():
	res = requests.post(URL+'account', data=USER).json()
	has_status(res, STATUS.USERNAME_USED)


# -----------------------------------------------------------------------------------
# /api/lists
def test_put_list():
	payload = {
		'name': 'test'
	}
	sec_request('put', 'lists', data=payload)
	res = std_request('put', 'lists', data=payload)
	has_status(res, STATUS.SUCCESS)
	has_members(res['data'], 'id_list')

def test_get_lists():
	res = sec_request('get', 'lists')
	data = res['data']
	assert len(data) == 2
	is_similar(data[0], name='test', owner='admin', todos=[], id_list=any)
	is_similar(data[1], name='test', owner='admin', todos=[], id_list=any)


# -----------------------------------------------------------------------------------
# /api/lists/:id_list
def test_patch_list():
	payload = {
		'name': 'test2'
	}
	sec_request('patch', 'lists/1', data=payload)
def test_fail_patch_list():
	res = std_request('get', 'lists/10')
	has_status(res, STATUS.BAD_LIST_ID)

def test_delete_list():
	sec_request('delete', 'lists/0')
def test_fail_delete_list():
	res = std_request('delete', 'lists/0')
	has_status(res, STATUS.BAD_LIST_ID)

def test_get_list():
	res = sec_request('get', 'lists/1')
	data = res['data']
	is_similar(data, id_list=1, name='test2', owner='admin', todos=[])
def test_fail_get_list():
	res = std_request('get', 'lists/0')
	has_status(res, STATUS.BAD_LIST_ID)


# -----------------------------------------------------------------------------------
# /api/lists/todos/:id_list
def test_put_todo():
	payload = {
		'name': 'todo',
		'task': 'task'
	}
	sec_request('put', 'lists/todos/1', data=payload)
	res = std_request('put', 'lists/todos/1', data=payload)
	has_status(res, STATUS.SUCCESS)
	has_members(res['data'], 'id_todo')
def test_fail_put_todo():
	payload = {
		'name': 'todo',
		'task': 'task'
	}
	res = std_request('put', 'lists/todos/0')
	has_status(res, STATUS.BAD_LIST_ID)

def test_get_todos():
	res = sec_request('get', 'lists/todos/1')
	data = res['data']
	assert len(data) == 2
	is_similar(data[0], name='todo', task='task', date=any, id_todo=any)
	is_similar(data[1], name='todo', task='task', date=any, id_todo=any)
def test_fail_get_todos():
	res = std_request('get', 'lists/todos/0')
	has_status(res, STATUS.BAD_LIST_ID)


# -----------------------------------------------------------------------------------
# /api/lists/:id_list/:id_todo
def test_patch_todo():
	payload = {
		'name': 'todo2',
		'task': 'task2'
	}
	res = sec_request('patch', 'lists/todos/1/1', data=payload)
def test_fail_patch_todo():
	payload = {
		'name': 'todo2',
		'task': 'task2'
	}
	res = std_request('patch', 'lists/todos/10/1', data=payload)
	has_status(res, STATUS.BAD_LIST_ID)
	res = std_request('patch', 'lists/todos/1/2', data=payload)
	has_status(res, STATUS.BAD_TODO_ID)

def test_delete_todo():
	sec_request('delete', 'lists/todos/1/0')
def test_fail_delete_todo():
	res = std_request('delete', 'lists/todos/0/0')
	has_status(res, STATUS.BAD_LIST_ID)
	res = std_request('delete', 'lists/todos/1/0')
	has_status(res, STATUS.BAD_TODO_ID)

def test_get_todo():
	res = sec_request('get', 'lists/todos/1/1')
	data = res['data']
	is_similar(data, id_todo=1, name='todo2', task='task2', date=any)
def test_fail_get_todo():
	res = std_request('get', 'lists/todos/0/0')
	has_status(res, STATUS.BAD_LIST_ID)
	res = std_request('get', 'lists/todos/1/0')
	has_status(res, STATUS.BAD_TODO_ID)

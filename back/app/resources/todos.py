from datetime import datetime
from flask_restful import Resource, reqparse, abort
from app.services.bdd import ListWrapper
from app.services.todos import Todos, Todo
from app.services.status import STATUS, endpoint
from app.services.swagger import Swagger


class ListsResource(Resource):
	@endpoint()
	@Swagger.doc(
	Swagger('Return all the TODO lists of the user', ['TODO API'])\
	.response(STATUS.SUCCESS, 'JSON representing all the TODO lists of the user')\
	.response(STATUS.NOT_LOGIN))
	def get(self, user=None):
		return STATUS.SUCCESS, Todos.find_all(owner=user['user'])

	@endpoint()
	@Swagger.doc(
	Swagger('Create a new TODO list', ['TODO API'])\
	.body('The name of the TODO list')\
	.in_body('name', 'string', True)\
	.response(STATUS.SUCCESS, 'The id of the newly created TODO list')\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.NOT_LOGIN))
	def put(self, user=None):
		body_parser = reqparse.RequestParser()
		body_parser.add_argument('name', type=str, required=True, help='Missing name of the todo list')
		args = body_parser.parse_args(strict=True)
		name = args['name']

		id_list = Todos.new_index('id_list')
		Todos.create(id_list, name, user['user'])
		return STATUS.SUCCESS, { 'id_list':id_list }


class ListsByIdResource(Resource):
	@endpoint()
	@Swagger.doc(Swagger('Return a TODO list from its id', ['TODO API'])\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.response(STATUS.SUCCESS, 'JSON representing the TODO list')\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def get(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			return STATUS.SUCCESS, todo_list
		return STATUS.BAD_LIST_ID
	
	@endpoint()
	@Swagger.doc(Swagger('Change the name of a TODO list', ['TODO API'])\
	.body('The new name')\
	.in_body('name', 'string', True)\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.response(STATUS.SUCCESS)\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def patch(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			body_parser = reqparse.RequestParser()
			body_parser.add_argument('name', type=str, required=True, help='Missing name of the todo list')
			args = body_parser.parse_args(strict=True)
			name = args['name']

			todo_list['name'] = name
			Todos.save()
			return STATUS.SUCCESS
		return STATUS.BAD_LIST_ID
	
	@endpoint()
	@Swagger.doc(Swagger('Delete a TODO list', ['TODO API'])\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.response(STATUS.SUCCESS)\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def delete(sef, id_list, user=None):
		if Todos.delete_one(id_list=id_list, owner=user['user']):
			return STATUS.SUCCESS
		return STATUS.BAD_LIST_ID


class TodosResource(Resource):
	@endpoint()
	@Swagger.doc(Swagger('Return the TODOS of a list from its id', ['TODO API'])\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.response(STATUS.SUCCESS, 'JSON list representing the TODOS')\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def get(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			return STATUS.SUCCESS, todo_list['todos']
		return STATUS.BAD_LIST_ID

	@endpoint()
	@Swagger.doc(Swagger('Create a new TODO in a TODO list', ['TODO API'])\
	.body('The name and content of the TODO')\
	.in_body('name', 'string', True)\
	.in_body('task', 'string', True)\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.response(STATUS.SUCCESS, 'The id of the newly created TODO')\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def put(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			todo_list = ListWrapper(todo_list['todos'], Todo)
			id_todo = todo_list.new_index('id_todo')

			body_parser = reqparse.RequestParser()
			body_parser.add_argument('name', type=str, required=True, help='Missing name of the todo')
			body_parser.add_argument('task', type=str, required=True, help='Missing task of the todo')
			args = body_parser.parse_args(strict=True)
			name = args['name']
			task = args['task']

			todo_list.create(id_todo, name, task)
			Todos.save()
			return STATUS.SUCCESS, { 'id_todo':id_todo }
		return STATUS.BAD_LIST_ID


def on_todo(f):
	def wrapper(self, id_list, id_todo, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			todo_list = ListWrapper(todo_list['todos'], Todo)
			result = f(todo_list, id_todo)
			if result is not None:
				return result
			return STATUS.BAD_TODO_ID
		return STATUS.BAD_LIST_ID
	return wrapper

class TodosByIdResource(Resource):
	@endpoint()
	@Swagger.doc(Swagger('Return a TODO from its id and list id', ['TODO API'])\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.in_path('id_todo', 'string', True, 'The TODO id')\
	.response(STATUS.SUCCESS, 'JSON representing the TODO')\
	.response(STATUS.MISSING_PARAM)\
	.response(404, 'Invalid list id or TODO id')\
	.response(STATUS.NOT_LOGIN))
	@on_todo
	def get(todo_list, id_todo):
		todo = todo_list.find_one(id_todo=id_todo)
		if todo:
			return STATUS.SUCCESS, todo

	@endpoint()
	@Swagger.doc(Swagger('Change a TODO', ['TODO API'])\
	.body('The new name and content of the TODO')\
	.in_body('name', 'string', False)\
	.in_body('task', 'string', False)\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.in_path('id_todo', 'string', True, 'The TODO id')\
	.response(STATUS.SUCCESS)\
	.response(STATUS.MISSING_PARAM)\
	.response(404, 'Invalid list id or TODO id')\
	.response(STATUS.NOT_LOGIN))
	@on_todo
	def patch(todo_list, id_todo):
		todo = todo_list.find_one(id_todo=id_todo)
		if todo:
			body_parser = reqparse.RequestParser()
			body_parser.add_argument('name', type=str, required=False, help='Missing name of the todo')
			body_parser.add_argument('task', type=str, required=False, help='Missing task of the todo')
			args = body_parser.parse_args(strict=False)
			name = args['name']
			task = args['task']

			if name is not None: todo['name'] = name
			if task is not None: todo['task'] = task
			todo['date'] = str(datetime.now())
			Todos.save()
			return STATUS.SUCCESS

	@endpoint()
	@Swagger.doc(Swagger('Delete a TODO', ['TODO API'])\
	.in_path('id_list', 'string', True, 'The TODO list id')\
	.in_path('id_todo', 'string', True, 'The TODO id')\
	.response(STATUS.SUCCESS)\
	.response(404, 'Invalid list id or TODO id')\
	.response(STATUS.NOT_LOGIN))
	@on_todo
	def delete(todo_list, id_todo):
		if todo_list.delete_one(id_todo=id_todo):
			Todos.save()
			return STATUS.SUCCESS

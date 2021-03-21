from flask_restful import Resource, reqparse, abort
from app.services.users import Users
from app.services.status import STATUS, endpoint
from app.services.swagger import Swagger


class AccountResource(Resource):
	@endpoint(restricted=False)
	@Swagger.doc(Swagger('Create a new user', ['User API'], jwt=False)\
	.body('The name and password of the user')\
	.in_body('user', 'string', True)\
	.in_body('pwd', 'string', True)\
	.response(STATUS.SUCCESS)\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.USERNAME_USED))
	def post(self):
		body_parser = reqparse.RequestParser()
		body_parser.add_argument('user', type=str, required=True, help='Missing the login of the user')
		body_parser.add_argument('pwd',  type=str, required=True, help='Missing the password associated to the user login')
		args = body_parser.parse_args(strict=True)
		user = args['user']
		pwd  = args['pwd']
		return create(user, pwd)

def create(user, pwd):
	u = Users.find_one(user=user)
	if u:
		return STATUS.USERNAME_USED
	Users.create(user, pwd)
	return STATUS.SUCCESS

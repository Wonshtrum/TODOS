from flask_restful import Resource, reqparse, abort
from app.services.users import Users, User
from app.services.status import STATUS, endpoint
from app.services.debug import DEBUG
from app.services.swagger import Swagger


class LoginResource(Resource):
	@endpoint(restricted=False)
	@Swagger.doc(Swagger('Login as a user', ['User API'], jwt=False)\
	.body('The name and password of the user')\
	.in_body('user', 'string', True)\
	.in_body('pwd', 'string', True)\
	.response(STATUS.SUCCESS, 'The token of the user')\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.BAD_LOGIN))
	def post(self):
		body_parser = reqparse.RequestParser()
		body_parser.add_argument('user', type=str, required=True, help='Missing the login of the user')
		body_parser.add_argument('pwd',  type=str, required=True, help='Missing the password associated to the user login')
		args = body_parser.parse_args(strict=True)
		user = args['user']
		pwd  = args['pwd']
		return login(user, pwd)


def login(user, pwd):
	u = Users.find_one(user=user, pwd=User.hash(pwd))
	if u:
		u = Users.decode(u)
		return STATUS.SUCCESS, { 'token':u.get_token() }
	else:
		return STATUS.BAD_LOGIN

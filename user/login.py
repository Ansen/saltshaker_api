# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from common.log import loggers
from common.sso import create_token, verify_password
import configparser
import os


logger = loggers()

config = configparser.ConfigParser()
conf_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
config.read(conf_path + "/saltshaker.conf")
expires_in = int(config.get("Token", "EXPIRES_IN"))

parser = reqparse.RequestParser()
parser.add_argument("username", type=str, required=True, trim=True)
parser.add_argument("password", type=str, required=True, trim=True)


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        if verify_password(args["username"], args["password"]):
            cookie_key, token = create_token(args["username"])
            logger.info("%s login success: " % args["username"])
            return {"status": True, "message": "", "data": {cookie_key: [token.decode("utf-8"), expires_in]}}
        else:
            logger.info("%s login failure: " % args["username"])
            return {"status": False, "message": "用户名或者密码错误"}

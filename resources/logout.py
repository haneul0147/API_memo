from flask_jwt_extended import get_jwt

from flask import request
from flask.json import jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource
from http import HTTPStatus

from mysql_connection import get_connection
from mysql.connector.errors import Error

from email_validator import validate_email, EmailNotValidError

from utils import hash_password, check_password

from flask_jwt_extended import create_access_token

# 로그아웃된 토큰은, 여기에 저장해 준다.
# 그러면, jwt가 알아서 토큰이 이 셋에 있는지 확인해서,
# 로그아웃 한 유저인지 판단한다.

jwt_blacklist = set()

# 로그아웃 클래스 
class UserLogoutResource(Resource) :
    @jwt_required()
    def post(self) :
        jti = get_jwt()['jti']
        print(jti)
        # 로그아웃된 토큰의 아이디값을, 블랙리스트에 저장한다.
        # jwt_blacklist.add(jti)

        # DB에 인서트하는 코드

        try :
            # 1. DB 에 연결
            connection = get_connection()
           
            # 2. 쿼리문 만들고
            query = '''insert into token
                        (jti)
                        values
                        (%s);'''
            # 파이썬에서, 튜플만들때, 데이터가 1개인 경우에는 콤마를 꼭
            # 써준다.
            record = (jti , )
            
            # 3. 커넥션으로부터 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서에 넣어서 실행한다.
            cursor.execute(query, record)

            # 5. 커넥션을 커밋한다.=> 디비에 영구적으로 반영하라는 뜻.
            connection.commit()

        except Error as e:
            print('Error ', e)
            # 6. username이나 email이 이미 DB에 있으면,
            #    이미 존재하는 회원이라고 클라이언트에 응답한다.
            return {'error' : 100} , HTTPStatus.BAD_REQUEST
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection is closed')



        return { 'error' : 0, 'result':'로그아웃 되었습니다.'}












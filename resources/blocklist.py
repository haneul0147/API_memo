from mysql_connection import get_connection
from mysql.connector.errors import Error

def check_blocklist(jti) :

    #  디비에서 토큰 테이블에서 확인한다.
    try :
        connection = get_connection()

        query = '''select * 
                    from token
                    where jti = %s; '''
        
        param = (jti, )
        
        cursor = connection.cursor(dictionary = True)

        cursor.execute(query, param)

        # select 문은 아래 내용이 필요하다.
        record_list = cursor.fetchall()
        print(record_list)

        ### 중요. 파이썬의 시간은, JSON으로 보내기 위해서
        ### 문자열로 바꿔준다.
        i = 0
        for record in record_list:
            record_list[i]['created_at'] = record['created_at'].isoformat()                
            i = i + 1
            
        # 위의 코드를 실행하다가, 문제가 생기면, except를 실행하라는 뜻.
    except Error as e :
        print('Error while connecting to MySQL', e)
        return {'error' : str(e)} , 400
    # finally 는 try에서 에러가 나든 안나든, 무조건 실행하라는 뜻.
    finally :
        print('finally')
        cursor.close()
        if connection.is_connected():
            connection.close()
            print('MySQL connection is closed')
        else :
            print('connection does not exist')

    if len(record_list) == 0 :
        return False
    else :
        return True


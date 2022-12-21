import pandas
import app.config as config
# import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, insert
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text, case
from sqlalchemy.pool import NullPool
from app.logger import logger

url = 'postgresql://{}:{}@{}:{}/{}'.format(config.db['user'], config.db['password'], config.db['host'], config.db['port'], config.db['database'])
engine = create_engine(url, client_encoding='utf-8')
Session = scoped_session(sessionmaker(bind=engine))
metadata = MetaData(bind=engine)



class Query_exc():
    def __init__(self):
        self.session = Session()

    def __del__(self):
        self.session.close()
        engine.dispose()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def reconnection(self):
        try:
            if self.session:
                self.session.close()
                engine.dispose()
        except Exception as e:
            print(e)
            logger.error(f'reconnection error: {e}')
        finally:
            self.session = Session()

    def execute(self, sql):
        try:
            res = self.session.execute(sql)
            self.commit()
        except Exception as e:
            print(e)
            logger.error(f'execute error: {e}')
            self.rollback()
            res = None
        finally:
            return res

    def select_all(self, sql):
        try:
            res = self.session.execute(sql).all()
        except Exception as e:
            print(e)
            logger.error(f'select_all error: {e}')
            self.rollback()
            res = None
        finally:
            return res

    def select_first(self, sql):
        try:
            res = self.session.execute(sql).first()
        except Exception as e:
            print(e)
            logger.error(f'select_first error: {e}')
            self.rollback()
            res = None
        finally:
            return res

class DAO(Query_exc):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def getAllEmployee(self, keyword):
        sql = f"SELECT (row_number() over()) AS num, * FROM employee WHERE discard = 0 AND TYPE != 1 AND (name LIKE '%{keyword}%' OR user_id LIKE '%{keyword}%' OR email LIKE '%{keyword}%' OR position LIKE '%{keyword}%') ORDER BY num DESC"
        result = super().select_all(sql)
        return result

    def getEmployee(self, id):
        sql = f"SELECT * FROM employee WHERE discard = 0 and user_id = '{id}' limit 1"
        result = super().select_first(sql)
        return result

    def updateEmployeePoint(self, id, point):
        sql = f"UPDATE employee SET point=point - {point} WHERE user_id='{id}'"
        res = super().execute(sql)
        return res
    
    def updateEmployee(self, name, id, email, position):
        sql = f"UPDATE employee SET name='{name}', email='{email}', position='{position}' WHERE user_id='{id}';"
        res = super().execute(sql)
        return res

    def insertLog(self, id, text, type):
        str(text).replace('\'','')
        sql = f"INSERT INTO log(user_id, text, error_type) values('{id}','{text}','{type}')"
        res = super().execute(sql)
        return res

    def insertEmployee(self, name, id, password, email, position, type=2, point=30000):
        sql = f"INSERT INTO employee(name, user_id, user_password, email, position, type, point) VALUES('{name}', '{id}', '{password}', '{email}', '{position}', {type}, {point});"
        res = super().execute(sql)
        return res

    def getPointLog(self, start, end, page, range, keyword=''):
        page = page - 1
        sql = f"SELECT (row_number() over()) AS num, plno, to_char(crtime, 'YYYY-MM-DD HH24:MI:SS') AS crtime, user_id, point, memo \
        FROM pay_log WHERE crtime BETWEEN TO_TIMESTAMP('{start}','YYYYMMDD') AND TO_TIMESTAMP('{end}','YYYYMMDD') + INTERVAL '1 day' \
        AND (user_id LIKE '%{keyword}%' OR memo LIKE '%{keyword}%')\
        ORDER BY crtime DESC LIMIT {range} OFFSET {page * range};"
        res = super().execute(sql)
        return res

    def insertPointLog(self, id, point, memo=''):
        sql = f"INSERT INTO pay_log(user_id, point, memo) VALUES('{id}', {point}, '{memo}');"
        res = super().execute(sql)
        return res

    def pointReset(self):
        sql = f"UPDATE employee SET point = 30000 WHERE discard=0"
        res = super().execute(sql)
        return res

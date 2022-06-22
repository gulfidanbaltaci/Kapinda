from flask_mysqldb import MySQL
import yaml
import sys

class PySql:

    def __init__(self, flask_app, path_to_yaml):

        db_details = yaml.load(open(path_to_yaml), Loader = yaml.FullLoader)

        flask_app.config['MYSQL_HOST'] = db_details['mysql_host']
        flask_app.config['MYSQL_USER'] = db_details['mysql_user']
        flask_app.config['MYSQL_PASSWORD'] = db_details['mysql_password']
        flask_app.config['MYSQL_DB'] = db_details['mysql_db']

        self.mysql = MySQL(flask_app)

        self.mysql_cursor = None

        self.__last_result = None

    def init(self):
        self.mysql_cursor = self.mysql.connection.cursor()


    def deinit(self):
        self.mysql_cursor.close()

    def run(self, sql_stmt, params = None):
        self.mysql_cursor.execute(sql_stmt, params)

    def run_many(self, sql_stmt, params):
        self.mysql_cursor.executemany(sql_stmt, params)

    def __result(self):
        try:
            self.__last_result = self.mysql_cursor.fetchall()
            return self.__last_result
        except InterfaceError:
            return self.__last_result

    @property
    def result(self):
        return self.__result()

    @property
    def scalar_result(self):
        try:
            return self.__result()[0][0]
        except IndexError:
            return None


    def commit(self):
         self.mysql.connection.commit()

    def rollback(self):
        self.mysql.connection.rollback()


    def run_transaction(self, function, *args, commit = True):
        try:
            
            self.init()

            result = function(self, *args)
        except:
            self.rollback()

            return None
        else:
            if commit:
                self.commit()

            return result
        finally:
            self.deinit()

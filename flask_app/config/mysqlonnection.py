from typing import final
import pymysql.cursors

class mySQLConnection:
    def __init__(self, db) -> None:
        connection = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "root",
            db = db,
            charset = "utf8mb4",
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
        self.connection = connection
    def query_db(self, query:str, data :dict = None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print(f"Running Query: {query}")
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went Wrong: ", e)
            finally:
                self.connection.close()


def connectToMySQL(db) -> mySQLConnection:
    return mySQLConnection(db)
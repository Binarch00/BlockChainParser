import mysql.connector
from settings import logger, DATABASE


class DataBase:

    def __init__(self, table_name="addresses"):
        self.table_name = table_name
        self.conn = mysql.connector.connect(
            user=DATABASE["user"], password=DATABASE["password"],
            host=DATABASE["host"], database=DATABASE["database"])

    def __del__(self):
        self.conn.close()

    def add_unique(self, info):
        try:
            cursor = self.conn.cursor()
            add_output = ("INSERT IGNORE INTO {} "
                          "(info) "
                          "VALUES (%s)".format(self.table_name))
            data = (info, )
            cursor.execute(add_output, data)
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logger.exception(ex)

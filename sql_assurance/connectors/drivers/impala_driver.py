from impala.dbapi import connect


class ImpalaConnector(object):
    def __init__(self, **kwargs):
        for key in ['host', 'port', 'database']:
            if key not in kwargs:
                raise Exception("Missing required parameters {}".format(key))

        self.__host = kwargs.get("host")
        self.__port = kwargs.get("port")
        self.__database = None

        if kwargs.get("database"):
            self.__database = kwargs.get("database")
        self.__connection = self._establish_connection()

    def query(self, sql_statement):
        self.__connection.execute(sql_statement)

        return self.__connection.fetchall()

    def _establish_connection(self):
        self.__connection = connect(
            self.__host, self.__port, self.__database
        )

        return self.__connection.cursor()

from sqlalchemy import create_engine

class MySqlConnection:

    def __init__(self, *args, **kwargs):
        self._user_name = args[0]
        self._password = args[1]
        self._database_name = args[2]

    def connect_to_database(self):
        _connection_string = 'mysql://{}:{}@localhost/{}'.format(self._user_name,self._password,self._database_name)
        _engine = create_engine(_connection_string)
        self._connection = _engine.connect()


    def use_table_and_column(self,table_name,column_name):
        self._table_name = table_name
        self._column_name = column_name


    def get_contacts_from_database(self):
        _query_string = 'select {} from {}'.format(self._column_name,self._table_name)
        _result = self._connection.execute(_query_string)
        _result_list = [row[self._column_name] for row in _result]
        return _result_list


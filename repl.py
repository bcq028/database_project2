from engine.database import Database
from os import listdir,environ
from os.path import join
from engine.index import IndexType
class REPL():
    def __init__(self):
        self.current_database:Database = None
        self.databases:dict[str,Database] = {}
        for db in listdir(environ.get('root_dir')):
            self.databases[db]=Database(join(environ.get('root_dir'),db))
        self.prompt = "db > "
        self.commands = {
            "CREATE DATABASE": self.create_database,
            "USE": self.use_database,
            "CREATE TABLE": self.create_table,
            "INSERT INTO": self.insert_into,
            "SELECT": self.select,
            "DROP TABLE": self.drop_table,
            "DROP DATABASE": self.drop_database,
            "EXIT": self.exit
        }

    def create_database(self, *args):
        db_name = args[0]
        if db_name in self.databases:
            print(f"Database {db_name} already exists.")
            return
        self.databases[db_name] = Database(db_name)
        print(f"Database {db_name} created.")

    def use_database(self, *args):
        db_name = args[0]
        if db_name not in self.databases:
            print(f"Database {db_name} does not exist.")
            return
        self.current_database = self.databases[db_name]
        print(f"Using database {db_name}.")

    def create_table(self, *args):
        if not self.current_database:
            print("No database selected.")
            return
        table_name = args[0]
        columns = args[1]
        self.current_database.create_table(table_name, columns)
        print(f"Table {table_name} created.")

    def insert_into(self, *args):
        if not self.current_database:
            print("No database selected.")
            return
        table_name = args[0]
        values = args[1]
        self.current_database.tables[table_name].insert(values)
        print("Data inserted.")

    def select(self, table_name):
        if not self.current_database:
            print("No database selected.")
            return
        self.current_database.tables[table_name].select()

    def drop_table(self, *args):
        if not self.current_database:
            print("No database selected.")
            return
        table_name = args[0]
        self.current_database.drop(table_name)
        print(f"Table {table_name} dropped.")

    def drop_database(self, *args):
        db_name = args[0]
        if db_name not in self.databases:
            print(f"Database {db_name} does not exist.")
            return
        del self.databases[db_name]
        print(f"Database {db_name} dropped.")

    def create_index(self, table_name, column, index_type=IndexType.Hash):
        table = self.current_database.tables[table_name]
        table.create_index(column, index_type)
        print(f"Index on column {column} created for table {table_name}")

    def lookup(self, table_name, column, value):
        table = self.database.get_table(table_name)
        rows = table.lookup(column, value)
        for row in rows:
            print(row)
        print(f"{len(rows)} rows found in table {table_name}")

    def drop_index(self, table_name, column):
        table = self.database.get_table(table_name)
        table.drop_index(column)
        print(f"Index on column {column} dropped for table {table_name}")

    def exit(self):
        print("Goodbye!")
        exit()


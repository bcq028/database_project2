from database import Database

class REPL():
    def __init__(self):
        self.current_database = None
        self.databases = {}
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

    def create_database(self, args):
        db_name = args[0]
        if db_name in self.databases:
            print(f"Database {db_name} already exists.")
            return
        self.databases[db_name] = Database(db_name)
        print(f"Database {db_name} created.")

    def use_database(self, args):
        db_name = args[0]
        if db_name not in self.databases:
            print(f"Database {db_name} does not exist.")
            return
        self.current_database = self.databases[db_name]
        print(f"Using database {db_name}.")

    def create_table(self, args):
        if not self.current_database:
            print("No database selected.")
            return
        table_name = args[0]
        columns = args[1:]
        self.current_database.create_table(table_name, columns)
        print(f"Table {table_name} created.")

    def insert_into(self, args):
        if not self.current_database:
            print("No database selected.")
            return
        table_name = args[0]
        values = args[1:]
        self.current_database.tables[table_name].insert(values)
        print("Data inserted.")

    def select(self, args):
        if not self.current_database:
            print("No database selected.")
            return
        table_name = args[3]
        columns, rows = self.current_database.tables[table_name].select()
        print(columns)
        for row in rows:
            print(row)

    def drop_table(self, args):
        if not self.current_database:
            print("No database selected.")
            return
        table_name = args[0]
        self.current_database.drop(table_name)
        print(f"Table {table_name} dropped.")

    def drop_database(self, args):
        db_name = args[0]
        if db_name not in self.databases:
            print(f"Database {db_name} does not exist.")
            return
        del self.databases[db_name]
        print(f"Database {db_name} dropped.")

    def exit(self, args):
        print("Goodbye!")
        exit()


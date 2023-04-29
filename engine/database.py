
from engine.table import Table

from os import remove,mkdir

from os.path import isfile,join,isdir

from engine.utils import file2table,table2file,get_csv_files

class Database():
    def __init__(self,database_dir:str):
        self.database_dir=database_dir
        if not isdir(database_dir):
            mkdir(database_dir)
        self.tables:dict[str,Table]={}
        self.sync()

    def sync(self):
        for table in get_csv_files(self.database_dir):
            self.tables[table]=Table(table,self.database_dir)


    def commit(self):
        for table in self.tables:
            table.commit()

    def create_table(self,name,columns):
        self.tables[name]=Table(name,self.database_dir,columns)

    def drop(self,table):
        if self.tables.pop(table,None) is None:
            raise NameError(f"Table{table} not exist")
        path=table2file(self.database_dir, table)
        remove(path)
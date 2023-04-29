
from table import Table

from os import listdir,remove 

from os.path import isfile,join

from utils import file2table,table2file

class Database():
    def __init__(self,database_dir:str):
        self.database_dir=database_dir
        self.tables={}
        self.sync()
        
    def sync(self):
        for table in self.get_files():
            self.tables[table]=Table(table,self.database_dir)
    def get_files(self):
        for fi in listdir(self.database_dir):
            if(isfile(join(self.database_dir,fi)) and fi.endswith(".csv")):
                yield file2table(fi)


    def commit(self):
        for table in self.tables:
            table.commit()

    def create_table(self,name,columns):
        self.tables[name]=Table(name,self.database_dir,columns)

    def drop(self,table):
        if self.tables.pop(table,None) is None:
            raise NameError(f"Table{table} not exist")
        remove(table2file(self.database_dir, table))
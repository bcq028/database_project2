from engine.utils import * 
from engine.index import Index,IndexType
class Table():
    def __init__(self,table_name:str,database_dir:str,columns=None):
        self.name=table_name
        self.dir=database_dir
        self.rows=[]
        self.index=None
        if columns:
            with open(table2file(database_dir,table_name), "x",encoding='utf-8') as fh:
                self.columns = columns
                t=write_csv_header(columns)
                fh.writelines(t)
                
                
        else:
            with open(table2file(database_dir,table_name),"r",encoding='utf-8') as fh:
                if not columns:
                    self.columns=get_columns(fh.readline(),fh.readline())
                    for row in fh:
                        self.rows.append(row)
                else:
                    self.columns=columns


    def insert(self,row):
        self.rows.append(row)
        self.commit()

    def delete(self,row):
        self.rows.remove(row)
        self.commit()

    def update(self,oldRow,newRow):
        for idx,row in self.rows:
            if row==oldRow:
                self.rows[idx]=newRow
        self.commit()

    def select(self):
        indexed_column = None
        for column in self.columns:
            if column.get('index'):
                indexed_column = column
                break
        if indexed_column:
            value = input(f'Enter the value to lookup in column "{indexed_column.name}": ')
            rows = indexed_column.index.lookup(value)
        else:
            rows = self.rows
        print('--- Results ---')
        for row in rows:
            print(row)  

    def commit(self):
        #TODO aptitude
        contents=write_csv_header(self.columns)
        with open(table2file(self.dir, self.name),"w+",encoding='utf-8') as fh:
            for row in self.rows:
                contents.append(write_csv_row(row))
            fh.writelines(contents)

        #索引相关

    def create_index(self, column, index_type=IndexType.Hash):
        self.index = Index(self, column, index_type)
        self.index.create_index()
        return self.index
    
    def drop_index(self, column):
        self.index.drop_index()

    def lookup(self, column, value):
        return self.index.lookup(value)
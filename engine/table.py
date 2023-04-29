import re
from engine.utils import table2file,type_str_map,parse_csv_line,write_csv_row,write_csv_header,get_columns

class Table():
    def __init__(self,table_name:str,database_dir:str,columns=None):
        self.name=table_name
        self.dir=database_dir
        self.rows=[]
        if columns:
            with open(table2file(database_dir,table_name), "x") as fh:
                self.columns = columns
                t=write_csv_header(columns)
                fh.writelines(t)
                
                
        else:
            with open(table2file(database_dir,table_name),"r") as fh:
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
        return (self.columns,self.rows)    

    def commit(self):
        #TODO aptitude
        contents=write_csv_header(self.columns)
        with open(table2file(self.dir, self.name),"w+") as fh:
            for row in self.rows:
                contents.append(write_csv_row(row))
            fh.writelines(contents)

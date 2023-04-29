import re
from utils import table2file,type_str_map,parse_csv_line,write_csv_row,write_csv_header,get_columns


class Table():
    def __init(self,table_name:str,database_dir:str,columns=None):
        self.name=table_name
        self.dir=database_dir
        self.rows=[]
        if not columns:
            with open(table2file(database_dir,table_name),"r") as fh:
                self.columns=get_columns(fh.readline(),fh.readline())
                for row in fh:
                    self.insert(row)
        else:
            self.columns=columns

    def insert(self,row):
        self.rows.append(row)

    def delete(self,row):
        self.rows.remove(row)

    def update(self,oldRow,newRow):
        for idx,row in self.rows:
            if row==oldRow:
                self.rows[idx]=newRow
    def select(self):
        return (self.columns,self.rows)    

    def commit(self):
        with open(table2file(self.dir, self.name),"w+") as fh:
            contents=write_csv_header(self.columns)
            for row in self.rows:
                contents.append(write_csv_row(row))
            fh.writelines(contents)

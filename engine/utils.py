from os.path import join, basename 

type_str_map = {
    str: "string",
    int: "int",
    bool: "boolean",
}

def parse_csv_line(line:str)->list[str]:
    return line.strip().split(',')

def table2file(dir:str,name:str)->str:
    return join(dir,name+'.csv')

def file2table(path:str):
    return basename(path).replace('.csv', '')


def write_csv_row(row:list[str]):
    ans=""
    for attr in row:
        if isinstance(attr, str):
            ans+="\""+attr.replace(",", "\\,")+"\""+","
        elif isinstance(attr, bool):
            ans+=str(attr).lower()+","
        elif attr is None:
            ans+=","
    return ans[:-1]+'\n'

def write_csv_header(columns):
    types=""
    names=""
    for col in columns:
        names=f'{names}\"{col["name"]}\"'
        col_type = type_str_map.get(col["type"], "")
        attrs = "".join(["?" if col["nullable"] else "","$" if col["primary key"] else ""])
        types=f'{types}{col_type}{attrs},'
    names=f'{names[:-1]}\n'
    types=f'{types[:-1]}\n'
    return [names,types]

def get_columns(types:str,names:str)->List:
        columns=[]
        attribs=map(lambda c:c.replace("\"",''),parse_csv_line(names))
        for idx,val in enumerate(parse_csv_line(types)):
            if val.startswith("string"):
                col_type=str 
            elif val.startswith("int"):
                col_type=int 
            elif val.startswith("boolean"):
                col_type=bool 
            else:
                col_type=None
            columns.append({
                "name":attribs[idx],
                "type":col_type,
                "nullable": True if val[-1:]=='?' else False,
                "primary key":True if val[-1:]=='$' else False
            })
        return columns
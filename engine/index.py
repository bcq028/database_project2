from engine.utils import * 
from enum import Enum
from bintrees import FastRBTree
import pickle

class IndexType(Enum):
    BTree='BTree'
    Hash='Hash'

class Index:
    def __init__(self, table, column, index_type=IndexType.Hash):
        self.table = table
        self.column = column
        self.index_type:IndexType = index_type
        self.index_file = join(table.dir, f"{table.name}.{column}.{index_type}.idx")
        self.index:BaseIndex = None

    def create_index(self):
        if self.index_type == IndexType.BTree:
            self.index = BTreeIndex()
        elif self.index_type == IndexType.Hash:
            self.index = HashIndex()
        else:
            raise ValueError("Invalid index type")
        column_id=-1
        for i,col in enumerate(self.table.columns):
            if col.get('name')==self.column:
                column_id=i
                break
        for i, row in enumerate(self.table.rows):
            self.index.insert(row[column_id], i)

        self.index.save(self.index_file)

    def drop_index(self):
        self.index.delete()
        self.index = None

    def lookup(self, value):
        if not self.index:
            if self.index_type == 'btree':
                self.index = BTreeIndex.load(self.index_file)
            elif self.index_type == 'hash':
                self.index = HashIndex.load(self.index_file)
            else:
                raise ValueError("Invalid index type")

        return [self.table.rows[i] for i in self.index.lookup(value)]

class BaseIndex:
    def insert(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def lookup(self, key) -> list[int]:
        raise NotImplementedError

    def save(self, file_name):
        raise NotImplementedError

    @staticmethod
    def load(file_path):
        raise NotImplementedError


class HashIndex(BaseIndex):
    def __init__(self):
        self.index = {}

    def insert(self, key, value):
        if key not in self.index:
            self.index[key] = []
        self.index[key].append(value)

    def lookup(self, key):
        if key not in self.index:
            return []
        return self.index[key]

    def delete(self):
        self.index = {}

    def save(self, file_path):
        with open(file_path, 'wb',encoding='utf-8') as f:
            pickle.dump(self.index, f)

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb',encoding='utf-8') as f:
            index = HashIndex()
            index.index = pickle.load(f)
        return index


class BTreeIndex(BaseIndex):
    def __init__(self):
        self.index = FastRBTree()

    def insert(self, key, value):
        self.index[key] = value

    def delete(self, key):
        del self.index[key]

    def lookup(self, key):
        return list(self.index.get(key, []))

    def save(self, filename):
        # 将内存中的B-Tree保存到磁盘上
        with open(filename, 'w',encoding='utf-8') as f:
            for key, value in self.index.items():
                f.write(f"{key},{value}\n")

    @staticmethod
    def load(filename):
        # 从磁盘上的文件加载B-Tree到内存中
        index = BTreeIndex()
        with open(filename, 'r',encoding='utf-8') as f:
            for line in f:
                key, value = line.strip().split(',')
                index.insert(key, value)
        return index
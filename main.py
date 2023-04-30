from repl import REPL

from os import environ

from engine.utils import get_columns

from engine.index import IndexType

def main():
    environ['root_dir']='example'
    repl = REPL()
    #DEBUG
    repl.use_database("db1")
    while True:
        print('=== Welcome to REPL ===')
        print('Please choose an operation:')
        print('1. Create Database')
        print('2. Drop Database')
        print('3. Use Database')
        print('4. Create Table')
        print('5. Drop Table')
        print('6. Insert Data')
        print('7. Select Data')
        print('8. Create Index')
        print('9. Drop Index')
        print('10. Quit')
        choice = input('Enter your choice: ')
        if choice == '1':
            db_name = input('Enter database name: ')
            repl.create_database(db_name)
        elif choice == '2':
            db_name = input('Enter database name: ')
            repl.drop_database(db_name)
        elif choice == '3':
            db_name = input('Enter database name: ')
            repl.use_database(db_name)
        elif choice == '4':
            table_name = input('Enter table name: ')
            types=input('enter attribute type separated by commas: ')
            names=input('enter column names separate by comma: ')
            columns=get_columns(types, names)           
            repl.create_table(table_name, columns)
        elif choice == '5':
            table_name = input('Enter table name: ')
            repl.drop_table(table_name)
        elif choice == '6':
            table_name = input('Enter table name: ')
            data = input('Enter data separated by commas: ').split(',')
            repl.insert_into(table_name, data)
        elif choice == '7':
            table_name = input('Enter table name: ')
            repl.select(table_name)
        elif choice == '8':
            table_name = input('Enter table name: ')
            column_name = input('Enter column name: ')
            index_type = IndexType.BTree if input('Enter index type (Hash/BTree): ')=='BTree' else IndexType.Hash
            repl.create_index(table_name, column_name, index_type)
        elif choice == '9':
            table_name = input('Enter table name: ')
            column_name = input('Enter column name: ')
            repl.drop_index(table_name, column_name)
        elif choice == '10':
            repl.exit()
            break
        else:
            print('Invalid choice. Please try again.')

main()

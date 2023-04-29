from repl import REPL

def main():
    repl = REPL()
    while True:
        print('=== Welcome to REPL ===')
        print('Please choose an operation:')
        print('1. Create Database')
        print('2. Drop Database')
        print('3. Create Table')
        print('4. Drop Table')
        print('5. Insert Data')
        print('6. Select Data')
        print('7. Quit')
        choice = input('Enter your choice: ')
        if choice == '1':
            db_name = input('Enter database name: ')
            repl.create_database(db_name)
        elif choice == '2':
            db_name = input('Enter database name: ')
            repl.drop_database(db_name)
        elif choice == '3':
            db_name = input('Enter database name: ')
            table_name = input('Enter table name: ')
            columns = input('Enter columns separated by commas: ').split(',')
            repl.create_table(db_name, table_name, columns)
        elif choice == '4':
            db_name = input('Enter database name: ')
            table_name = input('Enter table name: ')
            repl.drop_table(db_name, table_name)
        elif choice == '5':
            db_name = input('Enter database name: ')
            table_name = input('Enter table name: ')
            data = input('Enter data separated by commas: ').split(',')
            repl.insert_data(db_name, table_name, data)
        elif choice == '6':
            db_name = input('Enter database name: ')
            table_name = input('Enter table name: ')
            repl.select_data(db_name, table_name)
        elif choice == '7':
            repl.exit()
            break
        else:
            print('Invalid choice. Please try again.')

main()

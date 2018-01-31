import sqlite3
import os
import sys

isDatabaseExist = os.path.isfile('world.db')
dbcon = sqlite3.connect('world.db')


def main(args):
    if not isDatabaseExist and args[1] is not None:
        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""CREATE TABLE tasks(
                            id INTEGER PRIMARY KEY, 
                            task_name TEXT NOT NULL, 
                            worker_id INTEGER REFERENCES workers(id), 
                            time_to_make INTEGER NOT NULL, 
                            resource_name TEXT NOT NULL, 
                            resource_amount INTEGER NOT NULL
                           )""")
            cursor.execute("""CREATE TABLE workers(
                        id INTEGER PRIMARY KEY, 
                        name TEXT NOT NULL, 
                        status TEXT NOT NULL 
                       )""")
            cursor.execute("""CREATE TABLE resources(
                        name TEXT PRIMARY KEY,
                        amount INTEGER NOT NULL
                       )""")
        config_name = args[1]
        with open(config_name) as input_file:
            for line in input_file:
                data_list = line.rstrip('\n').split(',')
                if len(data_list) == 2:  # resources case
                    cursor.execute("INSERT INTO resources VALUES (?,?)", [data_list[0], data_list[1]])
                elif len(data_list) == 3:  # workers case
                    cursor.execute("INSERT INTO workers VALUES (?,?,?)",
                                   [data_list[1], data_list[2], 'idle'])
                elif len(data_list) == 5:  # tasks case
                    cursor.execute("INSERT INTO tasks VALUES (?,?,?,?,?,?)",
                                   [None, data_list[0], data_list[1], data_list[4], data_list[2], data_list[3]])
        dbcon.commit()

if __name__ == '__main__':
    main(sys.argv)

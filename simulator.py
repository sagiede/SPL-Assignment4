import sqlite3
dbcon = sqlite3.connect('world.db')

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

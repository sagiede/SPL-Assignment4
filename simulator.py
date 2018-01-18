import sqlite3
import os
dbcon = sqlite3.connect('world.db')

def main():
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks_list = cursor.fetchall()
        cursor.execute("SELECT * FROM workers")
        workers_list = cursor.fetchall()

        #while os.path.isfile('world.db') and len(tasks_list) > 0:
           # for worker in workers_list:
           #     if worker["status"] == "idle":





if __name__ == '__main__':
    main()
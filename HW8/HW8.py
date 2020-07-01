import argparse
import csv
import os
import sqlite3


parser = argparse.ArgumentParser(description='Provide name of project after -w')
parser.add_argument('-w', '--where', nargs='+', type=str, help='Enter project name', required=True)
args = parser.parse_args()

db_name = 'MyDatabase.db'
db_path = f'{os.getcwd()}\\{db_name}'

# Видаляє базу даних, якщо вже існує
if os.path.exists(db_path):
    os.remove(db_path)
    print(f'\nThe "{db_name}" database was recreated.\n')

# Створення підключення до бази
db_conn = sqlite3.connect(db_name)

# Створення курсору
handle = db_conn.cursor()

# Створення таблиці
with db_conn:
    handle.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE Projects(
            Name TEXT PRIMARY KEY,
            Description TEXT,
            Deadline INTEGER NOT NULL);
        CREATE TABLE Tasks(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Priority INTEGER NOT NULL,
            Details TEXT NULL,
            Status TEXT NOT NULL,
            Deadline INTEGER NOT NULL,
            Completed INTEGER NULL,
            Project TEXT NOT NULL,
            FOREIGN KEY(Project) REFERENCES Projects(Name));
        """)

with open('Project.csv', 'r') as f:
    f_csv = csv.DictReader(f, delimiter='|')
    with db_conn:
        for line in f_csv:
            handle.execute("""INSERT INTO Projects (Name, Description, Deadline) 
                                      VALUES (?, ?, ?);""",
                           (line['Name'], line['Description'], line['Deadline']))

with open('Tasks.csv', 'r') as f:
    f_csv = csv.DictReader(f, delimiter='|')
    with db_conn:
        for line in f_csv:
            handle.execute("""INSERT INTO Tasks (Priority, Details, Status, Deadline, Completed, Project) 
                                  VALUES (?, ?, ?, ?, ?, ?);""",
                           (line['Priority'], line['Details'], line['Status'], line['Deadline'],
                            line['Completed'], line['Project']))


with db_conn:
    handle.execute("SELECT "
                   "Id, Priority, Details, Status, date(Deadline, 'unixepoch') AS Deadline,"
                   "date(Completed, 'unixepoch') AS  Completed, Project "
                   "FROM Tasks "
                   f"WHERE Project = '{' '.join(args.where)}'")
    result_set = handle.fetchall()
db_conn.close()

if len(result_set) != 0:
    print('(Id, Priority, Details, Status, Deadline, Completed, Project)')
    for line in result_set:
        print(line)
else:
    print(f"Tasks for '{' '.join(args.where)}' project were not found. Please check entered project name.")

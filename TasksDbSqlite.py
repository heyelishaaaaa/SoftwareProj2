'''
This is the interface to an SQLite Database
'''

import sqlite3
import csv
from tkinter import filedialog

class TasksDbSqlite:
    def __init__(self, dbName='Tasks.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.jsonFile = self.dbName.replace('.db', '.json')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tasks (
                item TEXT PRIMARY KEY,
                name TEXT,
                subject TEXT,
                category TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Tasks (
                    item TEXT PRIMARY KEY,
                    name TEXT,
                    subject TEXT,
                    category TEXT,
                    status TEXT)''')
        self.commit_close()

    def fetch_tasks(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Tasks')
        tasks =self.cursor.fetchall()
        self.conn.close()
        return tasks

    def insert_task(self, item, name, subject, category, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Tasks (item, name, subject, category, status) VALUES (?, ?, ?, ?, ?)',
                    (item, name, subject, category, status))
        self.commit_close()

    def delete_task(self, item):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Tasks WHERE item = ?', (item,))
        self.commit_close()

    def update_task(self, new_name, new_subject, new_category, new_status, item):
        self.connect_cursor()
        self.cursor.execute('UPDATE Tasks SET name = ?, subject = ?, category = ?, status = ? WHERE item = ?',
                    (new_name, new_subject, new_category, new_status, item))
        self.commit_close()

    def item_exists(self, item):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Tasks WHERE item = ?', (item,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_tasks()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

    def export_json(self):
        with open(self.jsonFile, "w") as filehandle:
            dbEntries = self.fetch_tasks()
            entries_str_list = []

            for entry in dbEntries:
                entry_str = f'{{"item": "{entry[0]}", "name": "{entry[1]}", "subject": "{entry[2]}", "category": "{entry[3]}", "status": "{entry[4]}"}}'
                entries_str_list.append(entry_str)

            filehandle.write('[' + ',\n'.join(entries_str_list) + ']')

    def import_csv(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])

        if file_path:
            data = self.read_csv(file_path)
            for row in data:
                item, name, subject, category, status = row
                self.insert_task(item, name, subject, category, status)

            print('CSV imported successfully.')

    def read_csv(self, file_path):
        data = []
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        return data

def test_TasksDb():
    iTasksDb = TasksDbSqlite(dbName='TasksDbSql.db')

    for entry in range(30):
        iTasksDb.insert_task(entry, f'Name{entry}', f'EEE 111 {entry}', 'Homework', 'Not Started')
        assert iTasksDb.item_exists(entry)

    all_entries = iTasksDb.fetch_tasks()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iTasksDb.update_task(f'Name{entry}', f'EEE 111 {entry}', 'Long Exam', 'In Progress', entry)
        assert iTasksDb.item_exists(entry)

    all_entries = iTasksDb.fetch_tasks()
    assert len(all_entries) == 30

    for entry in range(10):
        iTasksDb.delete_task(entry)
        assert not iTasksDb.item_exists(entry) 

    all_entries = iTasksDb.fetch_tasks()
    assert len(all_entries) == 20
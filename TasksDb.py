from TasksDbEntry import TasksDbEntry
import json
import csv
from tkinter import filedialog

class TasksDb: 
    def __init__(self, init=False, dbName='TasksDb.csv'):
        # CSV filename         
        self.dbName = dbName
        self.jsonFile = dbName.replace('.csv', '.json')  # Change the attribute name
        # initialize container of database entries 
        print('TODO: __init__')
        self.entries = []


    def fetch_tasks(self):
        print('\nTODO: fetch_tasks')
        return [(entry.item, entry.name, entry.subject, entry.category, entry.status) for entry in self.entries]

    def insert_task(self, item, name, subject, category, status):
        newEntry = TasksDbEntry(item=item, name=name, subject=subject, category=category, status=status)
        self.entries.append(newEntry)
        print('TODO: insert_task')
        print('Task inserted successfully.')

    def delete_task(self, item):
        for entry in self.entries:
            if entry.item == item:
                self.entries.remove(entry)
                print('TODO: delete_task')
                print('Task deleted successfully.')
                return
       
    def update_task(self, new_name, new_subject, new_category, new_status, item):
        for entry in self.entries:
            if entry.item == item:
                entry.name = new_name
                entry.subject = new_subject
                entry.category = new_category
                entry.status = new_status
                print('TODO: update_task')
                print('Task updated successfully.')
                return

    def export_csv(self):
        with open(self.dbName, mode='w', newline='') as file:
            for entry in self.entries:
                file.write(f"{entry.item},{entry.name},{entry.subject},{entry.category},{entry.status}\n")
        print('TODO: export_csv')
        print('CSV exported successfully.')

    def export_json(self):
        data = []
        for entry in self.entries:
            entry_data = {
                "item": entry.item,
                "name": entry.name,
                "subject": entry.subject,
                "category": entry.category,
                "status": entry.status
            }
            data.append(entry_data)

        with open(self.jsonFile, "w") as filehandle:
            json.dump(data, filehandle, indent=2)

        print('TODO: export_json')
        print('JSON exported successfully.')

    def import_csv(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.entries = []
            data = self.read_csv(file_path)
            for row in data:
                item, name, subject, category, status = row
                new_entry = TasksDbEntry(item, name, subject, category, status)
                self.entries.append(new_entry)

            print('TODO: import_csv')
            print('CSV imported successfully.')

    def read_csv(self, file_path):
        data = []
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        return data
    
    def item_exists(self, item):
        return any(entry.item == item for entry in self.entries)

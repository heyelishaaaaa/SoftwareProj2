from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from TasksDbSqlite import TasksDbSqlite

class TasksGuiTk(Tk):

    def __init__(self, dataBase=TasksDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('First Semester Task Tracker')
        self.geometry('1500x500')
        self.config(bg='#cdb4db')
        self.resizable(False, False)

        self.font1 = ('Copperplate Gothic Light', 20, 'bold')
        self.font2 = ('Bookman Old Style', 12, 'bold')
        self.font3 = ('Bookman Old Style', 10)

        # Data Entry Form
        # 'Item' Label and Entry Widgets
        self.item_label = self.newCtkLabel('Item')
        self.item_label.place(x=20, y=40)
        self.item_entryVar = StringVar()
        self.item_entry = self.newCtkEntry(entryVariable=self.item_entryVar)
        self.item_entry.place(x=100, y=40)

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=20, y=100)
        self.name_entryVar = StringVar()
        self.name_entry = self.newCtkEntry(entryVariable=self.name_entryVar)
        self.name_entry.place(x=100, y=100)

        # 'Subject' Label and Combo Box Widgets
        self.subject_label = self.newCtkLabel('Subject')
        self.subject_label.place(x=20, y=160)
        self.subject_cboxVar = StringVar()
        self.subject_cboxOptions = ['EEE 111', 'EEE 113', 'EEE 118', 'Math 21', 'Physics 71', 'Speech 30', 'PE 2']
        self.subject_cbox = self.newCtkComboBox(options=self.subject_cboxOptions, 
                                    entryVariable=self.subject_cboxVar)
        self.subject_cbox.place(x=100, y=160)

        # 'Category' Label and Combo Box Widgets
        self.category_label = self.newCtkLabel('Category')
        self.category_label.place(x=20, y=220)
        self.category_cboxVar = StringVar()
        self.category_cboxOptions = ['Homework', 'Notes', 'Problem Set', 'Long Exam', 'Presentation']
        self.category_cbox = self.newCtkComboBox(options=self.category_cboxOptions, 
                                    entryVariable=self.category_cboxVar)
        self.category_cbox.place(x=100, y=220)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=280)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Not Started', 'In Progress', 'Done']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=280)


        self.add_button = self.newCtkButton(text='Add Task',
                                onClickHandler=self.add_entry,
                                fgColor='#ffc8dd',
                                hoverColor='#ffafcc',
                                borderColor='#ffc8dd')
        self.add_button.place(x=300,y=400)

        self.new_button = self.newCtkButton(text='New Task',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=300,y=450)

        self.update_button = self.newCtkButton(text='Update Task',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=600,y=400)

        self.delete_button = self.newCtkButton(text='Delete Task',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#bde0fe',
                                    hoverColor='#a2d2ff',
                                    borderColor='#bde0fe')
        self.delete_button.place(x=600,y=450)

        self.exportCSV_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.exportCSV_button.place(x=900,y=400)

        self.exportJSON_button = self.newCtkButton(text='Export to JSON',
                                    onClickHandler=self.export_to_json)
        self.exportJSON_button.place(x=1200,y=400)

        self.importCSV_button = self.newCtkButton(text='Import CSV',
                                    onClickHandler=self.import_a_csv)
        self.importCSV_button.place(x=900,y=450)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font3, 
                        foreground='#ffd6ff',
                        background='#c8b6ff',
                        fieldlbackground='#e7c6ff')

        self.style.map('Treeview', background=[('selected', '#cdb4db')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Item', 'Name', 'Subject', 'Category', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Item', anchor=tk.CENTER, width=15)
        self.tree.column('Name', anchor=tk.CENTER, width=200)
        self.tree.column('Subject', anchor=tk.CENTER, width=100)
        self.tree.column('Category', anchor=tk.CENTER, width=150)
        self.tree.column('Status', anchor=tk.CENTER, width=100)

        self.tree.heading('Item', text='Item')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Subject', text='Subject')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=350, y=20, width=1100, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#c8b6ff'

        widget = ttk.Label(self, 
                        text=text)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25
        widget_Options=options

        widget = ttk.Combobox(self, 
                              textvariable=entryVariable,
                              width=widget_Width)
        
        # set default value to 1st option
        widget['values'] = tuple(options)
        widget.current(0)
        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
                            width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        tasks = self.db.fetch_tasks()
        self.tree.delete(*self.tree.get_children())

        # Define tag configurations for different statuses
        self.tree.tag_configure("Not Started", background="red")
        self.tree.tag_configure("In Progress", background="orange")
        self.tree.tag_configure("Done", background="green")

        for task in tasks:
            item, name, subject, category, status = task
            self.tree.insert('', END, values=task, tags=(status,))

        # Apply tags to Treeview items based on status
        for tag, color in [("Not Started", "red"), ("In Progress", "orange"), ("Done", "green")]:
            self.tree.tag_configure(tag, background=color)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.item_entryVar.set('')
        self.name_entryVar.set('')
        self.subject_cboxVar.set('EEE 111')
        self.category_cboxVar.set('Homework')
        self.status_cboxVar.set('Not Started')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.item_entryVar.set(row[0])
            self.name_entryVar.set(row[1])
            self.subject_cboxVar.set(row[2])
            self.category_cboxVar.set(row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        item=self.item_entryVar.get()
        name=self.name_entryVar.get()
        subject=self.subject_cboxVar.get()
        category=self.category_cboxVar.get()
        status=self.status_cboxVar.get()

        if not (item and name and subject and category and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.item_exists(item):
            messagebox.showerror('Error', 'Item already exists')
        else:
            self.db.insert_task(item, name, subject, category, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a task to delete')
        else:
            item = self.item_entryVar.get()
            self.db.delete_task(item)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a task to update')
        else:
            item=self.item_entryVar.get()
            name=self.name_entryVar.get()
            subject=self.subject_cboxVar.get()
            category=self.category_cboxVar.get()
            status=self.status_cboxVar.get()
            self.db.update_task(name, subject, category, status, item)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.json')

    def import_a_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo('Success', f'Data imported from {self.db.dbName}.csv')
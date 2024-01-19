from TasksDb import TasksDb
from TasksGuiTk import TasksGuiTk

def main():
    db = TasksDb(init=False, dbName='TasksDb.csv')
    app = TasksGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()
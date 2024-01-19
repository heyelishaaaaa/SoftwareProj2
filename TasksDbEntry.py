class TasksDbEntry:
    def __init__(self,
                 item=1,
                 name='Task Name',
                 subject='EEE 111',
                 category='Homework',
                 status='Not Started'):
        self.item = item
        self.name = name
        self.subject = subject
        self.category = category
        self.status = status

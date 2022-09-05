
class Event:
    def __init__(self,name,from_date,to_date):
        self.name = name
        self.from_date = from_date
        self.to_date = to_date

class Calendar:
    def __init__(self):
        self.events = {}

    def add_event(self,event:Event):
        if event.name in self.events:
            print('Not unique name')
        elif self.is_colliding(event):
            print('This event is colliding with other')
        else:
            self.events[event.name] = event

    def edit_event(self,name,event:Event):
        self.remove_event(name)
        self.add_event(event)

    def remove_event(self,name):
        if name in self.events:
            print('No such event in the calendar')
        else:
            del self.events[name]

    def is_colliding(self,event):
        start = event.from_date
        end = event.to_date
        for e in self.events.values():
            if e.from_date < end and e.to_date > start:
                return True
        return False
            
c = Calendar()
e1 = Event(1,0,1)
e2 = Event(2,1,2)
c.add_event(e1)
c.add_event(e2)
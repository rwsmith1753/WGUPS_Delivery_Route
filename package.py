
class Package:
    # CONSTRUCTOR
    def __init__(self,info):
        self.id = int(info[0])
        self.street = info[1]
        self.city = info[2]
        self.state = info[3]
        self.zip = info[4]
        self.deadline = info[5]
        self.mass = int(info[6])
        self.notes = info[7]
        self.status = 'HUB'
        
        # CREATE SELF.ADDRESS TO MATCH DISTANCE TABLE ADDRESSES
        self.address = f'{self.street}\n({self.zip})'

    # SET STATUS AT HUB
    def inRoute(self):
        self.status = 'En Route'

    # SET STATUS WHEN DELIVERED
    def delivered(self, time: str('HH:MM:SS AM/PM')):
        self.status = f'Delivered at {time}'

    # GET PACKAGE INFO
    def get_id(self):
        return self.id
    def get_street(self):
        return self.address
    def get_city(self):
        return self.city
    def get_zip(self):
        return self.zip
    def get_deadline(self):
        return self.deadline
    def get_mass(self):
        return self.mass
    def get_notes(self):
        return self.notes
    def get_status(self):
        return self.status

    # SET PACKAGE INFO
    def set_id(self, id: int):
        self.id = id
    def set_street(self, street: str):
        self.street = street
        self.address = f'{self.street}\n({self.zip})' # UPDATE ADDRESS WITH NEW STREET
    def set_city(self, city: str):
        self.city = city
        self.address = f'{self.street}\n({self.zip})' # UPDATE ADDRESS WITH NEW CITY
    def set_zip(self, zip: str):
        self.zip = zip
        self.address = f'{self.street}\n({self.zip})' # UPDATE ADDRESS WITH NEW ZIP
    def set_deadline(self, deadline: str):
        self.deadline = deadline
    def set_mass(self, mass: str):
        self.mass = mass
    def set_notes(self, notes: str):
        self.notes = notes
    def set_status(self, status: str):
        self.status = status

    # PRINT PACKAGE AS STRING
    def __str__(self):
        return f'\nID: {self.id}:\nAddress: {self.address}\nDeadline: {self.deadline}\nWeight: {self.mass} kg\nNotes: {self.notes}\nStatus: {self.status}'
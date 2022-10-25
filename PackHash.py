from package import Package
from typing import Literal

# D. SELF-ADJUSTING DATA STRUCTURE (HASH TABLE)
class PackHash:
    # CONSTRUCTOR
    def __init__(self):
        self.hash = []
        self.length = 10

        # ADD 10 EMPTY LISTS FOR STORING PACKAGES
        for i in range(self.length):
            self.hash.append([])

    # CONVERT PACKAGE ID TO HASH KEY
    def create_key(self, id: int):
        return id % self.length

    # ADD PACKAGE TO HASH TABLE
    #    E. Insert Function
    def add_package(self, package: Package): 
        key = self.create_key(package.id)
        self.hash[key].append(package)

    # GET PACKAGE BY ID
    #    F. Look-Up Function
    def get_package(self, id: int):
        key = self.create_key(id)
        for p in self.hash[key]:
            if p.id == id:
                return p

    # MODIFY PACKAGE INFO
    def modify_package(self, id: int, att: Literal['ID', 'Street', 'City', 'Zip', 'Deadline', 'Mass', 'Notes', 'Status'], new: str):
        package = self.get_package(id)
        att = att.lower()
        if att == 'id':
            package.set_id(new)
        elif att == 'street':
            package.set_street(new)
        elif att == 'city':
            package.set_city(new)
        elif att == 'zip':
            package.set_zip(new)
        elif att == 'deadline':
            package.set_deadline(new)
        elif att == 'mass':
            package.set_mass(new)
        elif att == 'notes':
            package.set_notes(new)
        elif att == 'status':
            package.set_status(new)

        # HANDLE INCORRECT PARAMETER
        else:
            print('Invalid Entry. Transaction voided')
            return
        
    # UPDATE PACKAGE STATUS WHEN DELIVERED
    def deliver(self, id: int, time: str('HH:MM:SS AM/PM')):
        key = self.create_key(id)
        for p in self.hash[key]:
            if p.id == id:
                p.status = f'Delivered at: {time}'

    # GET ALL PACKAGES IN TABLE
    def get_all_packages(self):
        return [p for p in self.hash for p in p]
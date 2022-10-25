import csv
import math
from PackHash import PackHash

# from package import Package

distTable = 'data/WGUPS Distance Table.csv'
class Truck:
    def __init__(self,name):
        self.name = name
        self.payload = []
        self.speed = 18 #MPH
        self.weight = 0
        self.schedule = []
        self.location = ' HUB'
        self.miles = []
        self.travelled = 0
        self.time = 0
        self.deliveries = {}

    def get_payload(self):
        return self.payload
    def get_time(self):
        return "%04d" % self.time
        
    def load_truck(self,packageList):
        if len(packageList) <= 16:
            self.payload = packageList
        else:
            alert = print('Too Many Packages')
            return alert

    def deliver_package(self,id):
        self.payload.remove(id)
        self.status = 'En Route'

    def get_package(self,id):
        return self.payload.get_package(id)

        
    def check_status(self):
        return self.status

    #using hash table

    def load_package(self,Package):
        self.payload.add_package(Package)
        self.weight += Package.mass

    def view_payload(self):
        for p in self.payload:
            print(p)
        # pass

    def deliver(self,Package):
        self.payload.deliver(Package.id)
        self.weight += Package.mass 

    
    def start_route(self,time): 
        from main import allPackages
        # pack = allPackages.get_package(self.payload[4][0])
        # print(f'pack: {pack}')
        for d in range(len(self.payload)):
            for p in range(len(self.payload[d])):
                allPackages.get_package(self.payload[d][p]).status = 'En Route'
        # for p in allPackages.get_all_packages():
        #     if p.id in [[self.payload[i][j] for j in range(len(self.payload[i]))] for i in range(len(self.payload))]:
        #         print(p.id)
        #         p.set_status('En Route')
        self.time = time
        while len(self.payload) > 0:
            delivery = self.payload.pop(0)
            dist = self.miles.pop(0)
            self.travelled += dist
            self.time += (60 / self.speed) * dist
            for package in delivery:
                allPackages.deliver(package,self.time)
            self.deliveries.update({self.time:delivery})

    
            
    def complete_route(self):
        print(f'{self.name} route completed at {self.get_time()}. Total distance travelled: {self.travelled} miles')
        
    
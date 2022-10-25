"""

Author: Ryan Smith
Student ID: 010092517
Email: rsm1479@wgu.edu

Run: python main.py

"""
import csv
from package import Package
from PackHash import PackHash

# DECLARE AND INITIALIZE GLOBAL VARIABLES
global packages, distTable, packTable, allPackages
allPackages = PackHash()
packages = [3, 6, 9, 18, 25, 28, 32, 36, 38] # PREPOPULATE PACKAGE IDS RESERVED FOR TRUCKS 2 AND 3
pack_status = {}

# DISTANCE AND PACKAGE FILES
distTable = 'data/WGUPS Distance Table.csv'
packTable = 'data/WGUPS Package File.csv'

            
# DEFINE TRUCK CLASS VARIABLES AND METHODS
class Truck:
    # CONSTRUCTOR
    def __init__(self, name: str, startTime: str('HH:MM:SS AM/PM')):
        self.name = name
        self.startTime = startTime
        self.payload = []
        self.speed = 18 #MPH
        self.miles = []
        self.traveled = 0
        
        # PARSE STARTTIME INTO 24HR FORMAT TO SIMPLIFY CALCULATIONS
        self.startTime = self.startTime.split(' ')
        self.startHH = int(self.startTime[0].split(':')[0])
        self.startMM = int(self.startTime[0].split(':')[1])
        self.startSec = int(self.startTime[0].split(':')[2])
        self.startAMPM = self.startTime[1]

        if self.startHH >12:
            switchAMPM = 1
            while self.startHH > 12:
                switchAMPM += 1
                self.startHH -= 12
            if switchAMPM % 2 == 0:
                self.startAMPM = 'AM'
            else:
                self.startAMPM = 'PM'
        if self.startAMPM == 'PM' and self.startHH != 12:  
            self.startHH += 12
        
        self.time = [self.startHH,self.startMM,self.startSec,self.startAMPM]
        self.time24 = float(int(f'{"%02d" % self.time[0]}{"%02d" % self.time[1]}') + self.time[2] / 10)

    # GET ALL PACKAGES IN PAYLOAD
    def get_payload(self):
        for i in self.payload:
            for package in i:
                return package.info

    # GET CURRENT TIME
    def get_time(self):
        # CONVERT PACKAGE DELIVERY TIME TO 12HR FORMAT
        return f'{self.time[0]}:{"%02d" % self.time[1]}:{self.time[2]} {self.time[3]}'

    # GET STATUS OF PACKAGES IN PAYLOAD AT TARGET TIME    
    def all_packages_at_time(self, targetTime: str('HH:MM:SS AM/PM')):
        
        #RESET SELF.TIME AND SELF.TRAVELLED
        self.time = [self.startHH,self.startMM,self.startSec,self.startAMPM]
        self.time24 = float(int(f'{"%02d" % self.time[0]}{"%02d" % self.time[1]}') + self.time[2] / 10)
        self.travelled = 0

        # CONVERT TARGET TIME TO 24HR FORMAT
        targetTime = targetTime.split(' ')
        targetHH = int(targetTime[0].split(':')[0])
        targetMM = int(targetTime[0].split(':')[1])
        targetSec = int(targetTime[0].split(':')[2])
        targetAMPM = targetTime[1]
        if targetHH >12:
            switchAMPM = 0
            while self.startHH > 12:
                switchAMPM += 1
                targetHH -= 12
            if switchAMPM % 2 == 0:
                targetAMPM = 'AM'
            else:
                targetAMPM = 'PM'
        if targetAMPM == 'PM' and targetHH != 12:  
            targetHH += 12
        target24 = float(int(f'{"%02d" % targetHH}{"%02d" % targetMM}') + int(targetSec) / 10)

        # SET PACKAGE STATUSES TO 'EN ROUTE'
        for d in range(len(self.payload)):
            for p in range(len(self.payload[d])):
                allPackages.get_package(self.payload[d][p]).status = 'En Route'   

        # START DELIVERIES, STOP AT TARGET TIME 
        for i in range(len(self.payload)):
            if self.time24 < target24:
                # GRAB FRIST PACKAGE
                delivery = self.payload[i]
    
                # GRAB DISTANCE TO FIRST addresses
                dist = self.miles[i]
            
                # ADD DISTANCE TO TRUCK MILES
                self.travelled += dist
    
                # CALCULATE TRAVEL TIME AND CONVERT TO MINUTES AND SECONDS
                time = (60 / self.speed) * dist
                min = int(time - (time % 1)) 
                sec = int(time % 1 * 60) 
                while self.time[2] + sec >= 60:
                    min += 1
                    sec -= 60
                while self.time[1] + min >= 60:
                    self.time[0] += 1
                    min -= 60
                self.time[1] += min
                self.time[2] += sec
                
                # RECONVERT TO 24HR FORMAT AND SET AS CURRENT TRUCK TIME
                self.time24 = float(int(f'{"%02d" % self.time[0]}{"%02d" % self.time[1]}') + self.time[2] / 10)              

                # CONVERT PACKAGE DELIVERY TIME TO 12HR FORMAT
                if self.time24 >= 1200:
                    self.time[3] = 'PM'
                    if self.time24 >= 1300:
                        self.time[0] -= 12
                    
                # GET CURRENT TRUCK TIME AND SET PACKAGE DELIVERY STATUS  -- O(n) => Running Total: 
                if self.time24 < target24:
                    for package in delivery:
                        allPackages.get_package(package).delivered(self.get_time())

    # DELIVER ALL PACKAGES
    def complete_route(self):

        # RESET SELF.TIME AND SELF.TRAVELLED
        self.time = [self.startHH,self.startMM,self.startSec,self.startAMPM]
        self.time24 = float(int(f'{"%02d" % self.time[0]}{"%02d" % self.time[1]}') + self.time[2] / 10)
        self.traveled = 0
        
        # GRAB LAST PACKAGE IN PAYLOAD
        last_package = [allPackages.get_package(p) for p in self.payload[-1]]

        # SET INITIAL STATUS TO 'EN ROUTE' FOR ALL PACKAGES IN PAYLOAD
        for d in range(len(self.payload)):
            for p in range(len(self.payload[d])):
                allPackages.get_package(self.payload[d][p]).status = 'En Route'

        # DELIVER ALL PACKAGES IN PAYLOAD
        for i in range(len(self.payload)):
            delivery = self.payload[i]
            dist = self.miles[i]
            self.traveled += dist

            # CALCULATE TRAVEL TIME AND CONVERT TO MINUTES AND SECONDS
            time = (60 / self.speed) * dist
            min = int(time - (time % 1)) 
            sec = int(time % 1 * 60) 
            while self.time[2] + sec >= 60:
                min += 1
                sec -= 60   
            while self.time[1] + min >= 60:
                self.time[0] += 1
                min -= 60
            self.time[1] += min 
            self.time[2] += sec 

            # RECONVERT TO 24HR FORMAT AND SET AS CURRENT TRUCK TIME
            self.time24 = float(int(f'{"%02d" % self.time[0]}{"%02d" % self.time[1]}') + self.time[2] / 10)              
            # CONVERT PACKAGE DELIVERY TIME TO 12HR FORMAT
            if self.time24 >= 1200:
                self.time[3] = 'PM'
                if self.time24 >= 1300:
                    self.time[0] -= 12

            # UPDATE STATUS WHEN EACH PACKAGE IS DELIVERED
            for package in delivery:
                allPackages.get_package(package).delivered(self.get_time())
            
        # GET DISTANCE TO HUB FROM LAST DELIVERY
        drive_home = addDict[last_package[0].address][0]  
        
        # TRUCK 2 RETURNS TO HUB TO SWAP WITH TRUCK 3
        if self.name == 'Truck 2':
            self.traveled += drive_home 

        # CONVERT PACKAGE DELIVERY TIME TO 12HR FORMAT
        if self.time24 >= 1200:
            self.time[3] = 'PM'
            if self.time24 >= 1300:
                self.time[0] -= 12
        
        print(f'\n{self.name} delivered last package at {self.get_time()}. Total distance traveled: {float("{:.2f}".format(self.traveled))} miles')
####### END TRUCK CLASS ########


# READ PACKAGE FILE
#    Opens packTable file and returns all lines that contain package info
def package_csv():
    with open(packTable) as file:
        reader = csv.reader(file, delimiter=',')
        lines = [line for line in reader]
        return lines[8::] #RETURN ONLY PACKAGE LINES

        
# CREATE ALL PACKAGES FROM PACKAGE FILE AND ADD TO HASH TABLE
#     converts lines from packTable into Packages
#     add Packages to PackHash hash table
def create_PackHash():
    # INSTATIATE PACKAGES 
    for line in package_csv(): 
        package = Package(line)
        
        # SET INITIAL PACKAGE STATUS TO 'HUB'
        package.set_status('HUB')
        
        allPackages.add_package(package)
        
        # ADD NEW PACKAGE IDS TO PACKAGES LIST 
        if int(package.id) not in packages:
            packages.append(package.id)

            
# CREATE DICTIONARY {ADDRESS:ADDRESS INDEX:[DISTANCES]}
#    Supplimentary data structure
#    Gets complete list of distances for all addresses
def get_address_indexes():
    global addDict
    addDict = {}
    addresses = []
    with open(distTable) as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            addresses.append(line)
        for a in range(1, len(addresses)):
            for b in range(2, len(addresses[a])):
                if addresses[a][b] == '':
                    addresses[a][b] = float(addresses[b - 1][a + 1])
                addresses[a][b] = float(addresses[a][b])
            addDict.update({addresses[a][1]: [i for i in addresses[a][2:]]})

            
# READ PACKAGE FILE AND LOAD PACKAGES ONTO EACH TRUCK
def load_trucks():
    global truck1, truck2, truck3, packages,pack_truck_index
    truck1_packages = []
    truck2_packages = [3, 18, 36, 38, 6, 25, 28, 32] # PACKAGES REQUIRED ON TRUCK 2
    truck3_packages = [9] # TRUCK 3 LEAVES HUB AFTER PACKAGE 9 ADDRESS IS CORRECTED
    
    # CREATE AND PREPOPULATE {PACKAGE_ID:TRUCK} DICTIONARY
    pack_truck_index = {3:truck2, 6:truck2, 9:truck3, 18:truck2, 25:truck2, 25:truck2, 32:truck2, 36:truck2, 38:truck2}
    truck1_count = 0
    truck2_count = 8
    truck3_count = 1

    # LOAD PACKAGES ONTO TRUCKS 
    for line in package_csv():
        package = Package(line)
        
        # ADD PRIORITY PACKAGES TO TRUCK 1 
        if package.deadline != 'EOD' and package.id not in truck1_packages and package.id not in truck2_packages and package.id not in truck3_packages and package.id in packages and truck1_count < 16:
            truck1_packages.append(package.id)
            truck1_count += 1
            pack_truck_index.update({package.id:truck1})
            packages.remove(package.id)
            
        # IF NOT PRIORITY, ADD PACKAGE TO TRUCK 2
        elif truck2_count < 16 and package.id not in truck1_packages and package.id not in truck2_packages and package.id not in truck3_packages and package.id in packages:
            truck2_packages.append(package.id)
            truck2_count += 1
            pack_truck_index.update({package.id:truck2})
            packages.remove(package.id)

        # IF TRUCK 2 FULL, ADD PACKAGE TO TRUCK 3
        elif package.id not in truck1_packages and package.id not in truck2_packages and package.id not in truck3_packages and package.id in packages:
            truck3_packages.append(package.id)
            truck3_count += 1
            pack_truck_index.update({package.id:truck3})
            packages.remove(package.id)
                
    # SET TRUCK PAYLOADS
    truck1.payload = truck1_packages
    truck2.payload = truck2_packages
    truck3.payload = truck3_packages

# A. SELF-ADJUSTING ALGORITHM (NEAREST NEIGHBOR)
def optimize_route(Truck):
    '''    
    FIND OPTIMAL ROUTE FOR TRUCK PAYLOAD
        Generates a list of truck's package destinations
        Sets the first delivery as the closest address to HUB
            Appends Package.id to 'route'
            Deletes address from 'destinations' to eliminate duplicates
        Uses the previous address's row index to find the distance column index
            Finds min distance out of remaining destinations
            Appends next Package.id to 'route'
            **Repeats until all destinations reached
    
        Package.id's have been appended to 'route' in optimal order of delivery
        Truck's original payload is replaced with 'route'    
    '''
    route = []
    distances = []
    destinations = {}

    # SET ADDRESS FOR EACH PACKAGE
    for p in Truck.payload:
        destinations.update({allPackages.get_package(p).address: p})

    # FIND CLOSEST ADDRESS TO HUB
    next = None
    idx = 0
    for a in list(addDict):
        if a in destinations:
            if next == None:
                next = [a, idx, addDict[a][0]]
            else:
                if addDict[a][0] < addDict[next[0]][0]:
                    next = [a, idx, addDict[a][0]]
        idx += 1
    distances.append(next[2])
    route.append([p for p in Truck.payload if allPackages.get_package(p).address == next[0]])
    del destinations[next[0]]

    while len(list(destinations)) > 0:
        prev = next # HOLD PREVIOUS DELIVERY
        next = None
        idx = 0
        for a in list(addDict):
            if a in destinations:
                if next == None:
                    next = [a, idx, addDict[a][prev[1]]]
                else:
                    if addDict[a][prev[1]] < addDict[next[0]][prev[1]]:
                        next = [a, idx, addDict[a][prev[1]]]
            idx += 1
        distances.append(next[2])
        route.append([p for p in Truck.payload if allPackages.get_package(p).address == next[0]])
        del destinations[next[0]]
        
    Truck.payload = route
    Truck.miles = distances

# MAIN MENU     
#    G. Interface
def main_menu():
    
    # MENU OPTIONS
    print('1. View status of a package')
    print('2. View status of all packages')
    print('3. View total miles driven by each truck')
    
    menu = input('Enter 1, 2, or 3: ')
    if menu == '1':
        id = int(input('Enter Package ID: '))
        targetTime = input('Enter time (HH:MM:SS AM/PM): ')
        print(f'\nStatus of Package {id} at {targetTime}')
        targetTruck = pack_truck_index[id]
        targetTruck.all_packages_at_time(targetTime)
        print(f'Package {id}: {allPackages.get_package(id).status}')

        #PROMPT TO RETURN TO MAIN MENU OR EXIT
        back = input('Return to main menu? (Y/N): ')
        if back.lower() == 'y':
            main_menu()
        else:
            return
            
    elif menu == '2':
        targetTime = input('Enter time (HH:MM:SS AM/PM): ')
        truck1.all_packages_at_time(targetTime)
        truck2.all_packages_at_time(targetTime)
        truck3.all_packages_at_time(targetTime)
        
        # SHOW DELIVERY STATUS OF EACH PACKAGE 
        print('\n')
        for id in range(1,41):
            print(f'Package {id}: {allPackages.get_package(id).status}')
        print('\n')
        
        # PROMPT TO RETURN TO MAIN MENU OR EXIT
        back = input('Return to main menu? (Y/N): ')
        if back.lower() == 'y':
            main_menu()
        else:
            return
            
    # DISTANCE TRAVELLED FOR EACH TRUCK AND SUM OF DISTANCES TRAVELLED   
    elif menu == '3':
        truck1.complete_route()
        truck2.complete_route()
        truck3.complete_route()
        
        # PRINT TOTAL DISTANCE TRAVELLED FOR ALL TRUCKS
        total_miles = truck1.traveled + truck2.traveled + truck3.traveled
        print(f'\nTotal Miles Driven: {float("{:.2f}".format(total_miles))}\n')

        # PROMPT TO RETURN TO MAIN MENU OR EXIT
        back = input('Return to main menu? (Y/N): ')
        if back.lower() == 'y':
            main_menu()
        else:
            return
            
    # HANDLE INCORRECT ENTRY
    else:
        print('INVALID SELECTION')
        main_menu()
            
# ENTRY POINT
def run():    
    global truck1, truck2, truck3
    
    # INSTATIATE TRUCKS
    #    Truck 1 leaves hub at 8:00 AM
    #    Truck 2 leaves hub at 9:05 AM after more packages arrive
    #    Truck 3 leaves hub at 11:25 AM after correcting Package 9 address
    truck1, truck2, truck3 = Truck('Truck 1','8:00:00 AM'), Truck('Truck 2','9:05:00 AM'), Truck('Truck 3','11:25:00 AM')

    create_PackHash()
    get_address_indexes()
    load_trucks()
    
    # OPTIMIZE ROUTES FOR TRUCKS 1 AND 2
    optimize_route(truck1)
    optimize_route(truck2)
    
    # CORRECT PACKAGE 9 ADDRESS
    allPackages.modify_package(9,'street','410 S State St')
    allPackages.modify_package(9,'zip',84111)
    
    # OPTIMIZE TRUCK 3 ROUTE WITH CORRECTED ADDRESS
    optimize_route(truck3) 

    main_menu()

if __name__ == '__main__':
    run()

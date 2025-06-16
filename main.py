from data_series import DataSeries
from truck_object import TruckObject
from package_object import PackageObject
from hash_table import HashTable
import math
from datetime import timedelta, time

# create a data series object and populate the tables
ds = DataSeries()
ds.create_distance_table()
ds.create_package_table()
ds.create_address_table()

# instance of HashTable to store PackageObjects
hash_table = HashTable()
def load_hash_table():
    for package in ds.package_file:
        package = PackageObject(
            id = int(package[0]),
            address = package[1],
            city = package[2],
            state = package[3],
            zip_code = package[4],
            deadline = package[5],
            weight = int(package[6]),
            note = package[7],
            status = "At hub", # start with initial status,
            truck_num=None  # no truck assigned initially
        )
    hash_table.insert(package)

# loop through address table and retrive the index to cross reference distance table
def address_lookup(address):
    for row in ds.address_file:
        if address in row[2]:
            return int(row[0])

# distance between locations
def calucate_distance(row, col):
    # the table is symmetric, so if one result is None because cell is empty, access distance with the alternate index
    distance_rc = ds.distance_table[row][col]
    distance_cr = ds.distance_table[col][row]
    return distance_rc if distance_rc is not None else distance_cr

# the idea was to split up packages with some sort of logic 
# def distribute_packages():
#     eod_simple = [] # simplist packages to eliminate are EOD delivery with no special instructions
#     timed_packages = []
#     special_packages = []
#     for package in ds.package_file:
#         # append package id's
#         if package[5] == "EOD" and package[7] == None:
#             eod_simple.append(package[0]) 
#         elif package[5] != "EOD":
#             timed_packages.append(package[0])
#         else:
#             special_packages.append(package[0])
    
#     print(eod_simple) 
#     print(timed_packages)
#     print(special_packages)
# distribute_packages()

# instantiate trucks with packages loaded manually
truck1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
truck2_packages = [3, 6, 12, 18, 22, 25, 26, 27, 28, 32, 35, 36, 38, 39]
truck3_packages = [2, 4, 5, 7, 8, 9, 10, 11, 17, 21, 23, 24, 33]


# Truck objects, initialize at the hub
hub = ds.address_file[0][2]  # hub address from address file
truck1 = TruckObject(truck_num=1, packages=truck1_packages, cur_addr=hub)
truck2 = TruckObject(truck_num=2, packages=truck2_packages, cur_addr=hub)
truck3 = TruckObject(truck_num=3, packages=truck3_packages, cur_addr=hub)

# add_packages() takes a list of int:id and then appends package.id to truck.packages
truck1.add_packages(truck1.packages)
truck2.add_packages(truck2.packages)
truck3.add_packages(truck3.packages)

# random test in the middle of my main.py..... legit
# validate distribution of packages is correct
def validate_package_distribution() -> bool:
    pkg_set = set()
    all_pkgs = truck1.packages + truck2.packages + truck3.packages
    for pkg in all_pkgs:
        pkg_set.add(pkg)
    if len(pkg_set) == len(all_pkgs):
        print("Package distribution is valid.")
        return True
#################################
#validate_package_distribution()


def negotiate_route(truck: TruckObject): # specifying the type helps with language server completion 
    # truck.packages has array of packages, mileage starts at 0
    left = [] # left to deliver
    # print(f"packages before sorting by nearest distance: {truck.packages}")
    for pkg_id in truck.packages:
        pkg = hash_table.lookup(pkg_id) # retrives the PackageObject and place into left array
        if pkg is not None:
            left.append(pkg)
    # the algorithm needs to reconstruct truck.packages list in the order of delivery
    truck.clear_packages()
    
    # begin nearest neighbor algo
    # - add all packages to left(to deliver)
    # - find the nearest package to the truck's current address and move truck there
    #      - add the package to truck.packages
    while left:
        next_address = math.inf # this is distance away to next address, default to infinity
        next_package = None
        for pkg in left:
            # calculate address works like [row][col], so find the package in the row, then scroll over to truck location
            if calucate_distance(address_lookup(pkg.address), address_lookup(truck.cur_addr)) <= next_address:
                next_address = calucate_distance(address_lookup(pkg.address), address_lookup(truck.cur_addr))
                next_package = pkg
            
        # add pkg to truck.packages and then remove from left to exhaust the while loop
        truck.add_packages([next_package.id])
        left.remove(next_package)
        truck.cur_addr = next_package.address
        truck.mileage_sum += next_address
        
        
        # increment the time the truck mileage and then set a baseline time for the package
        # delivery time will be truck departure + baseline time
        truck.time += timedelta(hours=next_address / truck.avg_speed)
        next_package.base_time = truck.time
        
        
    # post sorted debug
    # print(f"packages after sorting by nearest distance: {truck.packages}")
    
    
    # for pkg_id in truck.packages:
    #     pkg = hash_table.lookup(pkg_id)
    #     print(f"Package ID: {pkg.id}, Address: {pkg.address}, Delivery Time: {pkg.delivery_time}, Status: {pkg.status}")
######################
negotiate_route(truck1)
negotiate_route(truck2)
negotiate_route(truck3)

def main():
    # load the hash table with PackageObjects
    load_hash_table()
    
    
    
    
    # use the total time from the nearest neighbor algo to set the delivery time
    # truck 3 can leave as soon as truck 1 driver is back
    def set_delivery_time():
        
        # truck1 has (mostly) packages that need to be delivered by 10:30, set departure time to 8:00am
        # truck1 packages [1, 13, 14, 15, 16, 19, 20, 30, 31, 34, 37, 40]
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRUCK 1 INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        truck1.depart = timedelta(hours=8)
        print(f"truck 1 base: {truck1.time}")
        print(f"truck 1 depart: {truck1.depart}")
        for pkg in truck1.packages:
            pkg = hash_table.lookup(pkg)
            pkg.departure_time = truck1.depart
            pkg.delivery_time = truck1.depart + pkg.base_time
            #pkg.print_package_info()
            
        # after truck1 has completed its route, return to hub
        truck1_return_trip = calucate_distance(address_lookup(hub), address_lookup(truck1.cur_addr))
        truck1.time += timedelta(hours=truck1_return_trip / truck1.avg_speed)    
        
        # truck2 packages 6, 25, 28, 32 arrive at 9:05, can depart immediately at 9:05
        # packages 3, 18, 36, 38 must be on truck 2
        # truck2 packages [3, 6, 12, 22, 24, 25, 26, 27, 28, 29, 32, 35, 36, 38, 39]
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRUCK 2 INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        truck2.depart = timedelta(hours=9, minutes=5)
        print(f"truck 2 base: {truck2.time}")
        print(f"truck 2 depart: {truck2.depart}")
        for pkg in truck2.packages:
            pkg = hash_table.lookup(pkg)
            pkg.departure_time = truck2.depart
            pkg.delivery_time = truck2.depart + pkg.base_time
            #pkg.print_package_info()
            
        # return trip for truck2
        truck2_return_trip = calucate_distance(address_lookup(hub), address_lookup(truck2.cur_addr))
        truck2.time += timedelta(hours=truck1_return_trip / truck2.avg_speed)
        
        
        # truck3 can leave after truck1 returns
        # depart = truck1.depart + truck1.time + return trip + round up to next hour
        # truck3 packages [2, 4, 5, 7, 8, 9, 10, 11, 17, 18, 21, 23, 33]
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRUCK 3 INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(f"truck1 return time: {truck1.depart + truck1.time}")
        truck3_depart = truck1.depart + truck1.time 
        truck3.depart = truck3_depart
        print(f"truck 3 base: {truck3.time}")
        print(f"truck 3 depart: {truck3.depart}")
        for pkg in truck3.packages:
            pkg = hash_table.lookup(pkg)
            pkg.departure_time = truck3.depart
            pkg.delivery_time = truck3.depart + pkg.base_time
            # pkg.print_package_info()
    ###################
    set_delivery_time()
            
    # set the package status based on the time
    def check_status(time):
        for pkg_id in truck1.packages:
            pkg = hash_table.lookup(pkg_id)
            pkg.update_status(time)
            pkg.print_package_info()
        
        for pkg_id in truck2.packages:
            pkg = hash_table.lookup(pkg_id)
            pkg.update_status(time)
            pkg.print_package_info()
        
        for pkg_id in truck3.packages:
            pkg = hash_table.lookup(pkg_id)
            pkg.update_status(time)
            pkg.print_package_info()
            
    def utility_menu(option: int):
        if option == 1:
            ds.print_distance_table()
        elif option == 2:
            ds.print_package_table()
        elif option == 3:
            ds.print_address_table()
        elif option == 4:
            truck1.print_truck_info()
            truck2.print_truck_info()
            truck3.print_truck_info()
        else:
            print("Invalid option. Please try again.")
    
    # start main cli functionality 
    print("Welcome to the WGUPS package lookup!")
    print("Use the following utilities to view package itinerary and truck information:")
    print("1. View Distance Table")
    print("2. View Package Table")
    print("3. View Address Table")
    print("4. View Truck Information")
    while True:
        try:
            option = int(input("Enter an option (1-4) or 0 to exit: "))
            if option == 0:
                print("Exiting the program. Goodbye!")
                break
            utility_menu(option)
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 4.")
    
    
    
    


    
    
        
    
    
if __name__ == "__main__":
    main()
    
    
    
    
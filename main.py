from data_series import DataSeries
from truck_object import TruckObject
from package_object import PackageObject
from hash_table import HashTable
import math, re, sys
from datetime import timedelta, time

##############################################################
# Ben Robbins SID: 011007860
# WGUPS Package Delivery System using the Nearest Neighbor Algorithm and package storage in a Hash Table
#  _       __________  ______  _____
# | |     / / ____/ / / / __ \/ ___/
# | | /| / / / __/ / / / /_/ /\__ \ 
# | |/ |/ / /_/ / /_/ / ____/___/ / 
# |__/|__/\____/\____/_/    /____/  
                                  

# load the hash table with PackageObjects
# time and space complexity O(N)
def load_hash_table(ds: DataSeries, hash_table: HashTable):
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
            status = "At hub", # init "At hub"
            truck_num = None # init None
        )
        hash_table.insert(package)

# loop through address table and retrive the index to cross reference distance table
# time complexity O(N)
# space complexity O(1), no data stored
def address_lookup(ds:DataSeries, address):
    for row in ds.address_file:
        if address in row[2]:
            return int(row[0])

# distance between locations
# time and space complexity O(1)
def calculate_distance(ds:DataSeries, row, col):
    # the table is symmetric, so if one result is None because cell is empty, access distance with the alternate index
    distance_rc = ds.distance_table[row][col]
    distance_cr = ds.distance_table[col][row]
    return distance_rc if distance_rc is not None else distance_cr

# random test in the middle of my main.py..... legit
# validate distribution of packages is correct by comparing length of set() to a list of all currently assigned packages
# time complexity O(N)
# space complexity 0(N)
def validate_package_distribution(all_pkgs) -> bool:
    pkg_set = set()
    for pkg in all_pkgs:
        pkg_set.add(pkg)
    if len(pkg_set) == len(all_pkgs):
        print("Package distribution is valid.")
        return True
#################################
#validate_package_distribution()

# nearest neighbor algorithm to sort packages by distance
# N(N-1)/2 -> O(N^2) time complexity
# N packages split between two internal data structures -> space complexity O(N)
def negotiate_route(truck: TruckObject, hash_table:HashTable, ds:DataSeries): # specifying the type helps with language server completion 
    # truck.packages has array of packages, mileage starts at 0
    left = [] # left to deliver
    # print(f"packages before sorting by nearest distance: {truck.packages}")
    for pkg_id in truck.packages:
        pkg = hash_table.lookup(pkg_id) # retrives the PackageObject and place into left array
        pkg.update_truck_num(truck.truck_num) 
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
            if calculate_distance(ds, address_lookup(ds, pkg.address), address_lookup(ds, truck.cur_addr)) <= next_address:
                next_address = calculate_distance(ds, address_lookup(ds, pkg.address), address_lookup(ds, truck.cur_addr))
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

# use the baseline time to set the delivery times for each truck
# time complexity services all 40 packages for route, split between 3 trucks O(N1+N2+N3) -> Time Complexity O(N)
# No growing data structures, space complexity O(1)
def set_delivery_time(ds:DataSeries, hash_table: HashTable, truck1: TruckObject, truck2: TruckObject, truck3: TruckObject, hub: str):
    
    # truck1 has (mostly) packages that need to be delivered by 10:30, set departure time to 8:00am
    # truck1 packages [1, 13, 14, 15, 16, 19, 20, 30, 31, 34, 37, 40]
    truck1.depart = timedelta(hours=8)
    for pkg in truck1.packages:
        pkg = hash_table.lookup(pkg)
        pkg.departure_time = truck1.depart
        pkg.delivery_time = truck1.depart + pkg.base_time
        
    # after truck1 has completed its route, return to hub
    truck1_return_trip = calculate_distance(ds, address_lookup(ds, hub), address_lookup(ds, truck1.cur_addr))
    truck1.mileage_sum += truck1_return_trip
    truck1.mileage_sum = round(truck1.mileage_sum, 1)  # clean float after all calculations complete
    truck1.time += timedelta(hours=truck1_return_trip / truck1.avg_speed)    
    
    # truck2 packages 6, 25, 28, 32 arrive at 9:05, can depart immediately at 9:05
    # packages 3, 18, 36, 38 must be on truck 2
    # truck2 packages [3, 6, 12, 22, 24, 25, 26, 27, 28, 29, 32, 35, 36, 38, 39]
    truck2.depart = timedelta(hours=9, minutes=5)
    for pkg in truck2.packages:
        pkg = hash_table.lookup(pkg)
        pkg.departure_time = truck2.depart
        pkg.delivery_time = truck2.depart + pkg.base_time

    # return trip for truck2
    truck2_return_trip = calculate_distance(ds, address_lookup(ds, hub), address_lookup(ds, truck2.cur_addr))
    truck2.mileage_sum += truck2_return_trip
    truck2.mileage_sum = round(truck2.mileage_sum, 1) 
    truck2.time += timedelta(hours=truck2_return_trip / truck2.avg_speed)
    
    # truck3 has the package(9) with the wrong address, set depart time to 10:20
    # truck3 packages [2, 4, 5, 7, 8, 9, 10, 11, 17, 18, 21, 23, 33]
    truck3.depart = timedelta(hours=10, minutes=20)
    for pkg in truck3.packages:
        pkg = hash_table.lookup(pkg)
        pkg.departure_time = truck3.depart
        pkg.delivery_time = truck3.depart + pkg.base_time
        
    # return trip for truck3
    truck3_return_trip = calculate_distance(ds, address_lookup(ds, hub), address_lookup(ds, truck3.cur_addr))
    truck3.mileage_sum += truck3_return_trip
    truck3.mileage_sum = round(truck3.mileage_sum, 1)
    truck3.time += timedelta(hours=truck3_return_trip / truck3.avg_speed)

# set the package status based on the time, adjusting for the delayed packages and wrong address package
# space O(1)
# time O(N), simple linear data assignment
def check_status(time: timedelta, hash_table: HashTable, truck1: TruckObject, truck2: TruckObject, truck3: TruckObject):
    print(f"Checking package status at {time}")
    print("\n")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRUCK 1 INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(f"Truck 1 Departure time: {truck1.depart}")
    for pkg_id in truck1.packages:
        pkg = hash_table.lookup(pkg_id)
        pkg.update_status(time)
        pkg.print_package_info_brief(time)
        
    print("\n")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRUCK 2 INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(f"Truck 2 Departure time: {truck2.depart}")
    for pkg_id in truck2.packages:
        pkg = hash_table.lookup(pkg_id)
        # truck 2 has the delayed packages # 6, 25, 28, 32, manually set the status
        if pkg_id in [6, 25, 28, 32]:
            if time < truck2.depart:
                pkg.status = "Delayed"
            else:
                pkg.update_status(time)
        else:
            pkg.update_status(time)
        pkg.print_package_info_brief(time)
        
    print("\n")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRUCK 3 INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(f"Truck 3 Departure time: {truck3.depart}")
    for pkg_id in truck3.packages:
        pkg = hash_table.lookup(pkg_id)
        # truck 3 has the wrong address package # 9, manually set the address ATTRIBUTE, the CSV contains the correct address
        if pkg_id == 9:
            if time < truck3.depart:
                pkg.address = "300 State St"
            else:
                pkg.address = "410 S State St"
        pkg.update_status(time)
        pkg.print_package_info_brief(time)

def main():

    # instantiate a data series object and call methods to populate the tables
    ds = DataSeries()
    ds.create_distance_table()
    ds.create_package_table()
    ds.create_address_table()
    
    # instantiate a hash table and populate it with PackageObjects
    hash_table = HashTable()
    load_hash_table(ds, hash_table)
    
    # assign packages to trucks
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
    
    # call the nearest neighbor alorithm for all trucks to determine the route and set baseline times
    for truck in [truck1, truck2, truck3]:
        negotiate_route(truck, hash_table, ds)
        
    # set the delivery times
    set_delivery_time(ds, hash_table, truck1, truck2, truck3, hub)
    
    print()    
    def user_menu(option):
        # check utility input as int
        if option.isdigit() and int(option) in range(8):
            option = int(option)
        if option == 1:
            ds.print_distance_table()
            print()
        elif option == 2:
            ds.print_package_table()
            print()
        elif option == 3:
            ds.print_address_table()
            print()
        elif option == 4:
            truck1.print_truck_info()
            truck2.print_truck_info()
            truck3.print_truck_info()
            print()
        elif option == 5:
            pkg_id = input("Enter package ID to lookup: ")
            if pkg_id.isdigit():
                pkg_id = int(pkg_id)
                pkg = hash_table.lookup(pkg_id)
                if pkg is not None:
                    pkg.update_status(pkg.delivery_time) # set the status to delivered for the purpose of the lookup
                    pkg.print_package_info()
                else:
                    print(f"Package ID {pkg_id} not found.")
            else:
                print("Invalid package ID. Please enter a number.")
            print()
        elif option == 6:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MILEAGE CALCULATIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            total_mileage = truck1.mileage_sum + truck2.mileage_sum + truck3.mileage_sum
            print(f"Truck 1 mileage including return trip ({truck1.cur_addr} -> {hub}): {truck1.mileage_sum} miles")
            print(f"Truck 2 mileage including return trip ({truck2.cur_addr} -> {hub}): {truck2.mileage_sum} miles")
            print(f"Truck 3 mileage including return trip ({truck3.cur_addr} -> {hub}): {truck3.mileage_sum} miles")
            print()
            print(f"Total mileage for all trucks: {total_mileage} miles")
            print()
        elif option == 7:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PACKAGE DEADLINE INFORMATION %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Packages with deadlines:")
            for pkg_id in truck1.packages + truck2.packages + truck3.packages:
                pkg = hash_table.lookup(pkg_id)
                note = pkg.note if pkg.note else "No Note"
                print(f"Package ID: {pkg.id}, Deadline: {pkg.deadline}, Address: {pkg.address}, Note: {note}")
        elif option == 0:
            print("Exiting the program. Goodbye!")
            sys.exit(0)
        else:
            # validate time input with regex
            pattern = r'^(0?[1-9]|1[0-2]):([0-5][0-9])(AM|PM|am|pm)$' # matches 09:00AM, 9:00PM, 12:30am, etc
            if re.match(pattern, option):
                groups = re.match(pattern, option).groups()
                input_time = timedelta(hours=int(groups[0]), minutes=int(groups[1]))
                # if in the afernoon, time = time + 12
                if groups[2].lower() == 'pm' and int(groups[0]) != 12:
                    input_time += timedelta(hours=12)
                check_status(input_time, hash_table, truck1, truck2, truck3)
            else:
                print("Invalid option. Please try again.")
                print()
            # print_menu()
            
    def print_menu():
        print("\n")
        print("Welcome to the WGUPS package lookup!")
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% UTILITIES %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Use the following utilities to view package and truck information:")
        print("1. View Distance Table")
        print("2. View Package Table")
        print("3. View Address Table")
        print("4. View Truck Information")
        print("5. View Package by ID")
        print("6. View total total mileage for all trucks")
        print("7. View Package Deadline Information")
        print("0. Exit the program")
        print()
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PACKAGE LOOKUP PORTAL %%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Enter a time in as HH:MM(AM/PM) to view all package information")

    
    # start main cli functionality 
    while True:
        try:
            print_menu()
            option = input("User Input: ")
            if option == 0:
                print("Exiting the program. Goodbye!")
                break
            user_menu(option)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
    
if __name__ == "__main__":
    main()
    
    
    
    
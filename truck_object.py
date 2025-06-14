from datetime import time, timedelta

class TruckObject:
    def __init__(self, truck_num, payload_capacity, cur_addr, depart=timedelta(hours=0), packages=[], mileage_sum=0, avg_speed=18):
        self.truck_num = truck_num
        self.payload_capacity = payload_capacity
        self.cur_addr = cur_addr
        self.depart = depart
        self.packages = packages
        self.mileage_sum = mileage_sum
        self.avg_speed = avg_speed
        
        # attribute for current time
        self.time = depart
        
    def print_truck_info(self):
        banner = "%" * 20 
        print(f"{banner} TRUCK {self.truck_num} INFO {banner}")
        print(f"Payload Capacity: {self.payload_capacity} lbs")
        print(f"Current Address: {self.cur_addr}")
        print(f"Average Speed: {self.avg_speed} mph")
        print("Packages on Truck:")
        for pkg in self.packages:
            print(f" - Package ID: {pkg}")
        print(banner * 2)
        print("\n")
    
    def add_packages(self, pkg_list):
        for pkg in pkg_list:
            if pkg not in self.packages:
                self.packages.append(pkg)
    
    def clear_packages(self):
        self.packages = []
    
    
      
        
    
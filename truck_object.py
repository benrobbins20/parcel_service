from datetime import time, timedelta

class TruckObject:
    def __init__(self, truck_num, cur_addr, depart=timedelta(hours=0), packages=[], mileage_sum=0, avg_speed=18):
        self.truck_num = truck_num
        self.cur_addr = cur_addr
        self.depart = depart
        self.packages = packages
        self.mileage_sum = mileage_sum
        self.avg_speed = avg_speed
        
        # attribute for truck departure time
        self.time = depart
        
    @property
    def mileage(self):
        return round(self.mileage_sum, 1)
    
    def print_truck_info(self):
        banner = "%" * 20 
        print(f"{banner} TRUCK {self.truck_num} INFO {banner}")
        print(f"Average Speed: {self.avg_speed} mph")
        print(f"Packages on Truck: {self.packages}")
        print(f"Departure: {self.depart} Delivery: {self.time} Return: {self.time + self.depart}")
        print(f"Total Mileage: {self.mileage_sum} miles")
        print(banner * 2)
        print("\n")
    
    def add_packages(self, pkg_list):
        for pkg in pkg_list:
            if pkg not in self.packages:
                self.packages.append(pkg)
    
    def clear_packages(self):
        self.packages = []
        
      
        
    
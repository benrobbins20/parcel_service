class PackageObject:
    def __init__(self, id, address, city, state, zip_code, deadline, weight, note, status, truck_num=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.truck_num = truck_num
        
        # add additional attributes for dpeature and delivery times
        self.base_time = None # this is a general baseline 
        self.departure_time = None
        self.delivery_time = None
        
        
    def print_package_info(self):
        banner = "%" * 20
        print(f"{banner} PACKAGE {self.id} INFO {banner}")
        print(f"Address: {self.address}, {self.city}, {self.state} {self.zip_code}")
        print(f"Deadline: {self.deadline}")
        print(f"Weight: {self.weight} lbs")
        print(f"Note: {self.note}")
        print(f"Status: {self.status}")
        print(f"Base Time: {self.base_time}")
        print(f"Departure Time: {self.departure_time}")
        print(f"Delivery Time: {self.delivery_time}")
        print(banner * 2)
        print("\n")
        
        
    def update_truck_num(self, truck_num):
        self.truck_num = truck_num
        
    def update_status(self, time):
        if time < self.departure_time:
            self.status = "At hub"
        elif (self.departure_time <= time < self.delivery_time):
            self.status = "In Transit"
        elif time >= self.delivery_time:
            self.status = "Delivery"
        else:
            self.status = None
        
        
    
    
        
    
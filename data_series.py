import csv
# i used openpyxl to create an address lookup
# import openpyxl, numpy as np, re


class DataSeries:
    # load the xl files into a shared np object
    def __init__(self):
        # data objects that will be used
        self.distance_table = None
        self.package_file = None
        self.address_file = None
        
        # csv files used
        self.dt_file = "distance_table.csv"
        self.pkg_file = "package_file.csv"
        # self.dt_file_xl = "Distance_Table.xlsx"
        
    def create_distance_table(self):
        data = [] 
        # utf-8-sig strips Byte Order Mark from Excel csv
        with open(self.dt_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                # avoids long list of empty cells (,,,,,,,)
                data.append([float(cell) if cell else None for cell in row])
        self.distance_table = data
    
    # print the distance space delimited without Nones
    def print_distance_table(self):
        for row in self.distance_table:
            print("|".join(str(cell) if cell is not None else '' for cell in row))
                
            
    def create_package_table(self):
        data = []
        with open(self.pkg_file, 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 7 and row[7] == '':
                    row[7] = None
                data.append(row)
            # quicker way is no loop, reader object converted to a list
            # data = list(reader)
            
        self.package_file = data

    def print_package_table(self):
        for row in self.package_file:
            #print(" : ".join(row))  # join the elements with colons
            print(row)
            
            
    # def generate_address_lookup(self):
    #     # single column A9:A35 of the distance table
    #     wb = openpyxl.load_workbook(self.dt_file_xl)
    #     ws = wb.active
    #     data = []
    #     index = 0
        
    #     # loop through cells in the single column, split lines of address, assign an index, save the shared np array
    #     for row in ws['A9':'A35']:
    #         for cell in row:
    #             lines = cell.value.split('\n')
    #             location = lines[0].strip()
    #             address = lines[1].strip()
    #             address = re.sub(r'[^A-Za-z0-9\s]', '', address) # strip non-alpha
    #             data.append([index, location, address])
    #             index += 1
    #     with open('address_file.csv', 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerows(data)
            
    
    def create_address_table(self):
        data = []
        with open('address_file.csv', 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.reader(file)
            # no loop, reader just reads each line and converts to a list
            data = list(reader)
        self.address_file = data
        
    def print_address_table(self):
        for row in self.address_file:
            # join the elements with colons
            print(" : ".join(row))
                
            
# local testing
if __name__ == "__main__":
    ds = DataSeries()
    ds.create_distance_table()
    # ds.print_distance_table()
    ds.create_package_table()
    # ds.print_package_table()
    ds.create_address_table()
    # ds.print_address_table()
    
    
    print(ds.distance_table[1][0])

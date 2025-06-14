from package_object import PackageObject

class HashTable:
    def __init__(self, buckets=50):
        # hashing algorithm will place PackageObjects into a lookup table
        # initially [None, None, None, ...] len=buckets, on object insert -> [[Object1, Object2], None,...]
        self.table = [None] * buckets
    
    # length of table is 50 buckets, the base project only has 40 packages with sequential id's 1-40
    # there will be no collisions for the base project, but retain the capability for bucket chaining
    def key(self, pkg_id):
        return int(pkg_id) % len(self.table)
        
    def insert(self,pkg_object):
        if not isinstance(pkg_object, PackageObject):
            raise TypeError("parameter must be of type PackageObject")
        
        # the hashmap inserts using the hash index, the entry is [id, PackageObject]
        index = self.key(pkg_object.id)
        entry = [pkg_object.id, pkg_object]
        
        # if the bucket is empty, insert [entry]
        if self.table[index] is None:
            self.table[index] = list([entry])
        # if the bucket is not empty, append the entry to the bucket
        else:
            self.table[index].append(entry)
            
        return
    
    def update(self, pkg_object):
        # exit if wrong type 
        if not isinstance(pkg_object, PackageObject):
            raise TypeError("parameter must be of type PackageObject")
        index = self.key(pkg_object.id)
        bucket = self.table[index]
        
        # exit if bucket is empty
        if bucket is None:
            raise KeyError(f"Package with ID {pkg_object.id} not found in the table.")
        
        # proceed with update
        # Note: the updated PackageObject already has updated fields, this adds it to the table
        else:
            for entry in bucket: # entry = [id, PackageObject]
                if entry[0] == pkg_object.id:
                    entry[1] = pkg_object
                    
        return
        
    # only need the id, the PackageObject is returned
    def lookup(self, id) -> PackageObject:
        index = self.key(id)
        bucket = self.table[index]
        if bucket is None:
            raise KeyError(f"Package with ID {id} not found in the table.")
        else:
            for entry in bucket:
                if entry[0] == id:
                    if isinstance(entry[1], PackageObject):
                        return entry[1]
                    
    # delete by id
    def delete(self, id):
        index = self.key(id)
        bucket = self.table[index]
        if bucket is None:
            raise KeyError(f"package with ID {id} not found in the table.")
        
        # proceed with delete
        for entry in bucket:
            if entry[0] == id:
                bucket.remove(entry) # .remove() will delete exact [id, PackageObject] entry
                return
    
    # must skip None rows and None buckets otherwise operations will fault out (shouldn't have None bucket in theory)
    def print_table(self):
        for row in self.table:
            if row is None:
                continue
            for bucket in row:
                if bucket is None:
                    continue
                print(
                    f"Key: {bucket[0]}, "
                    f"id: {bucket[1].id}, "
                    f"address: {bucket[1].address}, "
                    f"city: {bucket[1].city}, "
                    f"state: {bucket[1].state}, "
                    f"zip: {bucket[1].zip_code}, "
                    f"deadline: {bucket[1].deadline}, "
                    f"weight: {bucket[1].weight}, "
                    f"note: {bucket[1].note}, "
                    f"status: {bucket[1].status} "
                    f"truck_num: {bucket[1].truck_num}"
                )

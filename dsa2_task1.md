## Ben Robbins SID: 011007860
# C950 - Data Structures and Algorithms 2 Task 1

### A: Name the Self-Adjusting algorithm used to neotiate the package delivery route
#### The parcel service will leverage the use of the nearest neighbor algorithm, otherwise known the the Traveling Salesman Problem (TSP). It is a classic algorithm used in computer science to sort destinations by nearest distance first, which produces a much simpler approach for an algorithm in use by a package delivery service.

### B: Name the self-adjusting data structure used to store package information

#### The self-adjusting storage structure to be used is a chained hashmap. This is simple to implement as the "bucket" for each package contains an array of all the packages to resolve to that key. This allows for quick access as well as expandability if a hash collision were to occur. The actual item stored in the bucket is a python PackageObject, which is defined in code to allow attributes. This is useful because only the package ID needs to be used setup the nearest neighbor alorithm, aided by a lookup function that is used to retrieve the object from the hashmap.

### C1: Describe algorithm logic using pseudocode

#### The "negotiate_route" function will take the initial unsorted list of packages and then sort them in order of nearest next package in relation to the vehicle's current location.
```
fn negotiate_route()
    truck_packages = initial list of unsorted package IDs
    left_to_search = temporary copy of unsorted_packages 
    current_location = delivery hub

    # iterate over the unsorted packages and add to temporary list
    for package_id in truck_packages
        package = package_lookup(package_id)
        left_to_search.add(package)
    truck_packages.clear()  # clear the original list allow adding packages in order of nearest neighbor
    # O(N) linear time complexity to iterate over one list and add packages to another list

    # do the nearest neighbor algorithm
    while left_to_search is not empty
        nearest_package = None
        nearest_distance = infinity
        for package in left_to_search
            distance = calculate_distance(current_location, package.location)
            # continually set the nearest package 
            # Note: some locations may have the same address! Thus <= is used
            if distance <= nearest_distance
                nearest_distance = distance
                nearest_package = package
        
        # decrement the nearest package to exhaust the search
        left_to_search.remove(nearest_package)
        # add nearest package
        truck_packages.add(nearest_package) 
        # advance the truck's current location
        current_location = nearest_package.location
        # repeat while loop, overwrites nearest package/distance
```
###  Summary of Nearest Neighbor / TSP runtime complexity
#### The runtime complexity of the nearest neighbor alogirithm follows the pattern (N) + (N-1) + (N-2) ... N times, which resolves to the arithmatic sequence $N(N-1)/2$. The total algorithm equals $O(N) + O(N^2)$, the larger term dominates the runtime complexity, so the overall complexity is $O(N^2)$.

#### The hashmap leverages "chaining" to resolve collisions. The hashmap is designed with ample room to handle 40 packages with a default size of 50, so no collisions are expected. However, for expandability, each bucket stores an array of PackageObjects, identified by a unique package ID. While the insert() function runs at O(1), the lookup() function has the possilibilty of running at O(K) due to chaining 
```
fn lookup(id)
    key = id % hash table size
    bucket = hash_table[key]
    for package in bucket
        if package.id == id
            # found, worst case O(K), where K = number of packages in bucket
            return package 
    return None # package not found

```
### Summary of Hashmap lookup() runtime complexity
#### The lookup function has a worst case runtime complexity of O(K) from iterating over bucket items. However, in practice, the average case is O(1) because the hashmap is designed to have no collisions with unique ID's for 50 packages. 

### C2: Hardware and Software Specifications
#### Python 3.13.3 running on MacOS 15
### C3: 
#### Nearest Neighbor Algorithm: O(N^2)
#### Hashmap lookup: O(K) 
### C4:
#### Both the nearest neighbor algorithm and the hashmap lookup function are self-adjusting algorithms. Packages can be added to the algorithm with the ability to handle collisions in the hashmap as well as extending and negotiating the route due to the nature of the nearest neighbor algorithm. The order of delivery will always be adjusted based on the current location of the vehicle and the remaining packages to deliver.
### C5: Maintenance and Efficiency
#### Once the algorithm is in place, very little maintenance is required. Simply adding packages to the truck will automatically adjust the route as the nearest drop off location is recalculated. The algorithm is modular and object based, therefore it can easily be integrated into a larger system if needed. 
### C6: Weighing the Pros and Cons of the Self-Adjusting Algorithm
#### The nearest neighbor algorithm is a simple and effective way to sort packages by distance. It is easy to implement and understand, making it a good choice for a package delivery service. However, it does not always produce the optimal route, and it can be slow for large numbers of packages. Nearest neighbor is a greedy algorithm, meaning it very much considers only the next step, rather than a holistic view of the entire route. A shortest path algorithm such as Dijkstra's or 'A-Star' would be more efficient for larger numbers of packages. Overall, nearest neighbor is a good choice for this delivery scheme and satifies the delivery requirements for WGUPS.
#### The hashmap lookup function is also simple and effective. With an appropriately sized hashmap, the lookup function resolves a key/index that exists in the map, and only finds a bucket with 1 item, creating a very fast retrieval efficiency. It can be slow if there are many collisions as the lookup function may need to iterate over ALL of the items in the bucket to find a match.
### C7: Hashmap Key
#### The unique package ID is the obvious choice for a lookup key. For hashmap of size 50, ID's 1 and 51 can resolve to the same bucket, as the hashing function is simply a modulus of the ID by the size of the hashmap. eg. $51 \bmod 50 = 1$

## Ben Robbins SID: 011007860
# C950 - Data Structures and Algorithms 2: Task 1

### A: Name the Self-Adjusting algorithm used to neotiate the package delivery route
#### The parcel service will leverage the use of the nearest neighbor algorithm, otherwise known as the Traveling Salesman Problem (TSP). It is a classic algorithm used in computer science to sort destinations by nearest distance first, which produces a much simpler approach for an algorithm in use by a package delivery service.

### B: Name the self-adjusting data structure used to store package information

#### The self-adjusting storage structure to be used is a chained hash map. This is simple to implement as the "bucket" for each package contains an array of all the packages that resolve to that key. This allows for quick access as well as expandability if a hash collision were to occur. The actual item stored in the bucket is a python PackageObject, which is defined in code to allow attributes. This is useful because only the package ID needs to be used to implement the nearest neighbor alorithm, aided by a lookup function that is used to retrieve the object from the hash map.

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
    truck_packages.clear()  # clear the original list to allow adding packages in order of nearest neighbor
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
#### The runtime complexity of the nearest neighbor algorithm follows the pattern (N) + (N-1) + (N-2) ... N times, which resolves to the arithmetic sequence $N(N-1)/2$. The total algorithm equals $O(N) + O(N^2)$, the larger term dominates the runtime complexity, so the overall complexity is $O(N^2)$.

#### The hash map leverages "chaining" to resolve collisions. The hash map is designed with ample room to handle 40 packages with a default size of 50, so no collisions are expected. However, for expandability, each bucket stores an array of PackageObjects, identified by a unique package ID. While the insert() function runs at O(1), the lookup() function has the possibility of running at O(K) due to chaining 
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
### Summary of hash map lookup() runtime complexity
#### The lookup function has a worst case runtime complexity of O(K) from iterating over bucket items. However, in practice, the average case is O(1) because the hash map is designed to have no collisions with unique ID's for 50 packages. 

### C2: Hardware and Software Specifications
#### Python Version: Python 3.13.3
#### Hardware Overview

- **Model Name:** MacBook Pro
- **Model Identifier:** MacBookPro18,1
- **Model Number:** Z14W00105LL/A
- **Chip:** Apple M1 Pro
- **Total Number of Cores:** 10 (8 performance, 2 efficiency)
- **Memory:** 32 GB
- **System Firmware Version:** 11881.121.1
- **OS Loader Version:** 11881.121.1

### C3: Detailed runtime complexity
- **Hash map insert:** O(1) time and space complexity, the function itself does not contain and expandable data structure that grows with input, the insert method simple places item in chain of items which is a constant time operation.
- **Hash map update/lookup:** Due to chaining, the methods operate with an O(N) time complexity. In the astomically rare scenario that all packages resolve to the same bucket index, looping through all items would produce worst case scenario linear runtime complexity. (eg. 1, 51, 101, 151, etc) 
- **Data Series creation:** O(N), all items take a list of N items in the included tables and then creates a new python 2D array of N items.
- **Truck add_packages:** O(N), when the truck classes are instantiated, the add_packages method takes a list of N items and then adds them to the truck's package list.
- **Nearest Neighbor Algorithm:** O(N^2), the algorithm iterates over the list of packages N times, and for each package, it calculates the distance to every other package, resulting in a quadratic time complexity. As packages are removed and added to local arrays for sorting, space cmplexity remains at O(N). 
- **Total runtime complexity of the program:** The dominating factor is the nearest neighbor sorting algorithm. All of the additional methods produce no compounding data structures that grow with input, therefore the holitic space complexity remains O(N) and the overall runtime complexity is O(N^2).
#### Nearest Neighbor Algorithm: O(N^2)
#### hash map lookup: O(K) -> O(N)

### C4:
#### Both the nearest neighbor algorithm and the hash map lookup function are self-adjusting algorithms. Packages can be added to the algorithm with the ability to handle collisions in the hash map as well as extending and negotiating the route due to the nature of the nearest neighbor algorithm. The order of delivery will always be adjusted based on the current location of the vehicle and the remaining packages left to deliver.
### C5: Maintenance and Efficiency
#### Once the algorithm is in place, very little maintenance is required. Simply adding packages to the truck will automatically adjust the route as the nearest drop off location is recalculated. The algorithm is modular and object-oriented, therefore it can easily be integrated into a larger system if needed. 
### C6: Weighing the Pros and Cons of the Self-Adjusting Algorithm
#### The nearest neighbor algorithm is a simple and effective way to sort packages by distance. It is easy to implement and understand, making it a good choice for a package delivery service. However, it does not always produce the optimal route, and it can be slow for large numbers of packages. Nearest neighbor is a greedy algorithm, meaning it only considers the next step, rather than a holistic view of the entire route. A shortest path algorithm such as Dijkstra's or 'A-Star' would be more efficient for larger numbers of packages. Overall, nearest neighbor is a good choice for this delivery scheme and satifies the delivery requirements for WGUPS.
#### The hash map lookup function is also simple and effective. With an appropriately sized hash map, the lookup function resolves a key/index that exists in the map, and only finds a bucket with 1 item, creating a very fast retrieval efficiency. It can be slow if there are many collisions as the lookup function may need to iterate over ALL of the items in the bucket to find a match.
### C7: hash map Key
#### The unique package ID is the obvious choice for a lookup key. For a hash map of size 50, ID's 1 and 51 can resolve to the same bucket, as the hashing function is simply a modulus of the ID by the size of the hash map. eg. $51 \bmod 50 = 1$
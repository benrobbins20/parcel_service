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
        # (N) + (N-1) + (N-2) ... N times
```
#### The hashmap lookup function leverages "chaining" to resolve collisions. The program is designed with ample room to handle 40 packages, so no collisions are expected. However, for expandability, each bucket stores an array of PackageObjects, identified by a unique package ID.
```

```



latex

The formula is $n(n - 1)/2$.

$x^2 + y^2 = z^2$
$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$
$$
\sqrt{16} = 4
$$
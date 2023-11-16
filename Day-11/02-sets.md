# Sets and Set Operations

#### Overview:
A set in Python is an unordered collection of unique elements. It is useful for mathematical operations like union, intersection, and difference.

#### Creating a Set:
```python
my_set = {1, 2, 3, 4, 5}
```

#### Adding and Removing Elements:
```python
my_set.add(6)  # Adding an element
my_set.remove(3)  # Removing an element
```

#### Set Operations:
```python
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

union_set = set1.union(set2)  # Union of sets
intersection_set = set1.intersection(set2)  # Intersection of sets
difference_set = set1.difference(set2)  # Difference of sets
```

#### Subset and Superset:
```python
is_subset = set1.issubset(set2)  # Checking if set1 is a subset of set2
is_superset = set1.issuperset(set2)  # Checking if set1 is a superset of set2
```

### Practice Exercises and Examples

#### Example: Managing a Dictionary of Server Configurations and Optimizing Retrieval

##### Scenario:
Suppose you are managing server configurations using a dictionary.

```python
server_config = {
    'server1': {'ip': '192.168.1.1', 'port': 8080, 'status': 'active'},
    'server2': {'ip': '192.168.1.2', 'port': 8000, 'status': 'inactive'},
    'server3': {'ip': '192.168.1.3', 'port': 9000, 'status': 'active'}
}
```

##### Function for Retrieval:
```python
def get_server_status(server_name):
    return server_config.get(server_name, {}).get('status', 'Server not found')
```

##### Example Usage:
```python
server_name = 'server2'
status = get_server_status(server_name)
print(f"{server_name} status: {status}")
```


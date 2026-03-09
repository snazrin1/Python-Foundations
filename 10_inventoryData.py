# Create a list
inventory = ["Laptop", "Monitor", "Keyboard"]

# Accessing items
print(f"Primary item: {inventory[0]}") # Laptop

# Modifying the list
inventory.append("Mouse")      # Adds to the end
inventory.insert(1, "Webcam")  # Adds at index 1
inventory.pop(0)               # Removes "Laptop"

print(f"Current Stock: {inventory}")
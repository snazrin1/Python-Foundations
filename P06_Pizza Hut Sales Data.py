# --- P08_Pizza_Sales.py ---

# 1. Data Setup
toppings = ["pepperoni", "pineapple", "cheese", "sausage", "olives", "anchovies", "mushrooms"]
prices = [2, 6, 1, 3, 2, 7, 2]

# 2. Basic Analysis
num_pizzas = len(toppings)
print(f"We sell {num_pizzas} different kinds of pizza!")

# 3. Pairing Data with zip()
# We put price first so we can sort by price automatically
pizzas = list(zip(prices, toppings))
print("\nUnsorted Pizzas (Price, Topping):")
print(pizzas)

# 4. Sorting and Slicing
pizzas.sort() # Sorts from cheapest to most expensive
print("\nSorted Menu:")
print(pizzas)

cheapest_pizza = pizzas[0]
priciest_pizza = pizzas[-1] # Gets the last item

# 5. The Three Cheapest
three_cheapest = pizzas[:3] # Slices from index 0 to 2

print(f"\nCheapest option: {cheapest_pizza}")
print(f"Priciest option: {priciest_pizza}")
print(f"Budget Options: {three_cheapest}")
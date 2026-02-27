# --- STEP 1: THE CATALOG ---
# We store the names and prices in variables before they are used.
lovely_loveseat_description = "Lovely Loveseat. Tufted polyester blend on wood. 32 inches high x 40 inches wide x 30 inches deep. Red or white."
lovely_loveseat_price = 254.00

stylish_settee_description = "Stylish Settee. Faux leather on birch. 29.50 inches high x 54.75 inches wide x 28 inches deep. Black."
stylish_settee_price = 180.50

luxurious_lamp_description = "Luxurious Lamp. Glass and iron. 36 inches tall. Brown with cream shade."
luxurious_lamp_price = 52.15

# We store the tax rate as a float (8.8%)
sales_tax = 0.088

# --- STEP 2: INITIALIZE THE CUSTOMER ---
# Every customer starts with 0 dollars and no items.
customer_one_total = 0
customer_one_itemization = ""

# --- STEP 3: PROCESSING THE PURCHASE ---
# The customer decides to buy the Loveseat
customer_one_total += lovely_loveseat_price
customer_one_itemization += lovely_loveseat_description + "\n"

# The customer also decides to buy the Lamp
customer_one_total += luxurious_lamp_price
customer_one_itemization += luxurious_lamp_description + "\n"

# --- STEP 4: CALCULATING TAX ---
# Calculate the tax based on the subtotal
customer_one_tax = customer_one_total * sales_tax

# Add the tax to the running total
customer_one_total += customer_one_tax

# --- STEP 5: PRINT THE RECEIPT ---
# We use f-strings for professional currency formatting
print("\n" + "*"*30)
print("     OFFICIAL RECEIPT")
print("*"*30)

print("\nCUSTOMER ITEMS:")
print(customer_one_itemization)

print("-" * 30)
print(f"SUBTOTAL + TAX: ${customer_one_total:.2f}")
print("*"*30)
print("   THANK YOU FOR SHOPPING!")
print("*"*30)

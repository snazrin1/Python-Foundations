import random

# --- STEP 1: THE GENERATOR ---
# We pick a random number between 1 and 8
fortune_number = random.randint(1, 8)
lucky_number = random.randint(1, 100)
fortune_text = ""

# --- STEP 2: THE WISDOM LOGIC ---
if fortune_number == 1:
    fortune_text = "Great Success ahead!"
elif fortune_number == 2:
    fortune_text = "404: Luck not found."
elif fortune_number == 3:
    fortune_text = "A surprise awaits!"
elif fortune_number == 4:
    fortune_text = "Be prepared for challenges"
elif fortune_number == 5:
    fortune_text = "Today is your lucky day!"
elif fortune_number == 6:
    fortune_text = "You love peace"
elif fortune_number == 7:
    fortune_text = "Eat chocolate to have a sweeter life"
elif fortune_number == 8:
    fortune_text = "An exciting opportunity is just around the corner."
else:
    fortune_text = "Error: The cookie is empty!"

# --- STEP 3: THE REVEAL ---
print("CRACK! Your Fortune Cookie says:")
print(f"\"{fortune_text}\"")
print(f"Your Lucky Number for today is: {lucky_number}")
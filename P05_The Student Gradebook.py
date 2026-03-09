# --- P07_Gradebook.py ---

# 1. Past Data
last_semester_gradebook = [["politics", 80], ["latin", 96], ["dance", 97], ["architecture", 65]]

# 2. Current Subjects & Grades
subjects = ["physics", "calculus", "poetry", "history"]
grades = [98, 97, 85, 88]

# 3. Manually creating a 2D List
gradebook = [
    ["physics", 98], 
    ["calculus", 97], 
    ["poetry", 85], 
    ["history", 88]
]

print("Initial Gradebook:")
print(gradebook)

# 4. Adding new subjects using .append()
gradebook.append(["computer science", 100])
gradebook.append(["visual arts", 93])

# 5. Modifying: Switching Poetry to "Pass" (Removing the grade)
# We access the poetry sublist and remove the 85
gradebook[2].remove(85)
gradebook[2].append("Pass")

# 6. Combining Semesters
full_gradebook = last_semester_gradebook + gradebook

print("\nFull Academic Record:")
print(full_gradebook)
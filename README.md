# Python-Foundations

This is my professional coding journal for the 2026 After-School Coding Program.

# Lesson 1: Hello World
- Created a GitHub account.
- Launched a cloud-based development environment using "GitHub Codespaces".
- Wrote and executed my first Python script: `myfirstcodehello.py`.

#Tools Used
* Python 3
* VS Code (via Codespaces)
* Git for Version Control

# Lesson 2 : Variables, Input, F-String
- Learned how to use input() and variables
- Created Story Generator mini project

# Lesson 3 : Numbers and Operations
- Learned int, float, operators
- Created simple calculator mini project

# Project 1 : ASCII Art
Skill Learned: Multi-line strings and terminal formatting.
Challenge: Creating a visual "Welcome" sign for my repository.

# Project 2 : Furniture Store

### Project Overview
Developed a terminal-based Point of Sale (POS) system for a boutique furniture store. The script manages an inventory catalog and processes customer transactions.

### Core Skills
*  Tracking a running subtotal and item list.
*  Using `+=` to update numeric and string data.
*  Applying an 8.8% sales tax to a finalized subtotal.
*  Using "f-strings" for two-decimal currency precision.

### Execution Logic
1.  Stored product descriptions and prices in variables.
2.  Updated the total and itemization string as items were "purchased".
3.  Calculated and added tax to the final bill.
4.  Generated a clean, formatted receipt for the user.

# Lesson 4 : Conditional Logic (If Else and Elif)
Mastered the use of "Conditional Logic" concept using `if` and `else` and `elif`.
Created "The Secret Password Vault" mini project for If Else
Created "The Movie Ticket Grader" mini project for Elif

# Project 3 : Fortune Cookie Generator

### "Project Overview"
Developed a restaurant-style fortune cookie generator that provides randomized "message" and lucky numbers to users.

### Technical Skills Applied
* Integrated the `random` module to enable non-linear program behavior.
* Used extensive `if/elif/else` logic to map numeric values to string-based output.
*  Combined randomized text and integers into a single user-friendly terminal report.

### The Logic Flow
1. The program generates a random integer.
2. The integer is checked against a list of 8 possible fortunes.
3. The program prints the selected fortune and a secondary random "lucky number".

# Lesson 5 : Iterative Logic (Loops)
Mastered the use of `while` and `for` loops. 
Created "Rocket Launcher " mini project for while loop
Created "Task Automator " mini project for for loop

# Lesson 6 : Functions
Mastered to create reusable blocks of code using `def`. 
Created "Welcome Greeter" mini project 

# Project 4 : Adventure Game

### Project Overview
Engineered a non-linear, text-based adventure game utilizing modular programming. This project manages complex user-driven branching paths.

### Technical Skills Applied
* Organized game logic into reusable blocks, making the code easier to debug and expand.
* Used function returns to communicate state changes to the main game engine.
* Implemented a `while` loop to maintain an active program state until a "win" or "loss" condition is met.
* Developed multiple "if/else" decision trees to provide different outcomes based on user input.

### Execution Logic
1. Each room is defined as a unique function.
2. A central `while` loop acts as the engine, directing the player to the correct function based on the current "room" variable.
3. The loop breaks only when a terminal state ("end") is reached.

# Lesson 7 : Lists & 2D Arrays
Mastered storing and manipulating ordered collections of data.
Created "Inventory Manager" and "Gradebook" mini projects.

# Project 5 : The Academic Gradebook
Project Overview: Developed a multi-semester tracking system using two-dimensional lists.
Technical Skills: * Applied 2D list management to store Subjects and Grades together.
Used .append() and .remove() for real-time data updates.
Merged semesters using list concatenation (+).

# Project 6 : Pizza Hut Sales Engine
Project Overview: Built a sales tool using data pairing and sorting for business insights.
Technical Skills: * Used zip() to lock Toppings and Prices together.
Sorted paired data to rank items by price.
Utilized slicing ([:]) to extract budget-friendly options.

# Lesson 8 : Dictionaries
Mastered using Dictionary Comprehension to build datasets efficiently.
Learned to store Lists inside Dictionaries to manage complex relationships.

# Project 9 : Scrabble Point Tracker
Project Overview: Built a scoring engine that maps letters to points and calculates totals for multiple players.
Technical Skills: * Used {key:value for key, value in zip()} for automated dictionary creation.
Created a nested loop to calculate scores across a dictionary of word lists.
Developed a robust score_word() function with error handling for missing keys.

### Execution Logic
A master letter_to_points dictionary is created by zipping alphabets with their point values.
The score_word() function iterates through any string and sums the points based on the master dictionary.
A player_to_words dictionary organizes gameplay by mapping names to a list of played words.
The engine loops through each player, calculates their total via the scoring function, and stores the final rankings in player_to_points.




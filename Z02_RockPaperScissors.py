import random

def play_game():
    options = ["rock", "paper", "scissors"]
    user_score = 0
    computer_score = 0

    print("--- 🎮 Welcome to the Python Battle Arena 🎮 ---")

    while True:
        user_choice = input("\nChoose Rock, Paper, or Scissors (or type 'quit' to exit): ").lower()

        if user_choice == 'quit':
            break

        if user_choice not in options:
            print("⚠️ Invalid choice! Try again.")
            continue

        # Computer makes a random choice
        computer_choice = random.choice(options)
        print(f"Computer chose: {computer_choice}")

        # Determine the Winner
        if user_choice == computer_choice:
            print("It's a TIE! 👔")
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            print("You WIN! 🎉")
            user_score += 1
        else:
            print("Computer Wins! 🤖")
            computer_score += 1

        print(f"Scoreboard -> You: {user_score} | Computer: {computer_score}")

    # Save the Final Score to a file (Lesson 9 Skill)
    with open("game_results.txt", "a") as f:
        f.write(f"Final Score - Player: {user_score}, Computer: {computer_score}\n")
    
    print("\nThanks for playing! Your results have been saved to game_results.txt.")

play_game()
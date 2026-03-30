import random

def start_cheat_game():
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    last_distance = None
    
    print("--- 🛡️ The ISA Secret Number: Admin Edition 🛡️ ---")
    print("I'm thinking of a number between 1 and 100.")

    while attempts < max_attempts:
        # Use input as a string first to check for the cheat code
        user_input = input(f"\nAttempt {attempts + 1}: Enter guess: ").lower().strip()

        # --- THE CHEAT CODE ---
        if user_input == "isa_admin":
            print(f"🤫 [SYSTEM OVERRIDE]: The secret number is {secret_number}")
            continue # Don't count this as an attempt!

        try:
            guess = int(user_input)
            attempts += 1
            
            current_distance = abs(secret_number - guess)

            if guess == secret_number:
                print(f"🎉 BINGO! You found it in {attempts} tries!")
                return

            # Warmer/Colder Hints
            if last_distance is not None:
                if current_distance < last_distance:
                    print("🔥 WARMER!")
                else:
                    print("❄️ COLDER!")
            
            # High/Low Clues
            if guess < secret_number:
                print("Hint: Higher")
            else:
                print("Hint: Lower")

            last_distance = current_distance

        except ValueError:
            print("⚠️ Enter a number or a valid command!")

    print(f"\n💀 GAME OVER. The number was {secret_number}.")

start_cheat_game()
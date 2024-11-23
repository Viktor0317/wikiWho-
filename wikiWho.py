
import wikipedia
import random
import wikiWho_data
from wikiWho_start_screen import start_screen
import textwrap
from colorama import Fore, Style, init
import re

# Initialize colorama
init(autoreset=True)


def press_button_to_start():
    """ Pause the program until the user presses any button. """
    print(f"\n               {Fore.LIGHTYELLOW_EX}Press [ENTER] to start the game...")
    input()


def get_clues(person_name):
    """
    Pull first four sentences from wiki-summary page, split them
    into separate strings and skip first sentence because of revealing data.
    """
    try:
        summary = wikipedia.summary(person_name, sentences=4)

        sentences = re.split(r'(?<=\.)\s+', summary.strip())

        sentences = sentences[1:]

        return clean_clues(sentences, person_name)
    except Exception:
        return [f"{Fore.RED}[An error occurred while fetching clues]"]


def clean_clues(clues, person_name):
    """
    Censor clues by replacing the name with '********'.
    """
    name_parts = person_name.split()
    pronouns = [
        "he", "she", "they", "him", "her", "his", "hers", "theirs",
        "He", "She", "They", "Him", "Her", "His", "Hers", "Theirs",
        "father", "Father", "Mother", "mother", "Brother", "brother",
        "Sister", "sister"
    ]

    pronoun_pattern = r'\b(' + '|'.join(pronouns) + r')\b'
    sanitized_clues = []

    for clean_clue in clues:
        for part in name_parts:
            clean_clue = clean_clue.replace(part, "********")

        clean_clue = re.sub(pronoun_pattern, "***", clean_clue)
        sanitized_clues.append(clean_clue)

    return sanitized_clues


def get_valid_person(persons):
    """
    Randomly pick a valid person from game_data and verify their Wikipedia page exists.
    """
    while True:
        person = random.choice(persons)
        try:
            wikipedia.summary(person, sentences=1)
            return person
        except Exception as e:
            #print (f"{Fore.RED}[An error occurred while fetching valid person\n{e}")
            continue


def play_round(persons, lives, score):
    """
    Play a single round of the game.
    """
    correct_person = get_valid_person(persons)
    clues = get_clues(correct_person)
    options = random.sample(persons, 5)
    if correct_person in options:
        options.remove(correct_person)
    else :
        del options[-1]
    options.append(correct_person)
    random.shuffle(options)

    for idx, person in enumerate(options):
        print(f"                  {Fore.LIGHTBLUE_EX}{chr(97 + idx)}. {person}")

    for clue_idx, clue in enumerate(clues):
        print(f"\n{Fore.CYAN}------------------------------------------------------- "
              f"{Fore.YELLOW}💰{score} {Fore.RED}❤️{lives}")
        print(f"\n{Fore.MAGENTA}[Clue {clue_idx + 1}] --- {textwrap.fill(clue, 53)}")
        guess = input(f"\nYour guess ({Fore.YELLOW}a, b, c, d, e{Style.RESET_ALL}): ").strip().lower()

        if guess in ["a", "b", "c", "d", "e"]:
            selected_person = options[ord(guess) - 97]
            if selected_person == correct_person:
                print(f"{Fore.GREEN}[Correct!] --- Well done!\n")
                score += 10
                return lives, score
            elif lives == 1:
                lives -= 1
                return lives, score
            else:
                print(f"{Fore.RED}[Wrong!] --- Try another clue.")
                lives -= 1

                if lives == 1:
                    print(f"{Fore.RED}⚠️ Oops, only one life left! Choose wisely! 💀")
        else:
            print(f"{Fore.RED}[Invalid input] --- Please select one of the options (a, b, c, d, e).")

    print(f"{Fore.YELLOW}Out of clues! The correct answer was {correct_person}.\n")

    return lives, score


def get_available_category():
    """
    Retrieve the list of available categories from the game data.
    """
    category = []
    for entry in wikiWho_data.data:
        category.append(entry["category"])
    return category


def end_game_message(final_score):
    """
    Display a personalized end-of-game message based on the player's score.
    """
    trophy = "🏆" if final_score >= 50 else "🎮"
    print(f"\n{Fore.RED}====================== GAME OVER =======================")
    print(f"{Fore.YELLOW}Your Final Score: {final_score} {trophy}")

    # Add personalized messages
    if final_score >= 50:
        print("Amazing job! You're a pro gamer!")
    elif final_score >= 20:
        print("Great effort! Keep practicing!")
    else:
        print("Good try! Better luck next time!")

    print("Thanks for playing!")


def main():
    """
    The main game loop that manages the game flow, rounds, lives, and score.
    The game begins by displaying a welcome screen, prompts the user to select
    a category, and plays through multiple rounds until the player runs out of
    lives. At the end of the game, a final score and personalized message are
    displayed.
    The player can choose to restart or exit after the game ends.
    """
    lives = 5
    score = 0
    round_number = 1

    print(start_screen)
    print(f"                 {Fore.GREEN}Welcome to the Guessing Game!")
    print(f"{Fore.MAGENTA}Get ready for an epic adventure filled with challenges and excitement!")
    player_name = input(f"{Fore.YELLOW}Please enter your name to start the game: ").strip()  # Take player's name
    if player_name:
        print(f"Hello, {Fore.LIGHTCYAN_EX}{player_name}!{Fore.BLUE} Let's begin the adventure. Good luck!")
    else:
        print("You didn't enter a name. Welcome, Player! Let's get started.")

    press_button_to_start()
    print(f"{Fore.LIGHTMAGENTA_EX}                    The game begins now...\n")
    print(f"{Fore.CYAN}Guess the person based on clues. Correct guesses earn 10 points.")
    print(f"{Fore.RED}A wrong guess costs 1 life. Game ends when you lose all 5 lives.")
    print(f"\n{Fore.CYAN}-------------------------------------------------------  "
          f"{Fore.YELLOW}💰{score} {Fore.RED}❤️{lives}")

    while lives > 0:
        available_category = get_available_category()
        print(f"{Fore.CYAN}                Available Categories:")
        print(f"{Fore.YELLOW}=======================================================\n")
        for i, category in enumerate(available_category, start=1):
            print(f"             {Fore.BLUE}{i}. {category}")
        print(f"{Fore.YELLOW}\n=======================================================")

        while True:
            chosen_category = input(f"{Fore.YELLOW}\nPlease enter your choice of category (number): ")
            if chosen_category.isdigit() and 1 <= int(chosen_category) <= len(available_category):
                category_name = available_category[int(chosen_category) - 1]
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please select a number from the list.")

        for entry in wikiWho_data.data:
            if entry["category"] == category_name:
                persons_list = entry["names"]
                break

        print(f"\n{Fore.CYAN}----------------------- Options ----------------------- Round {round_number}\n")
        lives, score = play_round(persons_list, lives, score)
        round_number += 1

        if lives == 0:
            break

    end_game_message(score)
    choice = input(
        f"{Fore.YELLOW}Do you want to continue playing? {Fore.CYAN}🎮 (y/n): {Style.RESET_ALL}").strip().lower()
    if choice == "y":
        main()
    elif choice == "n":
        print(f"{Fore.CYAN}See you soon! {Fore.YELLOW}👋😊")


if __name__ == "__main__":
    main()
import sys
import threading
import time
from abc import ABC, abstractmethod

import omniORB.any

from TestDirectory import orb_connection
from WhatsTheWord.referenceClasses import Player, ValuesList

from omniORB import CORBA, PortableServer
import WhatsTheWord.client, WhatsTheWord__POA

connection = orb_connection.ORBConnector()
player = WhatsTheWord.referenceClasses.Player(0, "Tester123", "Test", 0, 0, -1, False)


class ClientCallbackImpl(WhatsTheWord__POA.client.ClientCallback):
    def __init__(self):
        self._observers = []

    def notify(self, list: WhatsTheWord.referenceClasses.ValuesList):
        for observer in self._observers:
            observer.update(list)

    def add_observer(self, observer):
        self._observers.append(observer)

    def removeObserver(self, observer):
        if observer in self.observers:
            self._observers.remove(observer)

    def removeAllObservers(self):
        self._observers.clear()

class ClientControllerObserver(ABC):
    @abstractmethod
    def update(self, list: ValuesList):
        pass

callback_impl = ClientCallbackImpl()
ref = callback_impl._this()

def main():
    login_controller = LoginRegisterController()
    callback_impl.add_observer(login_controller)
    login_controller.display_menu()

    # connection.getPlayerService().request(WhatsTheWord.client.player.START_GAME, player, ref)
    # connection.getORB().run()

class LoginRegisterController:
    def __init__(self):
        self.users = {}
        self.checker = True

    def displayUpdate(self, value_list):
        message = get_string_from_list(value_list)
        if message == "UNSUCCESSFUL_LOGIN":
            print("Unsuccessful login!")
        elif message == "USER_ALREADY_LOGGED_IN":
            print("User already logged in!")
        else:
            get_player_from_list(value_list)
            main_menu = MainMenu()
            main_menu.display_menu()

    def display_menu(self):
        """Displays the menu and handles user input."""
        while self.checker:
            print("\n--- Welcome to the Login System ---")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Please select an option (1, 2, or 3): ")

            if choice == '1':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                player.username = username
                player.password = password
                self.checker = False
                connection.getPlayerService().request(WhatsTheWord.client.player.LOGIN, player, ref)

            elif choice == '2':
                username = input("Choose a username: ")
                password = input("Choose a password: ")
                player.username = username
                player.password = password
                connection.getPlayerService().request(WhatsTheWord.client.player.REGISTER, player, ref)

            elif choice == '3':
                # Exit the program
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def update(self, values_list):
        self.displayUpdate(values_list)

def get_player_from_list(values_list):
    player.playerId = omniORB.any.from_any(values_list.values[1])
    player.username = omniORB.any.from_any(values_list.values[2])
    player.password = omniORB.any.from_any(values_list.values[3])
    player.wins = omniORB.any.from_any(values_list.values[4])
    player.hasPlayed = omniORB.any.from_any(values_list.values[5])

class MainMenu:
    def __init__(self):
        # Sample data for leaderboard
        self.leaderboard = [
            {"username": "alice", "score": 500},
            {"username": "bob", "score": 450},
            {"username": "charlie", "score": 400}
        ]
        self.checker = True

    def start_game(self):
        """Simulate starting a new game."""
        print("\nStarting a new game...")
        match_making_controller = MatchMakingController()
        callback_impl.removeAllObservers()
        callback_impl.add_observer(match_making_controller)
        self.checker = False
        connection.getPlayerService().request(WhatsTheWord.client.player.START_GAME, player, ref)
        match_making_controller.wait_for_start()

    def view_leaderboards(self):
        """Display the leaderboard."""
        print("\n--- Leaderboards ---")
        if not self.leaderboard:
            print("No scores available.")
        else:
            for rank, entry in enumerate(self.leaderboard, start=1):
                print(f"{rank}. {entry['username']} - Score: {entry['score']}")
        print()

    def exit_program(self):
        """Exit the program."""
        print("\nExiting... Goodbye!\n")
        exit()

    def display_menu(self):
        """Displays the main menu and handles user input."""
        while self.checker:
            print("\n--- Main Menu ---")
            print("1. Start Game")
            print("2. Leaderboards")
            print("3. Exit")
            choice = input("Please select an option (1, 2, or 3): ")

            if choice == '1':
                self.start_game()
            elif choice == '2':
                self.view_leaderboards()
            elif choice == '3':
                self.exit_program()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

class MatchMakingController:
    def __init__(self):
        pass

    def wait_for_start(self):
        print("Waiting for players...")
        while True:
            time.sleep(1)

    def displayUpdate(self, value_list):
        time = get_time_from_list(value_list)
        print(f"{time} second(s) remaining")
        if time == 0:
            game_controller = GameController()
            callback_impl.removeAllObservers()
            callback_impl.add_observer(game_controller)

    def update(self, values_list):
        self.displayUpdate(values_list)

class GameController:
    def __init__(self):
        self.player = None

    def play_game(self, value_list):
        try:
            timer_value = get_int_from_list(value_list)
            mystery_word = get_string_from_list(value_list)
        except CORBA.BAD_TYPE:
            print("Error: Invalid data types in ValuesList.")
            return

        guessed_letters = set()
        lives = [5]
        self.game_over = False
        current_player = player
        current_player.time = -1
        self.timer_value = timer_value
        self.current_time = timer_value

        def timer_thread():
            current_time = self.timer_value
            while current_time != -1 and not self.game_over:
                sys.stdout.write(f"\rTime remaining: {current_time}")
                sys.stdout.flush()
                self.current_time = current_time
                time.sleep(1)
                current_time -= 1
            if not self.game_over:
                print("Time's up!")
                self.game_over = True

        def input_thread():
            print(_display_word_progress(mystery_word, guessed_letters))

            while not _is_word_fully_guessed(mystery_word, guessed_letters) and lives[0] != 0 and not self.game_over:
                try:
                    input_char = input("\nEnter a letter: ").strip().lower()

                    if len(input_char) != 1 or not input_char.isalpha():
                        print("Please enter a single letter.")
                        continue

                    letter = input_char[0]

                    if letter in guessed_letters:
                        print("Letter already guessed! Try another one.")
                        continue

                    guessed_letters.add(letter)

                    if letter not in mystery_word:
                        print("Wrong guess!")
                        lives[0] -= 1
                        print(f"Guess/es left: {lives[0]}")

                    print(_display_word_progress(mystery_word, guessed_letters))

                    if _is_word_fully_guessed(mystery_word, guessed_letters):
                        print(f"You have guessed the word: {mystery_word}")
                        print(f"Time is: {self.current_time}")
                        current_player.time = self.current_time # Capture remaining time

                except EOFError:
                    print("\nInput interrupted.")
                    break
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        timer_thread_obj = threading.Thread(target=timer_thread)
        input_thread_obj = threading.Thread(target=input_thread)

        timer_thread_obj.start()
        input_thread_obj.start()

        timer_thread_obj.join()
        input_thread_obj.join()

        connection.getGame().sendTime(current_player)  # Assuming sendTime method exists in the remote object
        print("Player time sent!")

    def update(self, value_list):
        winner = get_winner_from_list(value_list)

        if winner != "":
            result_controller = ResultsController()
            result_controller.displayWinner(winner)

        self.play_game(value_list)

class ResultsController:
    def __init__(self):
        pass

    def displayWinner(self, winner):
        print(f"The winner is {winner}")
        mainMenuController = MainMenu()
        callback_impl.removeAllObservers()
        callback_impl.add_observer(mainMenuController)
        mainMenuController.display_menu()

def _display_word_progress(word, guessed_letters):
    progress = []
    for char in word:
        if char in guessed_letters:
            progress.append(char)
        else:
            progress.append("_")
    return "\nWord: " + "".join(progress).strip()


def _is_word_fully_guessed(word, guessed_letters):
    for char in word:
        if char not in guessed_letters:
            return False
    return True

def get_string_from_list(values_list):
    extracted_value = omniORB.any.from_any(values_list.values[0])
    if isinstance(extracted_value, str):
        str_from_any = extracted_value
    return str_from_any

def get_int_from_list(values_list):
    extracted_value = omniORB.any.from_any(values_list.values[1])
    if isinstance(extracted_value, int):
        int_from_any = extracted_value
    return int_from_any

def get_winner_from_list(values_list):
    extracted_value = omniORB.any.from_any(values_list.values[2])
    if isinstance(extracted_value, str):
        winner = extracted_value
    return winner

def get_time_from_list(values_list):
    extracted_value = omniORB.any.from_any(values_list.values[0])
    if isinstance(extracted_value, int):
        int_from_any = extracted_value
    return int_from_any


def worker():
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()


import sys
import threading
import time
from abc import ABC, abstractmethod

import omniORB
from WhatsTheWord.referenceClasses import Player, ValuesList

from omniORB import CORBA, PortableServer
import CosNaming, WhatsTheWord.client, WhatsTheWord__POA

# TODO: Class for testing, need to improve


class ClientCallbackImpl(WhatsTheWord__POA.client.ClientCallback):
    def notify(self, list: WhatsTheWord.referenceClasses.ValuesList):
        print("testing",list)

    def add_observer(self, observer):
        self._observers.append(observer)

    def removeObserver(self, observer):
        if observer in self.observers:
            self._observers.remove(observer)

    def removeAllObservers(self):
        self._observers.clear()

# Initialise the ORB
def main():
    # sys.argv.extend(["-ORBInitRef","NameService=corbaloc:iiop:localhost:10050/NameService"])
    orb = CORBA.ORB_init(["-ORBInitRef","NameService=corbaloc:iiop:localhost:10050/NameService"], CORBA.ORB_ID)

    # Obtain a reference to the root naming context
    obj = orb.resolve_initial_references("NameService")
    ncRef = obj._narrow(CosNaming.NamingContextExt)

    if ncRef is None:
        print("Failed to narrow the root naming context")
        sys.exit(1)

    obj_poa = orb.resolve_initial_references("RootPOA")
    rootpoa = obj_poa._narrow(PortableServer.POA)
    rootpoa._get_the_POAManager().activate()


    # Resolve the name "test.my_context/ExampleEcho.Object"
    gameName = [CosNaming.NameComponent("Game", ""), ]

    try:
        obj = ncRef.resolve(gameName)
    except CosNaming.NamingContext.NotFound as ex:
        print("Game Name not found")
        sys.exit(1)

    # Narrow the object to an Example::Echo
    game = obj._narrow(WhatsTheWord.game_logic.Game)

    playerServiceName = [CosNaming.NameComponent("PlayerService", ""), ]

    try:
        obj = ncRef.resolve(playerServiceName)
    except CosNaming.NamingContext.NotFound as ex:
        print("PlayerService Name not found")
        sys.exit(1)

    playerService = obj._narrow(WhatsTheWord.client.player.PlayerService)

    if game is None:
        print("Object reference is not an WhatsTheWord::Game")
        sys.exit(1)


    callback_impl = ClientCallbackImpl()
    ref = callback_impl._this()

    player = WhatsTheWord.referenceClasses.Player(0,"Tester123","Test",0,0,-1,False)
    game_controller = GameController()
    callback_impl.add_observer(game_controller)

    # Invoke the request operation
    playerService.request(WhatsTheWord.client.player.START_GAME, player, ref)
    orb.run()

class ClientControllerObserver(ABC):
    @abstractmethod
    def update(self, list: ValuesList):
        pass


def _display_word_progress(word, guessed_letters):
    progress = []
    for char in word:
        if char in guessed_letters:
            progress.append(char)
        else:
            progress.append("_")
    return "Word: " + "".join(progress).strip()


def _is_word_fully_guessed(word, guessed_letters):
    for char in word:
        if char not in guessed_letters:
            return False
    return True


class GameController:
    def __init__(self):
        self.player = None
        self.game = main().game  # Assuming Client.py sets this up

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
        current_player = Player(0, "Test", "Tester", 0, 0, -1, False) # Assuming Player is defined in Client.py

        def timer_thread():
            current_time = timer_value
            while current_time != -1 and not self.game_over:
                print(f"Time remaining: {current_time}")
                time.sleep(1)
                current_time -= 1
            if not self.game_over:
                print("Time's up!")
                self.game_over = True

        def input_thread():
            print(_display_word_progress(mystery_word, guessed_letters))

            while not _is_word_fully_guessed(mystery_word, guessed_letters) and lives[0] != 0 and not self.game_over:
                try:
                    input_char = input("Enter a letter: ").strip().lower()

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
                        current_player.time = timer_value # Capture remaining time
                        self.game_over = True

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

        self.game.sendTime(current_player) # Assuming sendTime method exists in the remote object
        print("Player time sent!")

    def update(self, value_list):
        self.play_game(value_list)


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




if __name__ == "__main__":
    main()


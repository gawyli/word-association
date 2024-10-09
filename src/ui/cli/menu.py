from src.game.game_logic import Game
from src.data.session_manager import SessionManager

class Menu:
    @staticmethod
    def main_menu():
        while True:
            print("\nMain Menu:")
            print("1. Start Game")
            print("2. View Sessions")
            print("3. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                game = Game()
                game.play()
            elif choice == "2":
                sessions = SessionManager.load_sessions()
                for session in sessions["sessions"]:
                    print(session)
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
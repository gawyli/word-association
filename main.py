import argparse
from src.ui.cli.menu import Menu
from src.ui.web.routes import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word Association Game")
    parser.add_argument("--web", action="store_true", help="Run the web interface")
    args = parser.parse_args()

    if args.web:
        app = create_app()
        app.run(debug=True)
    else:
        Menu.main_menu()
from modules.game import Game

def main():
    
    Game(
        resolution = None,
        mode = None,
        save_path = "./docs/save_data/000.json"
    ).run()

if __name__ == "__main__":
    main()
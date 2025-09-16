import argparse

import manager

def main() -> None:
    print("Start Patient Manager")
    controller = manager.Controller()
    
    ui_controller = manager.UIController(controller)
    ui_controller.start()
    
    controller.close()


if __name__ == "__main__":
    main()

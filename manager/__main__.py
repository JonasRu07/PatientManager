import argparse

import manager

def main(args) -> None:
    print("Start Patient Manager")
    controller = manager.Controller()
    
    ui_controller = manager.UIController(controller)
    ui_controller.start()
    
    controller.close()
        
    return 
    if args.define:
        controller.solve_define_answers()
        print('Define solution\n', controller.week)
    if args.complete:
        print(controller.solve_recursive())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--define", "-d", action="store_true", help="Solves all patients, which have an possible hour no other patient can attend to")
    parser.add_argument("--complete", "-c", action='store_true', help="Tries to find a solution, which all patients are in one the week")
    
    args = parser.parse_args()
    main(args)

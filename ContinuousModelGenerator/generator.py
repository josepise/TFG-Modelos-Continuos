from ContinuousModelGenerator import GeneratorController
# from controller import GeneratorController

def main():
    controller= GeneratorController()   
    controller.get_view().run()
    
if __name__ == "__main__":
    main()
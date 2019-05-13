from balancer import balance
from physics import molecules_input, display_molecules
from util import clear

#Repeter l'application en boucle
while True:
    #Menu
    clear()
    print("  ______                  _   _               ____        _                           ")
    print(" |  ____|                | | (_)             |  _ \      | |                          ")
    print(" | |__   __ _ _   _  __ _| |_ _  ___  _ __   | |_) | __ _| | __ _ _ __   ___ ___ _ __ ")
    print(" |  __| / _` | | | |/ _` | __| |/ _ \| '_ \  |  _ < / _` | |/ _` | '_ \ / __/ _ \ '__|")
    print(" | |___| (_| | |_| | (_| | |_| | (_) | | | | | |_) | (_| | | (_| | | | | (_|  __/ |   ")
    print(" |______\__, |\__,_|\__,_|\__|_|\___/|_| |_| |____/ \__,_|_|\__,_|_| |_|\___\___|_|   ")
    print("           | |                                                                        ")
    print("           |_|                                           Thomas B and Quentin R, 1G5  ")
    print(2*"\n")
    print("Enter equations in the following form : C1H4 + O2.")
    print("Don't forget to specify the subscript of each atoms even if it's one.")
    print("\n")

    #Input
    reactants_input = input("Enter reactants : ")
    products_input = input("Enter products : ")
    
    #Example of equation that doesn't work
    # reactants_input = "K1Mn1O4 + H1Cl1"
    # products_input = "K1Cl1 + Mn1Cl2 + H2O1 + Cl2"

    #Transform the user input (text) into molecules and atoms that we can use for computation
    try:
        reactants = molecules_input(reactants_input)
        products = molecules_input(products_input)
    except Exception as e:
        print(e)
        print("Press enter to continue.")
        input("")
        #Continue means return to the start of the loop, here the main loop of the program
        continue

    #Computation
    try:
        #The function to balance an equation, in the file balancer.py
        #The start and end variables stores the time it started and ended to compute the execution time
        reactants, products = balance(reactants, products)

        #Display
        print("")
        print("Balanced equation : ")
        print(display_molecules(reactants) + " => " + display_molecules(products))

    except Exception as e:
        #If an error as occured, print this
        print("Couldn't find solutions for this equation.")
        print(e)

    #Ask the user if he wants to quit
    print("\nEnter q to quit, press enter to balance another equation : ")
    #If the input is q, quit, else, continue the wile true loop
    action = input("")
    if(action == "q"):
        exit()
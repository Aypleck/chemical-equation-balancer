from linear_solver import solve
from util import harmonize

#Return how many atoms there are in a molecule, if there are not, return false
def in_molecule(atom_type, molecule):
    for atom in molecule['atoms']:
        if(atom['type'] == atom_type):
            return atom['coef']
    return False

#The referencial is the molecule that will be set to have a coeficient of 1
def equation_to_matrix(reactants, products, referencial):
    #We create a system of equation, for each atom types we make a new equation,  and for every molecule a new variable.
    #The variables and solutions are linked by a key which is the type of the atom
    equation = {
        "vars": {},
        "solutions": {}
    }
    ## GENERATING THE SOLTIONS ##

    #Generating the solutions of the system of equation by setting the coeficient of the referencial molecule to one
    #Test if our referencial molecule is in the reactants or products
    if(referencial < len(reactants)):
        for atom in reactants[referencial]['atoms']:
            equation["solutions"][atom["type"]] = atom["coef"]
    else:
        for atom in products[referencial - len(reactants)]['atoms']:
            equation["solutions"][atom["type"]] = atom["coef"]

    #The other ones must cancel up so the result of the equation must be 0
    #We can take the reactants or products for this part it doesn't matter because we just need to set every other atom equations equal to zero
    #And every atoms should show up on both sides
    for i in range(len(reactants)):
        #We already made the solutions for the referencial molecule
        if(i != referencial):
            #For every atoms in every molecules,
            for atom in reactants[i]["atoms"]:
                #If we haven't already, set the solution to 0
                if(not atom["type"] in equation["solutions"]):
                    equation["solutions"][atom["type"]] = 0

    ## GENERATING THE VARIABLES ##

    #Initialization of the variables
    for molecule in reactants:
        for atom in molecule['atoms']:
            equation["vars"][atom["type"]] = []

    #Adding one variable per molecule, the coeficient of the variable will be how much atoms of the equation they are in this molecule
    #For each molecules except our reference molecule
    for i in range(len(reactants)):
        if(i != referencial):
            molecule = reactants[i]
            #For every equations (atom types)
            for atom_type, values in equation['vars'].items():
                #If they are this type of atom in this molecule, add how much they are for coeficient
                if(in_molecule(atom_type,molecule)):
                    # Add the negative of the coef because we are on the reactant side
                    equation['vars'][atom_type].append(-1 * in_molecule(atom_type,molecule))
                #Else add 0 (because there are none, so this variable doesn't count in this equation)
                else:
                    equation['vars'][atom_type].append(0)

    #We do the same thing for the products, but adding instead of subscracting
    for i in range(len(products)):
        if(i != referencial - len(reactants)):
            molecule = products[i]
            for atom_type, values in equation['vars'].items():
                if(in_molecule(atom_type,molecule)):
                    equation['vars'][atom_type].append(in_molecule(atom_type,molecule))
                else:
                    equation['vars'][atom_type].append(0)



    #Format the equation into arrays to pass it into the linear equation system solver
    variables = []
    solutions = []

    for atom_type, values in equation['vars'].items():
        variables.append(values)

    for atom_type, value in equation['solutions'].items():
        solutions.append(value)

    return variables, solutions

#balance an equation
def balance(reactants, products):
    #The molecule which has the coeficient 1
    referencial = 0

    #Transform our equation into a matrix with our varaibles coeficients as coeficients
    variables, solutions = equation_to_matrix(reactants, products, referencial)

    #Solve the system of equation using the linear solver in the file linear_solver.py
    coefs = solve(variables, solutions)

    #Add the molecule which has coeficient 1
    coefs = coefs[:referencial] + [1.] + coefs[referencial:]

    #Make all coeficients integers
    coefs = harmonize(coefs)
    #Map the results of the system of equations into the molecules
    #For the reactants
    for i in range(len(reactants)):
        reactants[i]['coef'] = coefs[i]
    #And for the products
    for i in range(len(products)):
        products[i]['coef'] = coefs[i + len(reactants)]

    #Return the balanced reactants and products
    return reactants, products
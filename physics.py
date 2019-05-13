from util import separate

#Constructors
def atom(type, coeficient):
    return {
        "type": type,
        "coef": coeficient
    }

def molecule(atoms, coeficient):
    return {
        "atoms": atoms,
        "coef": coeficient
    }

#Validation
#Test if a molecule has a valid coeficient
def valid_molecule(molecule):
    if(molecule['coef'] <= 0):
        return False
    return True
#Test if multiples molecules all have valid coeficients
def valid_molecules(molecules):
    for molecule in molecules:
        if(valid_molecule(molecule) == False):
            return False
    return True

#Display
def display_atom(atom):
    return atom['type'] + str(atom['coef'])

def display_molecule(molecule):
    res = ""
    for atom in molecule["atoms"]:
        res += display_atom(atom)

    return str(int(molecule['coef'])) + "(" + res + ")"

def display_molecules(molecules):
    res = ""
    for i in range(len(molecules)):
        molecule = molecules[i]
        res += display_molecule(molecule)
        if(i != len(molecules) - 1):
            res += "+"
    return res

#Inputs

def molecule_input(molecule_str):
    atoms = []
    parsed = separate(molecule_str)

    if(len(parsed) / 2 != round(len(parsed) / 2)):
        raise Exception("Invalid molecule : "+molecule_str+", please enter \"1\"s after every atoms (like H2O1)")

    for i in range(int(len(parsed) / 2)):
        atoms.append(atom(parsed[2*i], int(parsed[2*i+1])))
    return molecule(atoms, 1)

def molecules_input(string):
    parsed = string.replace(" ","").split("+")
    molecules = []
    for mol in parsed:
        molecules.append(molecule_input(mol))
    return molecules
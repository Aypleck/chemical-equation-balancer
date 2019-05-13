from Matrix import Matrix

#

#Sole a linear system of equation using Matrices
def solve(equations, solutions):
    #Count the equation number
    equation_nbr = len(solutions)
    var_nbr = len(equations[0])

    #Checking if there is a coherent number of equations and solutions
    if(len(equations) != equation_nbr):
        raise Exception("Invalid number of equations and solutions.")

    #Checking if there are a valid amount of coeficient in every equations
    for equation in equations:
        if(len(equation) != var_nbr):
            raise Exception("Invalid number of coeficients.")

    #Validationg equation numbers
    if(var_nbr > equation_nbr):
        raise Exception("Not enought equations to solve this system.")


    #If there is too much equations for the variables, we need te remove some equations.

    #Get the number of equations we need to remove
    equations_to_remove = equation_nbr - var_nbr

    #Remove duplicated equations
    if(equations_to_remove > 0):
        #The arrays with the filtered equations
        new_equations = []
        new_solutions = []
        #add the first equation with its solution in the new one.
        new_equations.append(equations[0])
        new_solutions.append(solutions[0])
        #For every starting at the second one equations.
        for i in range(1, len(equations)):
            #Check if we need to remove one
            if(equations_to_remove >0):
                #check if it is duplicated
                #The variable that tells us if the equation is already in the new equations            
                duplicated = False
                #Test for every equations that we kept, if there is one that is the same as the one we want to add, if so, set duplicated to True
                for j in range(len(new_solutions)):
                    if(new_solutions[j] == solutions[i] and new_equations[j] == equations[i]):
                        duplicated = True
                        break
                #If the varaible is not duplicated or if we still
                if(duplicated == False or equations_to_remove == 0):
                    new_equations.append(equations[i])
                    new_solutions.append(solutions[i])   
                else:
                    equations_to_remove -= 1
            else:
                new_equations.append(equations[i])
                new_solutions.append(solutions[i])

        solutions = new_solutions
        equations = new_equations

    #Testing the type of the solutions
    for x in solutions:
        if type(x) is not int and type(x) is not float:
            raise Exception('All solutions must be numbers.')

    #Making the matrix containg the variables coeficients
    V = Matrix(equations)
    #Transfoming the horizontal matrix into a vertical one
    S = Matrix([[x] for x in solutions])

    #Solving VX=S for X
    #X = V^-1 . S
    #Try the fast gauss method for inverting matrices
    try:
        V.gauss_invert()
    #If it fails, try the method with 1/determiant * comatrix
    except Exception:
        V.invert()
    
    variables = V.dot_product(S)

    #Formating the answers found into an array
    res = []
    for v in variables.data:
        #Using the round() function to remove the floating point error, and +0 to remove the -0.0 values
        res.append(round(v[0],3)+0) 

    return res
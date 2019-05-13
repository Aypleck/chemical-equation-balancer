import os

#Clear the console
def clear():
    if(os.name=='nt'):
        os.system('cls')
    else:
        os.system('clear')


#Split a string by the number / letter change
#To do this we create an array strings which contains the splitted version of the string.
#We then make a temporary string which we fill with the input character by character until the type of the character changes
# We then put the temporary string in the array, clear the temp string and continue

def separate(string):
    strings = []    #The array containing the splitted parts of the input
    current_string = ""     #The current string that hasn't been 
    for i in range(len(string)):    #For every caracters of the input
        char = string[i]
        if(i > 0):                  #If this is not the first character, we can take the previous caracter
            last_char = string[i - 1]
            if(char.isdigit() != last_char.isdigit()):  #if the types are differents,
                strings.append(current_string)          #Append the temporary string to the result
                current_string = char                   #Clear the string
            else:
                current_string += char                  #if the types doesn't changes, just add the caracter to the current string
        else:
            current_string += char      #If the current caracter is the first one, add it to the string
    strings.append(current_string)      #Add the last temp string to the splitter version
    return strings


#Multiply a list of numbers by the lowest factor that makes them all integers, return the new set of numbers
def harmonize(numbers):
    #For a lot of factors
    for n in range(1, 10000):
        valid = True
        #test if every numbers are integers, if they are, return the new values
        for num in numbers:
            if(num * n != round(num * n)):
                valid = False
        if(valid == True):
            return [num * n for num in numbers]
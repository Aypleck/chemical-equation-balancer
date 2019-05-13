def shift_array(array, index):
    for i in range(index):
        a = array.pop(0)
        array.append(a)
    return array

class Matrix:
    def __init__(self, data):
        #Getting the matrix dimensions
        self.rows = len(data)
        self.cols = len(data[0])
        
        self.data = data

        #Checking if all rows have the same length
        for line in data:
            if(len(line) != self.cols):
                raise Exception('Invalid matrix line : ' + line)

    def dot_product(self, x):
        #Test if we multiply by a matrix
        if(type(x) is not Matrix):
            raise Exception('You must multiply by a Matrix.')
        #Test if the size of bothe matrix are compatible with multiplication
        if(self.cols != x.rows):
            print(self.cols, x.rows)
            raise Exception('Number of columns of the first matrix must be equal to the number of rows of the second one.')

        result = ZerosMatrix(self.rows, x.cols)
        for i in range(self.rows):
            for j in range(x.cols):
                sum = 0
                for k in range(self.cols):
                    sum += self.data[i][k] * x.data[k][j]
                result.data[i][j] = sum
        return result

    def multiply(self, k):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] *= k

    #Makes sure that there are no zeros on the diagonal
    def can_invert(self):
        if(self.cols != self.rows):
            return False

        for i in range(self.cols):
            if(self.data[i][i] == 0):
                return False

        return True
    
    #Shift the matrix horizontally
    def horizontal_shift(self, amount):
        #Shifts all the rows array
        for row in self.data:
            row = shift_array(row, amount)

    #Shift the matrix vertically
    def vertical_shift(self, amount):
        #For every columns of the matrix
        for i in range(0,self.cols):        

            #Get the old value of the columns and put it into an array
            new_col = []
            for j in range(self.rows):
                new_col.append(self.data[j][i])

            #Shif it
            new_col = shift_array(new_col, amount)

            #Fill the old columns with the new shifted one
            for j in range(self.rows):
                self.data[j][i] = new_col[j]

    #Get the determinant of the matrix
    def det(self):
        if(self.cols != self.rows):
            raise Exception("The Matrix must be a square.")
        
        #If the matrixd is a 2x2 Matrix
        if(self.cols == 2):
            return self.data[0][0] * self.data[1][1] - self.data[1][0] * self.data[0][1]

        #The sum that will keep track of our determinant
        sum = 0

        #For every element of the first row
        for elem_col in range(len(self.data[0])):
            #data of the new matrix
            new_data = []
            #Get the matrix of the elements that shares no columns or rows with the element we chose
            #i starts at one because we chose the first row
            for i in range(1, len(self.data)):
                new_data.append([])
                #Add every element to the new matrix that is not in the same column as elem
                for j in range(len(self.data[i])):
                    #if the element is not in the column of the element we chose, add it to the new matrix
                    if(j != elem_col):
                        new_data[i - 1].append(self.data[i][j])
            #Create a matrix with these new elements
            new_matrix = Matrix(new_data)
            #Get the determinant of that new matrix
            new_det = new_matrix.det()
            #Multiply by the element
            new_det *= self.data[0][elem_col]
            #Switch signs every columns, starting with positive
            if(elem_col % 2 == 1):
                new_det *= -1

            #Add this to the global sum
            sum += new_det
        return sum

    #Get the cofactor of the matrix for the value i j
    def cofactor(self,i,j):
        if(self.cols != self.rows):
            raise Exception("The Matrix must be a square.")

        #Size of the matrix
        size = self.rows
        
        #Get the factor that tells us if the cofactor needs to be multiplied by -1
        coef = (-1)**(i+j)

        sub_matrix_data = []
        #Get a subatrix without the row i and the col j
        for row in range(size):
            if(row != i):
                sub_matrix_data.append([])
                for col in range(size):
                    if(col != j):
                        sub_matrix_data[len(sub_matrix_data) - 1].append(self.data[row][col])

        sub_matrix = Matrix(sub_matrix_data)
        return sub_matrix.det() * coef

    #Get the comatrix

    def comatrix(self):
        if(self.cols != self.rows):
            raise Exception("The Matrix must be a square.")

        #Size of the matrix
        size = self.rows

        #Create a matrix made with the cofactors as its coefiscients
        comatrix_data = []

        for i in range(size):
            comatrix_data.append([])
            for j in range(size):
                comatrix_data[i].append(self.cofactor(i,j))

        return Matrix(comatrix_data)


    #Invert the matrix
    def gauss_invert(self):
        if(self.cols != self.rows):
            raise Exception("The Matrix must be a square.")

        #We make copy of the current matrix and make a unit matrix that will become our inverted one once the current matrix will be the unit matrix
        A_ = self.copy()
        I_ = UnitMatrix(self.cols)

        #If there are zeros on the diagonal, try to shift the matrix until there are no longer, if we can't, the matrix isn't invertible
        horizontal_shifts = 0
        vertical_shifts = 0
        while(horizontal_shifts < A_.cols and not A_.can_invert()):
            A_.horizontal_shift(1)
            horizontal_shifts += 1
            vertical_shifts = 0
            while(vertical_shifts < A_.rows and not A_.can_invert()):
                A_.vertical_shift(1)
                vertical_shifts += 1
                
        #If even after shifting the matrix we still cannot invert it with the Gauss method, we will assume that we can't invert it
        if(not A_.can_invert()):
            raise Exception("Couldn't find any inverse")

        #Transform the matrix A_ into a unit matrix, perform the same operations to a unit Matrix to get the inverse

        #Multiply the row by the inverse of diag_val to get a 1 where the unit matrix would have one
        for diag_index in range(A_.rows):
            diag_val = A_.data[diag_index][diag_index]
            for i in range(A_.cols):
                A_.data[diag_index][i] *= 1/diag_val
                I_.data[diag_index][i] *= 1/diag_val

            #Set the other values to 0 on this column by substracting the line with the 1 on this col, times the value of the element to get 0
            for i in range(A_.rows):
                if(i != diag_index):
                    #Get the factor by which we will multiply the row with the 1  before subscracting it to the row where we want a 0
                    scaler = A_.data[i][diag_index]
                    for j in range(A_.cols):
                        #Substracting the rows
                        A_.data[i][j] -= scaler * A_.data[diag_index][j]
                        I_.data[i][j] -= scaler * I_.data[diag_index][j]
        #Unshifts the Matrix
        I_.horizontal_shift((I_.rows) - vertical_shifts)

        #Unshifts the Matrix
        I_.vertical_shift((I_.rows) - horizontal_shifts)

        #Assign the value
        self.data = I_.data

    def invert(self):
        det = self.det()
        if(det == 0):
            yield Exception("Matrix has no iverse")
        invert = self.comatrix()
        invert.multiply(1/det)
        self.data = invert.data


    #Return a copy of itself, not a pointer
    def copy(self):
        new_data = []
        for j in range(self.rows):
            new_data.append([])
            for i in range(self.cols):
                new_data[j].append(self.data[j][i])
        return Matrix(new_data)
        
    #Display the matrix
    def display(self):
        for row in self.data:
            print([round(x,3)+0 for x in row])

#Create a unit matrix
class UnitMatrix(Matrix):
    def __init__(self, size):
        data = []
        for i in range(size):
            data.append([])
            for j in range(size):
                if(i == j):
                    data[i].append(1)
                else:
                    data[i].append(0)
        Matrix.__init__(self, data)

#Create a matrix filled with zeros
class ZerosMatrix(Matrix):
    def __init__(self, rows, cols):
        data = []
        for i in range(rows):
            data.append([])
            for j in range(cols):
                data[i].append(0)
        Matrix.__init__(self, data)
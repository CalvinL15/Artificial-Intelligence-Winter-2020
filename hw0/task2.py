# AI20S - HW0
# Student ID                : B06902100
# English Name              : Calvin Liusnando
# Chinese Name (optional)   : 劉益瑋


# Import packages here
import numpy as np
from sklearn.linear_model import LinearRegression

class Predictor:
    def __init__(self, dataset_path='salary_data.csv'):
        self.test = 0
        self.dataset_data, self.dataset_target = self.read_csv(dataset_path)
        self.model = self.train()

    @staticmethod
    def read_csv(file_path='salary_data.csv'):
        # Implement your CSV file reading here
        # returns data, target
        # Both outputs should be in numpy array format with type np.float64
        # You may reshape the array if necessary
        # raise NotImplementedError
        dataset = np.genfromtxt(file_path,delimiter=',',dtype=np.float64,skip_header=1)
        X = (dataset[:,0]).reshape((-1,1))
        X.dtype = np.float64
        y = (dataset[:,1].reshape((-1,1)))
        y.dtype = np.float64
        return X, y

    def train(self):
        # returns sklearn's fitted LinearRegression model
        # Remember to pass self.dataset_data and self.dataset_target as its parameters
        #raise NotImplementedError
        trained_data, trained_target = self.read_csv()
        return LinearRegression().fit(self.dataset_data, self.dataset_target)

    def predict(self, x):
        # returns model's prediction given x as input
        #raise NotImplementedError
        return self.train(self).predict(x)

    def write_prediction(self, x, write_path='prediction.txt'):
        # opens a file using write_path with a writeable access
        # write all the outputs from the model's prediction to the file
        # You must write the output line by line instead of writing its numpy array or list object
        # This method does not return anything
        # raise NotImplementedError
        file = open(write_path, "w")
        for i in self.predict(self, x):
            file.write(str(format(i, '.2f'))+'\n')
        file.close()
        return


if __name__ == '__main__':
    # You may test your program here
    # Anything residing in this block will not be graded
    print("Good luck!")
    p = Predictor
    tst = np.zeros(5).reshape(-1,1)
    for i in range(0,5):
    	tst[i][0] = 20-i
    p.write_prediction(p, tst) 
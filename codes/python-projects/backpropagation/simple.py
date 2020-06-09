import numpy as np
from matplotlib import pyplot as plt

def sigmoidFunction(z, derivative=False):
    """derivative: get normal when false, while derivative when true"""
    if derivative:
       return z * (1.0 - z) # since (z) is already done with sigmoid(x)
       #return sigmoidFunction(z) * (1.0 - sigmoidFunction(z))
    else:
       return 1.0/(1.0 + np.exp(-z))

def lossFunction(Out, Desired):
    """Out: result of forward
       Desired: desired result
       It calculate Sum of Squared Error."""
    return ((Desired - Out)**2).sum()

class NeuralNetwork:
    def __init__(self, n_x, n_h, n_y):
        """n_x: number of input nodes
           n_h: number of hidden nodes
           n_y: number of output nodes"""
        self.W1     = np.random.rand(n_x, n_h) 
        self.W2     = np.random.rand(n_h, n_y)
        self.hidden = np.zeros((1, n_h))
        self.output = np.zeros((n_y, 1))
        self.activation = sigmoidFunction

    def feedforward(self, In):
        """In: input data"""
        self.hidden = self.activation(np.dot(In, self.W1))
        self.output = self.activation(np.dot(self.hidden, self.W2))
        return self.output

    def backprop(self, In, Out, Desired):
        """In: input data
           Out: the result of forwared propagation
           Desired: desired value
           application of the chain rule to find derivative of the loss function
           with respect to W2 and W1"""
        diff = Out - Desired
        d_W2 = np.dot(self.hidden.T, (2*diff*self.activation(Out, True)))
        d_W1 = np.dot(In.T,\
                      np.dot(2*diff*self.activation(Out, True), self.W2.T)*self.activation(self.hidden, True))
        # update the weights with the derivative (slope) of the loss function
        self.W1 -= d_W1
        self.W2 -= d_W2

if __name__ == "__main__":
    X = np.array([[0,0,1],
                  [0,1,1],
                  [1,0,1],
                  [1,1,1]])
    Y = np.array([[0],[1],[1],[0]])

    nn = NeuralNetwork(X.shape[1],4,Y.shape[1])

    loss_values = []
    for i in range(1000):
        z = nn.feedforward(X)
        nn.backprop(X, z, Y)
        loss = lossFunction(z, Y)
        loss_values.append(loss)

    print(nn.output)

    #plt.figure()
    plt.plot(loss_values)
    plt.xlabel("Iterations"); plt.xlim(-10, len(loss_values))
    plt.ylabel("Loss")
    plt.show()

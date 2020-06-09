import numpy as np
from matplotlib import pyplot as plt
import pickle

def sigmoidFunction(z, derivative=False):
    """derivative: get normal when false, while derivative when true"""
    if derivative: return z * (1.0 - z)
    else         : return 1.0/(1.0 + np.exp(-z))

def lossFunction(Out, Desired):
    """Out: result of forward
       Desired: desired result
       It calculate Sum of Squared Error."""
    return ((Desired - Out)**2).sum()

class NeuralNetwork:
    def __init__(self, n_x, n_h, n_y, init=True):
        """n_x: number of input nodes
           n_h: number of hidden nodes
           n_y: number of output nodes
           init: initialize weights when True"""
        if init: # intialize random values
           self.W1  = np.random.rand(n_x, n_h) 
           self.W2  = np.random.rand(n_h, n_y)
        else: # fill all zeroes
           self.W1  = np.zeros((n_x, n_h))
           self.W2  = np.zeros((n_h, n_y))
        self.hidden = np.zeros((1, n_h))
        self.output = np.zeros((n_y, 1))
        self.activation = sigmoidFunction
        self.inference = self.feedforward

    def feedforward(self, In):
        # you need to fill code here

    def backprop(self, In, Out, Desired):
        # you need to fill code here

    def train(self, In, Desired, iter=1000):
        # you need to fill code here

    def save(self, file):
        """file: file name to write weights to"""
        with open(file, 'wb') as f:
             params = { "W1" : self.W1, "W2": self.W2 }
             pickle.dump(params, f)

    def load(self, file):
        """file: file name to read weights from"""
        with open(file) as f:
             params = { "W1" : [], "W2": []}
             params = pickle.load(f)
        self.W1 = params["W1"]
        self.W2 = params["W2"]

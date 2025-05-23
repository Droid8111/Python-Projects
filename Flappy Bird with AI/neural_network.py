import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        # Xavier/He initialization
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * np.sqrt(2 / (input_size + hidden_size))
        self.bias_hidden = np.zeros(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * np.sqrt(2 / (hidden_size + output_size))
        self.bias_output = np.zeros(output_size)

    def forward(self, inputs):
        # inputs: 1D array of length input_size
        hidden = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden = self._sigmoid(hidden)
        output = np.dot(hidden, self.weights_hidden_output) + self.bias_output
        return self._sigmoid(output)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def mutate(self, mutation_rate):
        # mutate weights and biases
        def mutate_array(arr):
            mask = np.random.rand(*arr.shape) < mutation_rate
            arr += mask * np.random.randn(*arr.shape) * 0.1
        mutate_array(self.weights_input_hidden)
        mutate_array(self.bias_hidden)
        mutate_array(self.weights_hidden_output)
        mutate_array(self.bias_output)

    def copy(self):
        clone = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        clone.weights_input_hidden = np.copy(self.weights_input_hidden)
        clone.bias_hidden = np.copy(self.bias_hidden)
        clone.weights_hidden_output = np.copy(self.weights_hidden_output)
        clone.bias_output = np.copy(self.bias_output)
        return clone
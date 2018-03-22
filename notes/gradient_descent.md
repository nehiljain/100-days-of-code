

Gradient Descent

- Its tried to maximiser or minimise the objective function F(x) by updating x in the direction of its gradient ∂F(x). ∆x = ∂F(x).µ

Tips and Tricks

- Batch Vanilla Gradient Descent is slow, stocastic gradient is faster and can be used to learn online.
- Sanity check for learning rate and loss calculations http://cs231n.github.io/assets/nn3/learningrates.jpeg
- Choosing a proper learning rate can be difficult.
- Applying same learning rate to all parameters is inefficient as our features can be of different frequencies.
- Getting trapped in suboptimal local maxima/minima.
- ADAM is one of the popular algorithms being used.

Important reads

- [unittests for SGD](https://arxiv.org/abs/1312.6055)
- [Details of gradient descent and various learning rates](http://ruder.io/optimizing-gradient-descent/)


Scikit-Optimize

- Gradient Free Optimisations
- When its best to use this package and in particular bayesian optimisations
  - function is a black box function
    - no closed formed solution
    - no gradients defined
  - function is expensive to calculate
  - we only have noisy observations of the given function

- During bayesin optimisation
  - the process starts with some observations of the objective function
  - build probablistic model based on gaussian proess (need to read more on this)
  - have a cheap utility function
  - once it knows the function with good probability then it used gradient based approach
- Bayesian means?
  - unknown objective function <=> random function (stochastic process) (need to read more)
- There are lots of different things to tune/guess/set to begin with. This library goes a good job of providing defaults.



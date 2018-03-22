
# coding: utf-8

# In[1]:


import math
import numpy as np


# In[2]:


alpha = 0.01
beta_1 = 0.9
beta_2 = 0.999  #initialize the values of the parameters
epsilon = 1e-8


# In[3]:


def func(x):
  return x*x - 4*x + 4


# In[4]:


def grad_func(x):         #calculates the gradient
  return 2*x - 4


# In[5]:


theta_0 = 0           #initialize the vector
m_t = 0 
v_t = 0 
t = 0


# In[6]:


while (1):          #till it gets converged
  t +=1
  g_t = grad_func(theta_0)    #computes the gradient of the stochastic function
  m_t = beta_1*m_t + (1-beta_1)*g_t #updates the moving averages of the gradient
  v_t = beta_2*v_t + (1-beta_2)*(g_t*g_t) #updates the moving averages of the squared gradient
  m_cap = m_t/(1-(beta_1**t))   #calculates the bias-corrected estimates
  v_cap = v_t/(1-(beta_2**t))   #calculates the bias-corrected estimates
  theta_0_prev = theta_0                
  theta_0 = theta_0 - (alpha*m_cap)/(math.sqrt(v_cap)+epsilon)  #updates the parameters
  print('t {},theta0 {}, alpha {}'.format(t, theta_0, alpha))  
  if(theta_0 == theta_0_prev):    #checks if it is converged or not
    break


# Learning how to use gradient to search for global maxima of a function.
# 
# Suppose
# Y = f(X)
# 
# Problem: Find x such that Y is maximum.
# 
# 
# 

# In[7]:


import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
x = np.linspace(10,25,100)


# In[8]:


# Non-Convex Function
y = np.sin(x)

plt.scatter(x, y)
plt.show()


# In[9]:


# Convex Function
import math

x_try = []
def f(x):
#     print(x)
    x_try.append(x)
    return x * np.log(x)

y = list(map(f, x))
print(min(y))
plt.scatter(x, y)
plt.show()

from scipy import optimize
minimum = optimize.fmin(f, 100,full_output=1)
minimum

plt.scatter(range(len(x_try)),x_try)



# In[10]:


from scipy.optimize import curve_fit


# In[11]:


def func(x, a, b, c):
    print(a,b,c)
    return a * np.exp(-b * x) + c


# In[12]:


xdata = np.linspace(0, 4, 50)
y = func(xdata, 2.5, 1.3, 0.5)
np.random.seed(1729)
y_noise = 0.2 * np.random.normal(size=xdata.size)
ydata = y + y_noise
plt.plot(xdata, ydata, 'b-', label='data')


# In[13]:


popt, pcov = curve_fit(func, xdata, ydata)


# In[14]:


popt


# In[15]:


plt.plot(xdata, func(xdata, *popt), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))


# In[16]:


# Convex Function
x_try = []
def f(x):
    x_try.append(x)
    return x ** 8

y = list(map(f, x))
print(min(y))
plt.scatter(x, y)
plt.show()

from scipy import optimize
minimum = optimize.fmin(f, 100,full_output=1)
minimum

plt.scatter(range(len(x_try)),x_try)



# In[18]:


# Noisy
from skopt import gp_minimize
x_try = []
def f(x):
    
    return (np.sin(5 * x) * (1 - np.tanh(x ** 2)) *
            np.random.randn() * 0.1)
y = list(map(f, x))
print(min(y))
plt.scatter(x, y)
plt.show()

res = gp_minimize(f, [(-2.0, 2.0)])
res

plt.scatter(range(len(x_try)),x_try)


# In[21]:


x_try = []
def f(x):
    x_try.append(x[0])
    return (np.sin(5 * x[0]) * (1 - np.tanh(x[0] ** 2)) *
            np.random.randn() * 0.1)

res = gp_minimize(f, [(-2.0, 2.0)])


# In[27]:


noise_level=0.1
def f(x, noise_level=0.1):
    return np.sin(5 * x[0]) * (1 - np.tanh(x[0] ** 2)) + np.random.randn() * noise_level
x = np.linspace(-2, 2, 400).reshape(-1, 1)
fx = [f(x_i, noise_level=0.0) for x_i in x]
plt.plot(x, fx, "r--", label="True (unknown)")
plt.fill(np.concatenate([x, x[::-1]]),
         np.concatenate(([fx_i - 1.9600 * noise_level for fx_i in fx], 
                         [fx_i + 1.9600 * noise_level for fx_i in fx[::-1]])),
         alpha=.2, fc="r", ec="None")
plt.legend()
plt.grid()
plt.show()


# In[28]:


res = gp_minimize(f,                  # the function to minimize
                  [(-2.0, 2.0)],      # the bounds on each dimension of x
                  acq_func="EI",      # the acquisition function
                  n_calls=15,         # the number of evaluations of f 
                  n_random_starts=5,  # the number of random initialization points
                  noise=0.1**2,       # the noise level (optional)
                  random_state=123)   # the random seed


# In[29]:


print("x^*=%.4f, f(x^*)=%.4f" % (res.x[0], res.fun))


# In[30]:


res.models


# In[31]:


from skopt.plots import plot_convergence
plot_convergence(res);


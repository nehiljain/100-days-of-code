
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

# In[37]:


import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
x = np.linspace(10,25,100)


# In[8]:


# Non-Convex Function
y = np.sin(x)

plt.scatter(x, y)
plt.show()


# In[36]:


# Convex Function
import math
def f(x):
    return x * np.log(x)

y = list(map(f, x))
print(y)
print(min(y))
plt.scatter(x, y)
plt.show()

from scipy import optimize
minimum = optimize.fmin(f, 100,full_output=1)
minimum


# In[25]:


from scipy.optimize import curve_fit


# In[11]:


def func(x, a, b, c):
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


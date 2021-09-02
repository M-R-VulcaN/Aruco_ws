import numpy as np
import matplotlib.pyplot as plt

# x = np.linspace(0, 2*np.pi, 10)
# y = np.sin(x)
t_full=np.linspace(0, 9, 10)
t_no_nans = [0,1,2,3,6,7,8,9]
y = [0,1,2,3,6,7,8,9]

yinterp = np.interp(t_full, t_no_nans, y)
plt.plot(t_no_nans, y, 'o')
plt.plot(t_full, yinterp, '-x')
plt.show()

#%%
import numpy
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


#%%
distances = numpy.loadtxt(open("distances.csv","r"),delimiter=" ")


#%%
distances


#%%
plt.figure(figsize=(8,6))
plt.xlim([0, 20000])
plt.xlabel('distance in metric space')
plt.ylabel('distance in embedding space')
plt.scatter(distances[:, 0], distances[:, 1])
plt.savefig('distance.pdf')



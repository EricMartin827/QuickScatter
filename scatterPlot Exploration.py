import pandas as pd
import matplotlib.pyplot as plt

#from sklearn.cluster import KMeans

df = pd.read_excel("heightWeightChart.xlsx", index_col = 0)


df.plot.scatter(x = "Height(Inches)", y = "Weight(Pounds)")
plt.show()



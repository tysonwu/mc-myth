import plotly.express as px
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


df = pd.read_csv('df.csv')
df['increment'] = df['informed_score'] - df['random_score']

# fig = px.density_heatmap(df, x='al', y='acl', z='increment', histfunc='avg')
fig = px.density_heatmap(df, x='kl', y='acl', z='increment', histfunc='avg')
# fig = px.density_heatmap(df, x='kl', y='al', z='increment', histfunc='avg')
fig.show()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# img = ax.scatter(df['kl'], df['al'], df['asl'], c=df['increment'], cmap=plt.inferno())
# fig.colorbar(img)
# plt.show()
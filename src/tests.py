import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns



shapefile_path = "ne_110m_land/ne_110m_land.shp"
world = gpd.read_file(shapefile_path)
world.plot()
plt.show()
# Written by Savindu9x
# Last Modified on 20-09-2021

# Import Libraries
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Returns the scatterplot for user specified k_number
def kmeansProcess():
    # Creating root window
    root = tk.Tk()
    # creating canvas
    canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
    canvas1.pack()
    # Creating a label to showcase the clustering plots
    label1 = tk.Label(root, text='k-Means Clustering')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)
    # Text Labels specifying number of clusters
    label2 = tk.Label(root, text='Type Number of Clusters:')
    label2.config(font=('helvetica', 8))
    canvas1.create_window(200, 120, window=label2)

    entry1 = tk.Entry(root)
    canvas1.create_window(200, 140, window=entry1)

    # function to Import data from excel file
    def getExcel():
        global df
        import_file_path = filedialog.askopenfilename()
        read_file = pd.read_excel(import_file_path)
        df = DataFrame(read_file, columns=['x', 'y'])
        print(df)

    # Creating a button to export the data from excel
    browseButtonExcel = tk.Button(text=" Import Excel File ", command=getExcel, bg='green', fg='white',
                                  font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 70, window=browseButtonExcel)

    # Let the user enter number of clusters
    # k-means clustering
    def getKMeans():
        global df
        global numberOfClusters
        # Prompts user to enter k
        numberOfClusters = int(entry1.get())
        # apply Kmeans algorithm in df dataset with specified num of clusters
        kmeans = KMeans(n_clusters=numberOfClusters).fit(df)
        centroids = kmeans.cluster_centers_
        # Display coordinates of centroids
        label3 = tk.Label(root, text=centroids)
        canvas1.create_window(200, 250, window=label3)

        # plotting
        figure1 = plt.Figure(figsize=(4, 3), dpi=100)
        ax1 = figure1.add_subplot(111)
        ax1.scatter(df['x'], df['y'], c=kmeans.labels_.astype(float), s=50, alpha=0.5)
        ax1.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
        scatter1 = FigureCanvasTkAgg(figure1, root)
        scatter1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)

    # creating process button
    processButton = tk.Button(text=' Process k-Means ', command=getKMeans, bg='brown', fg='white',
                              font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 170, window=processButton)

    root.mainloop()

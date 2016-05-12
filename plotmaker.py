class PlotMaker():
    '''A set of functions to make different kinds of plots. Specify an input file (.csv), an output file (.png), and columns to use as a python list of integers
       Other parameters can be changed in the code'''
  
      
    def __init__(self,mydata,output_file,cols_to_use):
        self.mydata = mydata
        self.output_file = output_file
        self.cols_to_use = cols_to_use
        
    def heatmapmaker(self,sample_names,entity_names):
        '''A function for making heatmap. Sample names on x-axis, entity names on y-axis. Two text files need to be
           specified as well: one with tab separated sample names, the other containing newline separated
           entity names (e.g.Gene symbols). Assumes a dataframe with row and column names'''
    
        import pandas as pd
        import seaborn as sns
        sns.set(font_scale = 1.05)

        ## Read in sample names from a text file, and convert to list
        collection_file_1 = open(sample_names,'r+')
        pre_list_1 = collection_file_1.read()
        sample_ids= pre_list_1.split()

        ##Read in entity (e.g. Gene symbols)names from a textfile
        collection_file_2 = open(entity_names,'r+')
        pre_list_2 = collection_file_2.read()
        entity_names= pre_list_2.split("\n")

        #Read in data
        df = pd.read_csv(self.mydata, header = None, skiprows = [0], usecols = self.cols_to_use)
        assert self.mydata.endswith(".csv")
        
        g = sns.heatmap(df,xticklabels = sample_ids,yticklabels = entity_names,label = 'small',robust = False,cmap = "bwr",cbar = True,vmin = -0.8,vmax = 0.8)
        sns.plt.xticks(rotation = 0)

        ##from matplotlib.patches import Rectangle
        ##ax1 = g.add_patch(Rectangle((0, 59), 37, 0, fill=False, edgecolor='orange', lw=0.6))

        ## Save figure to local disk
        sns.plt.savefig(self.output_file,format = 'png',bbox_inches = 'tight',dpi = 300)
        sns.plt.clf()
        ##sns.plt.show()
        return "Completed"

    def barplotmaker(self):
        '''Function to make bar plots. Input is a csv file. And output file needs to be specified'''
    
        import pandas as pd
        import seaborn as sns

        sns.set(font_scale = 1.05)
        sns.set_style("whitegrid", {"axes.linewidth": "0","axes.labelcolor":"0.8"})
        sns.despine()

        #Read in data
        df = pd.read_csv(self.mydata, index_col = None,header = None, skiprows = [0],usecols = self.cols_to_use)
        assert self.mydata.endswith(".csv")
        sns.plt.figure(figsize = (8,1.1), dpi = 300)
        sns.barplot(data = df, palette = "Blues")

        ## Save figure to local drive
        
        sns.plt.savefig(self.output_file,format = 'png',dpi = 300,bbox_inches = 'tight')
        assert self.output_file.endswith(".png")
        return "Completed"

        #mybar.set(ylabel = "Number of pathways")
        #sns.plt.show()

    def boxplotmaker(self,xlabel,ylabel):
        '''Function to make boxplots. Input is a .csv file, xlabel (string), ylabel(string),and
        output file (.png) specification'''

        import pandas as pd
        import seaborn as sns
        sns.set(font_scale = self.font_size)
        sns.set_style("whitegrid", {"axes.linewidth": "0","axes.labelcolor":"0.1"})
        sns.despine()

        # Read in data as a csv file

        mydata = pd.read_csv(self.mydata,index_col = None,header = None, skiprows = [0],usecols = self.cols_to_use)
        assert self.mydata.endswith(".csv")

        ha = ['right', 'center', 'left']
        sns.boxplot(data = mydata, x = xlabel,y = ylabel, palette = "Blues", width = 1.0, linewidth = 2.1)

        sns.plt.xticks(rotation = 0, ha = ha[1])

        sns.plt.savefig(self.output_file,format = 'png',bbox_inches = 'tight',dpi = 300)
        assert self.output_file.endswith(".png")
        return "Completed"
        #sns.plt.show()
 

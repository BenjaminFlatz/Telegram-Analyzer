import pandas as pd
import argparse
import os
from bs4 import BeautifulSoup
from pathlib import Path
from os import path
import matplotlib.pyplot as plt

class TAnalyzer
    def __init__(self):
         
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.parser.add_argument("-f", "--filename", help="filename for output file", default="data", type=str)
        self.parser.add_argument("-p", "--path", help="path", default="ChatExport_DD_MM_YYYY" + os.path.sep, type=str)
        self.parser.add_argument("-n", "--number", help="number of html files", default=41, type=int)
        self.args = self.parser.parse_args() 
        
        
    
    def read_file(self, file):
        
        
        f = open(file, encoding="utf8")     
        soup = BeautifulSoup(f, 'html.parser')
        full_messages = soup.find_all('div', attrs={'class': 'message default clearfix'})
        names = []#soup.find_all('div', attrs={'class': 'from_name'})
        times = []#soup.find_all('div', attrs={'class': 'pull_right date details'})
        messages = []#soup.find_all('div', attrs={'class': 'text'})

        df_full = pd.DataFrame({'full_message':full_messages})
        for index, row in df_full.iterrows():
            #print(index)
            names.append(str(row['full_message'].find('div', attrs={'class': 'from_name'})).replace('<div class="from_name">\n', '').replace('\n       </div>', ''))
            times.append(str(row['full_message'].find('div', attrs={'class': 'pull_right date details'})).replace('<div class="pull_right date details" title=', '')[1:20])
            messages.append(str(row['full_message'].find('div', attrs={'class': 'text'})).replace('<div class="text">\n', '').replace('\n       </div>', '').replace('<br/>', ''))
            
        df = pd.DataFrame({'name':names,
                           'time':times,
                           'message':messages})
        
        #print(df.to_string())
        
        f.close()
        try:
            #df = df.T
            #df = self.string2Timestamp(df)
            if path.exists(self.args.filename) and not df.empty:
                df.to_csv(self.args.filename, sep=',', mode="a", header=False, index=False)
            elif not df.empty:
                df.to_csv(self.args.filename, sep=',', mode="w", header=True, index=False)
        except PermissionError as e:
            print(repr(e))
        return(df)

    def read(self):

        pathlist = Path(self.args.path).glob('**'+ os.path.sep +'*.html')
        for path in pathlist:
            print(str(path))
            self.read_file(str(path))
      
    def vis(self, title, filename, x, y, kind, typecal):
        try:
            df = pd.read_csv(filename)
            #df = self.string2Timestamp(df)

            if typecal == "count":
                df = df.groupby(x)[y].count()
            elif typecal == "mean":
                df = df.groupby(x)[y].mean()
            elif typecal == "max":
                df = df.groupby(x)[y].max()
            elif typecal == "min":
                df = df.groupby(x)[y].min() 
            else:
                print("select a valid type of calculation")
                return
            df.plot(kind=kind)#, subplots=True)
            #print(df)
        
            plt.title(title)
            plt.show()
        except KeyError as e:
            print(repr(e))
        except AttributeError as e:
            print(repr(e))       

    def run(self):
        self.vis("Telegram-Analyzer", self.args.filename, "name", "time", "bar", "count")

if __name__ == "__main__":
    t_analyzer = TAnalyzer()
    t_analyzer.run()

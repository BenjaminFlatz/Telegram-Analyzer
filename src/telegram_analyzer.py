import pandas as pd
import os
from bs4 import BeautifulSoup
from pathlib import Path
from os import path
import matplotlib.pyplot as plt
import matplotlib
import csv
import numpy as np
import re


class TelegramAnalyzer:
    def __init__(self, outDir):
        self.path = path
        self.outDir = outDir
        self.df = pd.read_csv("data/chat.csv")
 
    def export_2_csv(self, file, writer):

        f = open(file, encoding="utf8")
        soup = BeautifulSoup(f, 'html.parser')
        fullMessages = soup.find_all('div', attrs={'class': 'message default clearfix'})

    

        for fullMessage in fullMessages:
            # print(fullMessage)
            try:

                fromName = fullMessage.find_next('div', attrs={'class': 'from_name'}).text.strip()
                timestamp = fullMessage.find_next('div', attrs={'class': 'pull_right date details'}).get("title")
                body = fullMessage.find_next('div', attrs={'class': 'text'}).get_text().strip()

                writer.writerow([fromName, timestamp, body])
                    

                

            except AttributeError as e:
                print(repr(e))
                # print(fullMessage)

   

        f.close()

    def read(self, filename):
        with open(filename, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(["name", "timestamp", "body"])


            files = Path(self.path).glob('**' + os.path.sep + '*.html')
            for file in files:
                print(str(file))
                self.export_2_csv(str(file), writer)


    

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
            df.plot(kind=kind)  # , subplots=True)
            # print(df)

            plt.title(title)
            plt.show()
        except KeyError as e:
            print(repr(e))
        except AttributeError as e:
            print(repr(e))
            

    def show_statistics(self):

        df = pd.read_csv("data/statistics.csv")
        df.plot(x="name", y="messages", kind="scatter")  # , subplots=True)
        #print(df)

        plt.title("statistics")
        plt.show()



    def get_statistics(self):
        df = pd.DataFrame(columns=["category", "sum"])
        categories = self.get_categories(self.df)#pd.read_csv(categoriesFile).applymap(str.lower)
        data = self.df

        messageSum = []
        categoriesList = []
        for index, category in categories.iterrows():
            messageSum.append(data['body'].str.contains(category['body']).sum())
            categoriesList.append(category['body'])
            print(str(categoriesList) + str(messageSum))
            
        df = pd.DataFrame({"category":categoriesList,
                            "sum":  messageSum})
        df.to_csv('data/statistics.csv')

        """
        for index, row in data.iterrows():

            for index, category in categories.iterrows():
                print(row['name'], category['name'])



                #if row['body'].str.contains(category['name']).any():
                #    print(category['name'])
                
        """

    def set_primary_key(self, df):
        

        primaryKeys = []
        for index, row in df.iterrows():
            primaryKeys.append(index)

        newDf = pd.DataFrame(columns=['primary_key'])
        newDf.append(df)
        print(newDf)
        return newDf

    def get_towns(self):
        df = pd.read_csv(self.outDir + os.path.sep + 'orte.csv').apply(lambda x: x.astype(str).str.lower())
        towns = []
        print(df.reset_index(drop=True))
        df = df.reset_index(drop=True)
        df.to_csv(self.outDir + os.path.sep + 'towns.csv')
        for index, row in df.iterrows():
            towns.append(str(row['name']).lower())
        return towns

    def get_msg_categories(self):
        df = pd.read_csv("data/chat.csv")
        df = df.assign(body=df['body'].str.replace(',', '').str.split(' ')).explode('body').reset_index().apply(lambda x: x.astype(str).str.lower())
        df = df.rename(columns={'index': 'msgKey'})
        print(df)
        df.to_csv(self.outDir + os.path.sep + 'categorized.csv', mode='w')

        return df



    def plot(self, df):
        towns = self.get_towns()
        print(towns)
        return
        df = self.get_df_by_towns(df, towns)
        #cmap = plt.get_cmap('viridis')
        #colors = cmap(np.linspace(0, 1, len(df)))
       
        #matplotlib.rc('font', family='Arial')
        df.plot.scatter(x="body", y="name")
        #plt.hist(x=df['body'], bins=len(df.index),alpha=0.5)
        #plt.hist(x=df["body"].values)
        #plt.xlabel("X", size=16)
        #plt.ylabel("y", size=16)
        plt.xticks(rotation=90)
        plt.rc('axes', unicode_minus=False)
        plt.title("Cops Radar Stau", size=18)
        plt.grid(color='grey', linestyle='-.', linewidth=0.2)
        plt.show()

    def get_df_by_towns(self, df, towns):
        df = df.assign(body=df['body'].str.replace(',', '').str.split(' ')).explode('body').reset_index().apply(lambda x: x.astype(str).str.lower())
        df = df.loc[df['body'].isin(towns)]
        print(df)
        df.to_csv(self.outDir + os.path.sep + 'categorized.csv', mode='w')

        return df

    def get_categories(self, df):
        df = df.assign(body=df['body'].str.replace(',', '').str.split(' ')).explode('body')
        df["body"] = df["body"].str.replace('[^a-zA-Z]', '')
        df = pd.DataFrame(df["body"]).applymap(str.lower)
        df = df.drop_duplicates(subset=['body'])
        print(df)
        return df
    
    
    def run(self):
        print(self.get_statistics())

if __name__ == "__main__":
    ta = TelegramAnalyzer('data')
    ta.run()
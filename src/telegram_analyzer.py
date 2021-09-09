import pandas as pd
import os
from bs4 import BeautifulSoup
from pathlib import Path
from os import path
import matplotlib.pyplot as plt
import csv

class TelegramAnalyzer:
    def __init__(self):
        self.path = path
 
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
        # print(df)

        plt.title("statistics")
        plt.show()



    def get_statistics(self, categoriesFilename, chatFile):


        df = pd.DataFrame(columns=["category", "sum"])
        categories = pd.read_csv(categoriesFilename).applymap(str.lower)
        data = pd.read_csv(chatFile).applymap(str.lower)


        
        messageSum = []
        for index, category in categories.iterrows():
            print(category['name']+" "+str(data['body'].str.contains(category['name']).sum()))
            messageSum.append(data['body'].str.contains(category['name']).sum())
            
        categories['messages'] = messageSum
        print(categories)

        categories.to_csv('data/statistics.csv')

        """
        for index, row in data.iterrows():

            for index, category in categories.iterrows():
                print(row['name'], category['name'])



                #if row['body'].str.contains(category['name']).any():
                #    print(category['name'])
                
        """

    def set_primary_key(self, file):
        df = pd.read_csv(file)

        primaryKeys = []
        for index, row in df.iterrows():
            primaryKeys.append(index)

        newDf = pd.DataFrame(columns=['primary_key'])
        newDf.append(df)
        print(newDf)

if __name__ == "__main__":
    ta = TelegramAnalyzer()
    ta.set_primary_key("data/chat.csv")
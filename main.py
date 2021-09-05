from src import TelegramAnalyzer
import argparse
import os





if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--categories", help="categories file", default="vorarlberg.csv", type=str)
    parser.add_argument("-f", "--filename", help="data file", default="data.csv", type=str)
    parser.add_argument("-p", "--path", help="path", default="ChatExport" + os.path.sep, type=str)
    parser.add_argument("-n", "--number", help="number of html files", default=74, type=int)
    args = parser.parse_args()

    ta = TelegramAnalyzer(args.filename)

    #ta.vis("Telegram-Analyzer", "statistics.csv", "name", "email", "bar", "sum")
    #ta.categorize(args.categories)
    ta.show_statistics()


    

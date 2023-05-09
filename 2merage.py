import glob
import pandas as pd
import time

timestamp = time.strftime('%Y%m%d_%H%M%S')


def merage_dataframe():
    interesting_files = glob.glob("output/*.csv") 
    df = pd.concat((pd.read_csv(f, header = 0) for f in interesting_files), ignore_index=True)
    df.to_csv('output/meraged_'+timestamp+'.csv')


def main():
    merage_dataframe()


if __name__ == "__main__":
    main()
import sys
import DataPrep

def main():
    fname = DataPrep.get_data("https://raw.githubusercontent.com/CapitalOneRecruiting/DS/master/transactions.zip")
    DataPrep.get_databuffer(fname)


if __name__ == "__main__":
    main()
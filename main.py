import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import DataPrep as DP
import DataAnalysis as DA
import DataSampling as DS

def main():
    # GET DATASET AND STORE AS JSON FILE
    fname = DP.get_data("https://raw.githubusercontent.com/CapitalOneRecruiting/DS/master/transactions.zip")

    # CONVERT TO DATAFRAME AND FILL IN BLANKS
    df = DP.get_databuffer(fname)

    # SAVE TO PICKLE FOR EASY AND FAST ACCESS
    # df.to_pickle('data.pkl')
    # data.pkl -> original data (786363 x 29)
    # df = pd.read_pickle('data.pkl')
    # cols = df.columns.values

    # DATA PREP
    df = DP.data_prep(df)
    # df.to_pickle('data.pkl')
    # data1.pkl -> add features (786363 x 34)
    cols = df.columns.values

    # EDA
    # info shows column names, null values, dtypes
    df.info()
    # no duplicates to drop
    df.drop_duplicates(inplace=True)
    print(df.describe())
    # print(df.isFraud.unique())
    # print(df.isFraud.value_counts())
    # scatter plot is pointless cause you wont be able to understand much as isFraud = {0,1}
    # for i in cols:
    #     DA.scatter_plot(df, i, 'isFraud')
    # DA.pairwise_correlation(df)
    # DA.get_isFraudTrue(df)

    # 98:2 ratio for V:F so adjusting to get 7:3 (avoid underfit)
    # tmp_v = df.loc[df['isFraud'] == 0].sample(n=28974, random_state=1)
    # tmp_f = df.loc[df['isFraud'] == 1]
    # df_adjusted = pd.concat([tmp_v, tmp_f])

    # DA.creditLimit_check(df, df_adjusted)
    # DA.overdraw_check(df, df_adjusted)
    # DA.merchName_check(df, df_adjusted)
    # DA.merchCat_check(df, df_adjusted)
    # DA.location_check(df, df_adjusted)
    # DA.posEntryMode_check(df, df_adjusted)
    # DA.posCond_check(df, df_adjusted)
    # DA.dateAddressChange_check(df, df_adjusted)
    # DA.CVV_check(df, df_adjusted)
    # DA.transactionType_check(df, df_adjusted)
    # DA.card_check(df, df_adjusted)
    # DA.expDateMatched_check(df, df_adjusted)

    exclude = ['accountNumber', 'customerId', 'availableMoney', 'transactionDateTime', 'transactionAmount', 'currentBalance', 'overDraw', 'storeID', 'overSeas', 'accountOpenDate', 'dateOfLastAddressChange', 'addressChangeActivity', 'cardCVV', 'enteredCVV', 'cvvMatch', 'cardLast4Digits', 'cardPresent', 'expirationDateKeyInMatch', 'isFraud']
    cols = [i for i in cols if i not in exclude]
    df_w_dummies, cols = DP.add_dummies(df, cols)
    # df_w_dummies.shape => (786363, >440)

    # SAMPLING
    param = ['overDraw', 'transactionAmount', 'overSeas', 'addressChangeActivity', 'cvvMatch', 'currentBalance', 'cardLast4Digits', 'cardPresent', 'expirationDateKeyInMatch', 'isFraud']
    stratify_param = []
    stratify_param.append(cols)
    stratify_param.append(param)
    stratify_param = [i for sublist in stratify_param for i in sublist]
    # df_w_dummies.to_pickle('data2.pkl') => for easier and faster access next time around
    # data2.pkl -> add dummies (786363 x 439)

    # df = df.select_dtypes(np.number)
    # only for read_pickle('data2.pkl')

    DS.strat_sample(df, df.columns.values)
    plt.plot([0, 1], [0, 1], 'k--', label='TPR = FPR')
    plt.show()

if __name__ == "__main__":
    main()
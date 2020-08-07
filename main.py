import pandas as pd
import DataPrep as DP
import DataAnalysis as DA
import DataSampling as DS

def main():
    # GET DATASET AND STORE AS JSON FILE
    # fname = DP.get_data("https://raw.githubusercontent.com/CapitalOneRecruiting/DS/master/transactions.zip")

    # CONVERT TO DATAFRAME AND FILL IN BLANKS
    # df = DP.get_databuffer(fname)

    # SAVE TO PICKLE FOR EASY AND FAST ACCESS
    # df.to_pickle('data.pkl')
    df = pd.read_pickle('data1.pkl')
    print(df.loc[0])
    # df = DP.data_prep(df)
    # df.to_pickle('data1.pkl')
    # print(df.loc[0])

    # ANALYSIS
    # DA.get_isFraudTrue(df)
    # DA.accNum_check(df)
    # DA.overdraw_check(df)
    # DA.creditLimit_check(df)
    # DA.merchName_check(df)
    # DA.merchCat_check(df)
    # DA.location_check(df)
    # DA.posEntryMode_check(df)
    # DA.posCond_check(df)
    # DA.dateAddressChange_check(df)
    # DA.CVV_check(df)
    # DA.transactionType_check(df)
    # DA.card_check(df)
    # DA.expDateMatched_check(df)

    # SAMPLING
    stratify_parameters = ['creditLimit', 'overDraw', 'overSeas', 'posEntryMode', 'posConditionCode', 'merchantCategoryCode', 'addressChangeActivity', 'cvvMatch', 'transactionType', 'cardPresent', 'expirationDateKeyInMatch', 'isFraud']
    stratified_report = DS.stratified_sample_report(df, ['isFraud'])
    print(stratified_report)
    # with pd.ExcelWriter('sampleCount.xlsx') as writer:
    #     stratified_report.to_excel(writer)

    stratified_sample = DS.stratified_sample(df, ['isFraud'])
    print(stratified_sample)

if __name__ == "__main__":
    main()
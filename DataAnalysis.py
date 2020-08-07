import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# get Fraud df for a look
def get_isFraudTrue(df):

    new_df = df.loc[df['isFraud'] == True]
    new_df = new_df.replace(r'^\s*$', np.nan, regex=True)
    new_df.to_excel('Fraud_data.xls')

    fraud_grpd = df.groupby('isFraud').size()
    print(fraud_grpd)
    FvV = [0,0]
    FvV[0] = fraud_grpd[1]
    FvV[1] = fraud_grpd[0]

    # pie chart
    labels = ['Fraudulent', 'Valid']
    plt.pie(FvV, labels=labels, startangle=45, shadow= False, radius=1.2, autopct='%1.2f%%')
    plt.show()

def accNum_check(df):

    accNum = np.sort(df['accountNumber'].unique())
    FvV = []
    report = []

    accNum_grpd = df.groupby(['accountNumber', 'isFraud']).size()
    print(accNum_grpd)
    for i in accNum:
        valid = max(accNum_grpd.loc[i, 0], 0)
        fraud = max(accNum_grpd.loc[i, 1], 0)
        FvV.append([fraud, valid])
        if fraud/(fraud+valid) > 0.15:
            report.append(i)

    print(accNum)
    print(FvV)
    print(report)

# DONE - v2
def overdraw_check(df):

    overdrawY = [ df.loc[(df['overDraw'] == 1) & (df['isFraud'] == True)].count()['isFraud'],
                  df.loc[(df['overDraw'] == 1) & (df['isFraud'] == False)].count()['isFraud']]
    overdrawN = [ df.loc[(df['overDraw'] == 0) & (df['isFraud'] == True)].count()['isFraud'],
                  df.loc[(df['overDraw'] == 0) & (df['isFraud'] == False)].count()['isFraud']]

    # probabilities
    total = overdrawY[0] + overdrawY[1] + overdrawN[0] + overdrawN[1]
    print("total = " + str(total))
    print("overdrawn")
    print(overdrawY)
    print("not overdrawn")
    print(overdrawN)
    print("\nProbability of overdrawn and fraudulent transaction = " + str(overdrawY[0]/total))
    print("\nProbability of not overdrawn and fraudulent transaction = " + str(overdrawN[0]/total))

    # bar chart
    left = [1, 2, 3, 4]
    height = [overdrawY[0], overdrawY[1], overdrawN[0], overdrawN[1]]
    tick_label = ['Overdrawn-Fraud', 'Overdrawn-Valid', 'Not Overdrawn-Fraud', 'Not Overdrawn-Valid']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.show()

    # pie chart
    labels = ['Overdrawn', 'Not Overdrawn']
    slices = [overdrawY[0], overdrawN[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def creditLimit_check(df):

    credLimitList = np.sort(df['creditLimit'].unique())
    FvV = []
    labels = []
    slices = []

    credLim_grpd = df.groupby(['creditLimit', 'isFraud']).size()
    for i in credLimitList:
        FvV.append([ credLim_grpd.loc[i, 1], credLim_grpd[i, 0]])
        labels.append(i)
        slices.append(FvV[0])

    # bar chart
    length = len(credLimitList)
    left = []
    height = []
    tick_label = []

    for i in range(0, 2*length):
        left.append(i)
        height.append(FvV[int(i/2)][int(i%2)])
        if i % 2 == 0:
            tick_label.append(str(credLimitList[int(i/2)]))
        else:
            tick_label.append(str(credLimitList[int(i/2)]))

    plt.bar(left, height, tick_label=tick_label, width=0.5, color=['red','green'])
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, radius = 1.2, autopct = '%1.2f%%')
    plt.legend()
    plt.show()

# Can something more be done?
def merchName_check(df):

    merchNames = df['merchantName'].unique()
    FvV = []
    # for pie chart
    labels = []
    slices = []

    merchNames_grpd = df.groupby(['merchantName']).size()
    print(merchNames_grpd)
    merchNames_grpd_FvV = df.groupby(['merchantName', 'isFraud']).size()
    print(merchNames_grpd_FvV)
    for i in merchNames:
        if merchNames_grpd_FvV.loc[i]['isFraud'] == True:
            print('works')
    #     elif merchNames_grpd_FvV['isFraud'][2*i+1] == False:
    #         FvV.append(merchNames_grpd_FvV[2*i][0], 0)
    #         slices.append(merchNames_grpd_FvV[2*i][0])
    #     else:
    #         FvV.append([merchNames_grpd_FvV[2*i][0], merchNames_grpd_FvV[2*i+1][0]])
    #         slices.append(merchNames_grpd_FvV[2*i][0])
    #     labels.append(i)
    #
    # print(merchNames_grpd)
    # print(merchNames)
    # print(FvV)
    #
    # plt.pie(slices, labels=labels, startangle=45, radius = 1.2, autopct = '%1.2f%%')
    # plt.legend()
    # plt.show()

# ADD online offline fraud distribution
def merchCat_check(df):

    merchCat = df['merchantCategoryCode'].unique()
    FvV = []
    # for pie chart
    labels = []
    slices = []

    merchCat_grpd = df.groupby(['merchantCategoryCode', 'isFraud']).size()
    print(merchCat_grpd.loc[merchCat[0]['False']])
    # for i in merchCat:
    #     fraud = merchCat_grpd.loc[i, 1]
    #     valid = merchCat_grpd[i, 0]
    #
    #     FvV.append([ fraud, valid])
    #     labels.append(i)
    #     slices.append(merchCat_grpd.loc[i, 1])
    #
    # print(merchCat_grpd)
    # print(merchCat)
    # print(FvV)
    #
    # # bar chart
    # length = len(merchCat)
    # left = []
    # height = []
    # tick_label = []
    #
    # for i in range(0, 2*length):
    #     left.append(i)
    #     height.append(FvV[int(i/2)][int(i%2)])
    #     if i % 2 == 0:
    #         tick_label.append(str(merchCat[int(i/2)]) + '-Fraud')
    #     else:
    #         tick_label.append(str(merchCat[int(i/2)] + '-Valid'))
    #
    # plt.bar(left, height, tick_label=tick_label, width=0.75, color=['red','green'])
    # plt.show()
    #
    # # pie chart
    # plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    # plt.legend()
    # plt.show()

# DONE - v2
def location_check(df):

    loc_match = [ df.loc[(df['overSeas'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                  df.loc[(df['overSeas'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    loc_differ = [ df.loc[(df['overSeas'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                 df.loc[(df['overSeas'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # probabilities
    total = loc_match[0] + loc_match[1] + loc_differ[0] + loc_differ[1]
    print("total = " + str(total))
    print("location matched")
    print(loc_match)
    print("location different")
    print(loc_differ)
    print("\nProbability of location match and fraudulent transaction = " + str(loc_match[0]/total))
    print("\nProbability of location diff and fraudulent transaction = " + str(loc_differ[0]/total))

    # bar chart
    left = [1, 2, 3, 4]
    height = [loc_match[0], loc_match[1], loc_differ[0], loc_differ[1]]
    tick_label = ['Loc Match-Fraud', 'Loc Match-Valid', 'Loc Diff-Fraud', 'Loc Diff-Valid']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.show()

    # pie chart
    labels = ['Location Match', 'Location Diff']
    slices = [loc_match[0], loc_differ[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def dateAddressChange_check(df):

    datesMatch = [ df.loc[(df['addressChangeActivity'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['addressChangeActivity'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    datesDiffer = [ df.loc[(df['addressChangeActivity'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['addressChangeActivity'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # probabilities
    total = datesMatch[0] + datesMatch[1] + datesDiffer[0] + datesDiffer[1]
    print("total = " + str(total))
    print("dates match")
    print(datesMatch)
    print("dates differ")
    print(datesDiffer)
    print("\nProbability of dates match and fraudulent transaction = " + str(datesMatch[0]/total))
    print("\nProbability of dates differ and fraudulent transaction = " + str(datesDiffer[0]/total))

    # bar chart
    left = [1, 2, 3, 4]
    height = [datesMatch[0], datesMatch[1], datesDiffer[0], datesDiffer[1]]
    tick_label = ['Dates Match-Fraud', 'Dates Match-Valid', 'Dates Differ-Fraud', 'Dates Differ-Valid']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.show()

    # pie chart
    labels = ['Dates Match', 'Dates Differ']
    slices = [datesMatch[0], datesDiffer[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def posEntryMode_check(df):

    posEntryModes = df['posEntryMode'].unique()
    FvV = []
    # for pie chart
    labels = []
    slices = []

    posEntryModes_grpd = df.groupby(['posEntryMode', 'isFraud']).size()
    for i in posEntryModes:
        FvV.append([ posEntryModes_grpd.loc[i, 1], posEntryModes_grpd[i, 0]])
        labels.append(i)
        slices.append(posEntryModes_grpd.loc[i, 1])

    print(posEntryModes_grpd)
    print(posEntryModes)
    print(FvV)

    # bar chart
    length = len(posEntryModes)
    left = []
    height = []
    tick_label = []

    for i in range(0, 2*length):
        left.append(i)
        height.append(FvV[int(i/2)][int(i%2)])
        if i % 2 == 0:
            tick_label.append(str(posEntryModes[int(i/2)]) + '-Fraud')
        else:
            tick_label.append(str(posEntryModes[int(i/2)] + '-Valid'))

    plt.bar(left, height, tick_label=tick_label, width=0.75, color=['red','green'])
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def posCond_check(df):

    posConds = df['posConditionCode'].unique()
    FvV = []
    # for pie chart
    labels = []
    slices = []

    posConds_grpd = df.groupby(['posConditionCode', 'isFraud']).size()
    for i in posConds:
        FvV.append([ posConds_grpd.loc[i, 1], posConds_grpd[i, 0]])
        labels.append(i)
        slices.append(posConds_grpd.loc[i, 1])

    print(posConds_grpd)
    print(posConds)
    print(FvV)

    # bar chart
    length = len(posConds)
    left = []
    height = []
    tick_label = []

    for i in range(0, 2*length):
        left.append(i)
        height.append(FvV[int(i/2)][int(i%2)])
        if i % 2 == 0:
            tick_label.append('Code ' + str(posConds[int(i/2)]) + '-Fraud')
        else:
            tick_label.append('Code ' + str(posConds[int(i/2)] + '-Valid'))

    plt.bar(left, height, tick_label=tick_label, width=0.75, color=['red','green'])
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def CVV_check(df):

    CVVmatch = [ df.loc[(df['cvvMatch'] == 1) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['cvvMatch'] == 1) & (df['isFraud'] == False)].count()['isFraud']]
    CVVdiffer = [ df.loc[(df['cvvMatch'] == 0) & (df['isFraud'] == True)].count()['isFraud'],
                      df.loc[(df['cvvMatch'] == 0) & (df['isFraud'] == False)].count()['isFraud']]

    # probabilities
    total = CVVmatch[0] + CVVmatch[1] + CVVdiffer[0] + CVVdiffer[1]
    print("Total = " + str(total))
    print("CVVs Match")
    print(CVVmatch)
    print("CVVs Differ")
    print(CVVdiffer)
    print("\nProbability of CVV entered correctly and fraudulent transaction = " + str(CVVmatch[0]/total))
    print("\nProbability of CVV entered incorrectly and fraudulent transaction = " + str(CVVdiffer[0]/total))

    # bar chart
    left = [1, 2, 3, 4]
    height = [CVVmatch[0], CVVmatch[1], CVVdiffer[0], CVVdiffer[1]]
    tick_label = ['CVV Correct-Fraud', 'CVV Correct-Valid', 'CVV Incorrect-Fraud', 'CVV Incorrect-Valid']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.show()

    # pie chart
    labels = ['CVV Correct', 'CVV Incorrect']
    slices = [CVVmatch[0], CVVdiffer[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def transactionType_check(df):

    transactionTypes = df['transactionType'].unique()
    FvV = []
    # for pie chart
    labels = []
    slices = []

    transType_grpd = df.groupby(['transactionType', 'isFraud']).size()
    for i in transactionTypes:
        FvV.append([ transType_grpd.loc[i, 1], transType_grpd[i, 0]])
        labels.append(i)
        slices.append(transType_grpd.loc[i, 1])

    # bar chart
    length = len(transactionTypes)
    left = []
    height = []
    tick_label = []

    for i in range(0, 2*length):
        left.append(i)
        height.append(FvV[int(i/2)][int(i%2)])
        if i % 2 == 0:
            tick_label.append(str(transactionTypes[int(i/2)]) + '-Fraud')
        else:
            tick_label.append(str(transactionTypes[int(i/2)]) + '-Valid')

    plt.bar(left, height, tick_label=tick_label, width=0.75, color=['red','green'])
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def card_check(df):

    cardPresent = [ df.loc[(df['cardPresent'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['cardPresent'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    cardAbsent = [ df.loc[(df['cardPresent'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                   df.loc[(df['cardPresent'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # # probabilities
    total = cardPresent[0] + cardPresent[1] + cardAbsent[0] + cardAbsent[1]
    print("total = " + str(total))
    print("card present")
    print(cardPresent)
    print("card absent")
    print(cardAbsent)
    print("\nProbability of card present and fraudulent transaction = " + str(cardPresent[0]/total))
    print("\nProbability of card absent and fraudulent transaction = " + str(cardAbsent[0]/total))

    # bar chart
    left = [1, 2, 3, 4]
    height = [cardPresent[0], cardPresent[1], cardAbsent[0], cardAbsent[1]]
    tick_label = ['Card Present-Fraud', 'Card Present Valid', 'Card Absent-Fraud', 'Card Absent-Valid']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.show()

    # pie chart
    labels = ['Card Present', 'Card Absent']
    slices = [cardPresent[0], cardAbsent[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# DONE - v2
def expDateMatched_check(df):

    expDateMatched = [ df.loc[(df['expirationDateKeyInMatch'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                       df.loc[(df['expirationDateKeyInMatch'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    expDateDiffer = [ df.loc[(df['expirationDateKeyInMatch'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                       df.loc[(df['expirationDateKeyInMatch'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # probabilities
    total = expDateMatched[0] + expDateMatched[1] + expDateDiffer[0] + expDateDiffer[1]
    print("Total = " + str(total))
    print("Expiry key matched")
    print(expDateMatched)
    print("Expiry key different")
    print(expDateDiffer)
    print("\nProbability of expiry key match and fraudulent transaction = " + str(expDateMatched[0]/total))
    print("\nProbability of expiry key different and fraudulent transaction = " + str(expDateDiffer[0]/total))

    # bar chart
    left = [1, 2, 3, 4]
    height = [expDateMatched[0], expDateMatched[1], expDateDiffer[0], expDateDiffer[1]]
    tick_label = ['Exp Key Match-Fraud', 'Exp Key Match-Valid', 'Exp Key Diff-Fraud', 'Exp Key Diff-Valid']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.show()

    # pie chart
    labels = ['Exp Key Matched', 'Exp Key Diff']
    slices = [expDateMatched[0], expDateDiffer[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()
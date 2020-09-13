import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def scatter_plot(df, feature, target):

    plt.figure(figsize=(16, 8))
    plt.scatter(
        df[feature],
        df[target],
        c='black'
    )
    plt.xlabel(feature)
    plt.ylabel(target)
    plt.show()

def pairwise_correlation(df):

    corr = df.corr()
    print(corr)
    sns.heatmap(corr, annot=True)
    plt.show()

def get_isFraudTrue(df):

    # EXPORT FRAUD DATA TO EXCEL (for a look)
    # new_df = df.loc[df['isFraud'] == True]
    # new_df = new_df.replace(r'^\s*$', np.nan, regex=True)
    # new_df.to_excel('Fraud_data.xls')

    fraud_grpd = df.groupby('isFraud').size()
    print(fraud_grpd)
    FvV = [0,0]
    FvV[0] = fraud_grpd[1]
    FvV[1] = fraud_grpd[0]

    # pie chart
    labels = ['Fraudulent', 'Valid']
    plt.pie(FvV, labels=labels, startangle=45, shadow= False, radius=1.2, autopct='%1.2f%%')
    plt.show()

def creditLimit_check(df, df_adjusted):

    credLimitList = np.sort(df['creditLimit'].unique())
    FvV = []
    labels = []
    slices = []

    credLim_grpd = df.groupby(['creditLimit', 'isFraud']).size()
    for i in credLimitList:
        F = credLim_grpd.loc[i, 1]
        V = credLim_grpd[i, 0]
        FvV.append([F,V])
        labels.append(i)
        slices.append(F)

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='creditLimit', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Division by credit limit - V:F = 98.42:1.58')
    a1 = sns.countplot(x='creditLimit', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Division by credit limit - V:F = 7:3')
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, radius = 1.2, autopct = '%1.2f%%')
    plt.legend()
    plt.show()

def overdraw_check(df, df_adjusted):

    overdrawY = [ df.loc[(df['overDraw'] == 1) & (df['isFraud'] == True)].count()['isFraud'],
                  df.loc[(df['overDraw'] == 1) & (df['isFraud'] == False)].count()['isFraud']]
    overdrawN = [ df.loc[(df['overDraw'] == 0) & (df['isFraud'] == True)].count()['isFraud'],
                  df.loc[(df['overDraw'] == 0) & (df['isFraud'] == False)].count()['isFraud']]

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='overDraw', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Number of transactions overdrawn - V:F = 98.42:1.58')
    a1 = sns.countplot(x='overDraw', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Number of transactions overdrawn - V:F = 7:3')
    plt.show()

    # pie chart
    labels = ['Overdrawn', 'Not Overdrawn']
    slices = [overdrawY[0], overdrawN[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

# Can something more be done?
def merchName_check(df, df_adjusted):

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

# ADD online offline fraud distribution - check
def merchCat_check(df, df_adjusted):

    merchCat = df['merchantCategoryCode'].unique()
    FvV = []
    # for pie chart
    labels = []
    slices = []

    merchCat_grpd = df.groupby(['merchantCategoryCode', 'isFraud']).size()
    # print(merchCat_grpd.loc[merchCat[0,0]])
    for i in merchCat:
        fraud = merchCat_grpd.loc[i, 1]
        valid = merchCat_grpd[i, 0]

        FvV.append([ fraud, valid])
        labels.append(i)
        slices.append(merchCat_grpd.loc[i, 1])

    print(merchCat_grpd)
    print(merchCat)
    print(FvV)

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='merchantCategoryCode', hue='isFraud', ax=axes[0], data=df)
    a0.set_xticklabels(a0.get_xticklabels(), rotation=90)
    a0.set_title('Division by merchant category code - V:F = 98.42:1.58')
    a1 = sns.countplot(x='merchantCategoryCode', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_xticklabels(a1.get_xticklabels(), rotation=90)
    a1.set_title('Division by merchant category code - V:F = 7:3')
    plt.show()

    # # pie chart
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def location_check(df, df_adjusted):

    loc_match = [ df.loc[(df['overSeas'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                  df.loc[(df['overSeas'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    loc_differ = [ df.loc[(df['overSeas'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                 df.loc[(df['overSeas'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='overSeas', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Number of overseas transaction - V:F = 98.42:1.58')
    a1 = sns.countplot(x='overSeas', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Number of overseas transaction - V:F = 7:3')
    plt.show()

    # pie chart
    labels = ['Location Match', 'Location Diff']
    slices = [loc_match[0], loc_differ[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def posEntryMode_check(df, df_adjusted):

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

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='posEntryMode', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Division by posEntryMode - V:F = 98.42:1.58')
    a1 = sns.countplot(x='posEntryMode', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Division by posEntryMode - V:F = 7:3')
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def posCond_check(df, df_adjusted):

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
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='posConditionCode', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Division by posConditionCode - V:F = 98.42:1.58')
    a1 = sns.countplot(x='posConditionCode', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Division by posConditionCode - V:F = 7:3')
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def dateAddressChange_check(df, df_adjusted):

    datesMatch = [ df.loc[(df['addressChangeActivity'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['addressChangeActivity'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    datesDiffer = [ df.loc[(df['addressChangeActivity'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['addressChangeActivity'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='addressChangeActivity', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Division by address change activity - V:F = 98.42:1.58')
    a1 = sns.countplot(x='addressChangeActivity', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Division by address change activity - V:F = 7:3')
    plt.show()

    # pie chart
    labels = ['Dates Match', 'Dates Differ']
    slices = [datesMatch[0], datesDiffer[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def CVV_check(df, df_adjusted):

    CVVmatch = [ df.loc[(df['cvvMatch'] == 1) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['cvvMatch'] == 1) & (df['isFraud'] == False)].count()['isFraud']]
    CVVdiffer = [ df.loc[(df['cvvMatch'] == 0) & (df['isFraud'] == True)].count()['isFraud'],
                      df.loc[(df['cvvMatch'] == 0) & (df['isFraud'] == False)].count()['isFraud']]

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='cvvMatch', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Division by cvvMatch - V:F = 98.42:1.58')
    a1 = sns.countplot(x='cvvMatch', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Division by cvvMatch - V:F = 7:3')
    plt.show()

    # pie chart
    labels = ['CVV Correct', 'CVV Incorrect']
    slices = [CVVmatch[0], CVVdiffer[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def transactionType_check(df, df_adjusted):

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
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='transactionType', hue='isFraud', ax=axes[0], data=df)
    a0.set_xticklabels(a0.get_xticklabels(), rotation=90)
    a0.set_title('Division by transactionType - V:F = 98.42:1.58')
    a1 = sns.countplot(x='transactionType', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_xticklabels(a1.get_xticklabels(), rotation=90)
    a1.set_title('Division by transactionType - V:F = 7:3')
    plt.show()

    # pie chart
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def card_check(df, df_adjusted):

    cardPresent = [ df.loc[(df['cardPresent'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                    df.loc[(df['cardPresent'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    cardAbsent = [ df.loc[(df['cardPresent'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                   df.loc[(df['cardPresent'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='cardPresent', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Division by cardPresent - V:F = 98.42:1.58')
    a1 = sns.countplot(x='cardPresent', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Division by cardPresent - V:F = 7:3')
    plt.show()

    # pie chart
    labels = ['Card Present', 'Card Absent']
    slices = [cardPresent[0], cardAbsent[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

def expDateMatched_check(df, df_adjusted):

    expDateMatched = [ df.loc[(df['expirationDateKeyInMatch'] == True) & (df['isFraud'] == True)].count()['isFraud'],
                       df.loc[(df['expirationDateKeyInMatch'] == True) & (df['isFraud'] == False)].count()['isFraud']]
    expDateDiffer = [ df.loc[(df['expirationDateKeyInMatch'] == False) & (df['isFraud'] == True)].count()['isFraud'],
                       df.loc[(df['expirationDateKeyInMatch'] == False) & (df['isFraud'] == False)].count()['isFraud']]

    # bar chart
    f, axes = plt.subplots(ncols=2, figsize=(17, 6))
    a0 = sns.countplot(x='expirationDateKeyInMatch', hue='isFraud', ax=axes[0], data=df)
    a0.set_title('Division by expiration Date Match - V:F = 98.42:1.58')
    a1 = sns.countplot(x='expirationDateKeyInMatch', hue='isFraud', ax=axes[1], data=df_adjusted)
    a1.set_title('Division by expiration Date Match - V:F = 7:3')
    plt.show()

    # pie chart
    labels = ['Exp Key Matched', 'Exp Key Diff']
    slices = [expDateMatched[0], expDateDiffer[0]]
    plt.pie(slices, labels=labels, startangle=45, shadow=False, radius=1.2, autopct='%1.2f%%')
    plt.legend()
    plt.show()

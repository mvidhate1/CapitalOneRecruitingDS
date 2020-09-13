import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, StratifiedKFold
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import Models

def strat_sample(df, feature_cols):

    tmp_v = df.loc[df['isFraud'] == 0].sample(n=28974, random_state=1)
    tmp_f = df.loc[df['isFraud'] == 1]
    df_final = pd.concat([tmp_v, tmp_f])

    df_final = df_final[feature_cols]
    y = df_final.loc[:, 'isFraud']
    X = df_final.loc[:, [i for i in df_final.columns.values if i != 'isFraud']]

    # FIND max accuracy and corresponding no. of features
    # nof_list = np.arange(1, 439)
    # high_score = 0
    # Variable to store the optimum features
    # nof = 0
    # score_list = []
    # for n in range(len(nof_list)):
    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33333, random_state=0)
    #     model = LogisticRegression(solver='liblinear', C=10.0)
    #     rfe = RFE(estimator=model, n_features_to_select=nof_list[n])
    #     X_train_rfe = rfe.fit_transform(X_train, y_train)
    #     X_test_rfe = rfe.transform(X_test)
    #     model.fit(X_train_rfe, y_train)
    #     score = model.score(X_test_rfe, y_test)
    #     score_list.append(score)
    #     if (score > high_score):
    #         high_score = score
    #         nof = nof_list[n]
    # print("Optimum number of features: %d" % nof)
    # print("Score with %d features: %f" % (nof, high_score))

    # SPLIT DATASET INTO TRAIN AND TEST
    # original data
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33333, random_state=2)
    # Models.log_Reg(X_train, y_train, X_test, y_test, 400)
    # Models.lasso_Reg(X_train, y_train, X_test, y_test, 400)

    skf = RepeatedStratifiedKFold(n_splits=5, n_repeats=1)
    fold = 0
    logreg_score = []
    lghs = 0
    lassoreg_score = []
    lshs = 0

    for train, test in skf.split(X, y):
        fold += 1
        print("FOLD = ", fold)
        print(' Train: ', train, '\n Test: ', test)
        X_train, X_test = X.iloc[train], X.iloc[test]
        y_train, y_test = y.iloc[train], y.iloc[test]
        lgs = Models.log_Reg(X_train, y_train, X_test, y_test, 439, fold)
        logreg_score.append(lgs)
        if lgs > lghs:
            lghs = lgs
        lss = Models.lasso_Reg(X_train, y_train, X_test, y_test, 439, fold)
        lassoreg_score.append(lss)
        if lss > lshs:
            lshs = lss

    print('LogReg\n HighScore = ', lghs, '\n Mean = ', np.mean(logreg_score), '\n Std = ', np.std(logreg_score))
    print('LassoReg\n HighScore = ', lshs, '\n Mean = ', np.mean(lassoreg_score), ';\n Std = ', np.std(lassoreg_score))

    # TO FIND IMPORTANT FEATURES (based on feature coefficients)
    # cols = X.columns.values.tolist()
    # features = []
    # for sublist in lss.coef_:
    #     for i in sublist:
    #         if abs(i) > 0.5:
    #             ind_list = np.where(sublist == i)
    #             j = 0
    #             while ind_list[0][j] in features:
    #                 j += 1
    #             ind = ind_list[0][j]
    #             features.append(ind)
    #             print(cols[ind])
    # print(lgs.coef_, lgs.intercept_)
    # print(X.columns.values)
    # print(lss.coef_, lss.intercept_)

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn import metrics
import matplotlib.pyplot as plt

def log_Reg(X_train, y_train, X_test, y_test, nof, fold):

    logreg = LogisticRegression(solver='liblinear', C=10.0)
    rfe = RFE(estimator=logreg, n_features_to_select=nof)
    X_train_rfe = rfe.fit_transform(X_train, y_train)
    X_test_rfe = rfe.transform(X_test)
    logreg.fit(X_train_rfe,y_train)

    print("LOGREG")
    # check on train data
    y_pred = logreg.predict(X_train_rfe)
    visualize(logreg, 'train', X_train_rfe, y_train, y_pred, fold)
    # check on test data
    y_pred = logreg.predict(X_test_rfe)
    visualize(logreg, 'test', X_test_rfe, y_test, y_pred, fold)

    # print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
    print('-----')

    return logreg.score(X_test_rfe, y_test)

def lasso_Reg(X_train, y_train, X_test, y_test, nof, fold):

    lassoreg = LogisticRegression(penalty='l1', solver='liblinear', C=10.0)
    # can also use solver='saga'
    rfe = RFE(estimator=lassoreg, n_features_to_select=nof)
    X_train_rfe = rfe.fit_transform(X_train, y_train)
    X_test_rfe = rfe.transform(X_test)
    lassoreg.fit(X_train_rfe, y_train)

    print("LASSO")
    # check on train data
    y_pred = lassoreg.predict(X_train_rfe)
    visualize(lassoreg, 'train', X_train_rfe, y_train, y_pred, fold)
    # check on test data
    y_pred = lassoreg.predict(X_test_rfe)
    visualize(lassoreg, 'test', X_test_rfe, y_test, y_pred, fold)

    # print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
    print('-----')

    return lassoreg.score(X_test_rfe, y_test)

def visualize(reg, type, X_test, y_test, y_pred, fold):

    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    print(cnf_matrix)

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))

    # ROC - AUC
    y_pred_proba = reg.predict_proba(X_test)[::, 1]
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    if type == 'train' and fold == 1:
        plt.plot(fpr, tpr, label="ROC-%s (train)(AUC=%0.5f)(Fold=%d)" %(reg,auc,fold))
    elif type == 'test':
        plt.plot(fpr, tpr, label="ROC-%s (test)(AUC=%0.5f)(Fold=%d)" %(reg,auc,fold))
    plt.xlabel('False +ve Rate (1-Specificity)')
    plt.ylabel('True +ve Rate (Sensitivity)')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.legend(loc='lower right')

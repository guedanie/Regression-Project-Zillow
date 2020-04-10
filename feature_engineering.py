# We used SelectKBest to select the top 2 features based on how correlated each feature is with the target variable. We ended up with exam1 and exam3.
# We use RFE and a linear regression algorithm to keep the top 2 features based on which features lead to the best performing linear regression model.
# This eliminated exam2 and also left us with exam1 and exam3, like SelectKBest.

from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectKBest, f_regression

def select_kbest(X, y, k):
    f_selector = SelectKBest(f_regression, k=k)
    f_selector.fit(X, y)
    X_reduced = f_selector.transform(X)
    f_support = f_selector.get_support()
    f_feature = X.loc[:,f_support].columns.tolist()
    print(str(len(f_feature)), 'selected features')
    print(f_feature)

def rfe(X, y, k):
    lm = LinearRegression()
    rfe = RFE(lm, k)
    X_rfe = rfe.fit_transform(X, y)
    lm.fit(X_rfe, y)
    mask = rfe.support_
    rfe_features = X.loc[:,mask].columns.tolist()
    print(str(len(rfe_features)), 'selected features')
    print(rfe_features)

def optimal_number_of_features(x, y):   
    """
    Takes:
          x_train: Pandas df
          y_train: Pandas df
    Returns:
          int: number of optimum features
          score
    """ 
    features_range = range(1, len(x.columns)+1)
    high_score = 0
    number_of_features = 0
    for n in features_range:
        model = LinearRegression()
        train_rfe = RFE(model, n).fit_transform(x, y)
        model.fit(train_rfe, y)
        score = model.score(train_rfe, y)
        if(score > high_score):
            high_score = score
            number_of_features = n
    return number_of_features, score
import access
import numpy as np
from sklearn.model_selection import KFold
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures


def do_linear_regression(type_id, model_class, **kwargs):
    matrix = access.item_matrix(type_id) # item id of abyssal magstab
    data = np.array(matrix)
    x = data[:, 1:]
    y = data[:, 0]

    kfold = KFold(n_splits=5)
    mses = []
    dummy_mses = []
    for train, test in kfold.split(x, y):
        linear_reg_model = model_class(normalize=True, **kwargs)
        linear_reg_model.fit(x[train], y[train])
        y_pred = linear_reg_model.predict(x[test])

        dummy_model = DummyRegressor(strategy='mean')
        dummy_model.fit(x[train], y[train])
        dummy_pred = dummy_model.predict(x[test])

        mses.append(mean_squared_error(y[test], y_pred))
        dummy_mses.append(mean_squared_error(y[test], dummy_pred))
    mse = np.array(mses).mean()
    dummy_mse = np.array(dummy_mses).mean()

    print(f'{model_class.__name__} Mean Squared Error: {mse}')
    print(f'Dummy Classifier (Mean) Mean Squared Error: {dummy_mse}')
    print(f'Percentage Difference: {(abs(mse - dummy_mse)/mse) * 100}%')


def do_regression_cross_val(type_id, model_class):
    matrix = access.item_matrix(type_id)  # item id of abyssal magstab
    data = np.array(matrix)
    x = data[:, 1:]
    y = data[:, 0]

    # cross_val
    alphas = [0.0001, 0.001, 0.01, 0.1, 1]
    kfold = KFold(n_splits=5)
    alpha_mses = []
    alpha_std_devs = []
    for alpha in alphas:
        mses = []
        for train, test in kfold.split(x, y):
            ridge_model = model_class(alpha=alpha, normalize=True)
            ridge_model.fit(x[train], y[train])
            y_pred = ridge_model.predict(x[test])
            mses.append(mean_squared_error(y[test], y_pred))
        mses = np.array(mses)
        alpha_mses.append(mses.mean())
        alpha_std_devs.append(mses.std())

    plt.errorbar(alphas, alpha_mses, alpha_std_devs)
    plt.title(f'{model_class.__name__} 5-Fold Cross-Validation for Alpha')
    plt.xlabel('alpha')
    plt.ylabel('mean squared error (w/ standard deviation)')
    plt.show()


def do_polynomial_reg(type_id, model_class):
    matrix = access.item_matrix(type_id) # item id of abyssal magstab
    data = np.array(matrix)
    x = data[:, 1:]
    y = data[:, 0]

    kf = KFold(n_splits=5)
    q_values = [1,2,3,4,5,6]
    mean_error=[]
    std_error=[]

    for q in q_values:
        Xpoly = PolynomialFeatures(q).fit_transform(x)
        model = model_class(normalize=True)
        temp=[]
        plotted = False
        
        for train, test in kf.split(Xpoly):
            model.fit(Xpoly[train], y[train])
            ypred = model.predict(Xpoly[test])
            temp.append(mean_squared_error(y[test],ypred))
        
        mean_error.append(np.array(temp).mean())
        std_error.append(np.array(temp).std())
    
    
    for i in range(len(mean_error)):
        print('The mean error for q=', i+1, 'is', mean_error[i], '\n')
    
    plt.errorbar(q_values,mean_error,yerr=std_error,linewidth=3)
    plt.xlabel('q')
    plt.ylabel('Mean square error')
    plt.show()

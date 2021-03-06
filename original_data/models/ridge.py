import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
from sklearn.linear_model import Ridge
from evaluate_models import EvaluateModels
from cross_validation import CrossValidation

cross_validate = CrossValidation()
evaluate = EvaluateModels()

data = pd.read_csv("../../data/formatted_data_new.csv")
days = data.iloc[:, 0]
cases = data.iloc[:, 1]
traffic = data.iloc[:, 2]

cases_df = cases
traffic_df = traffic
cases = pd.DataFrame(cases).to_numpy()
traffic = pd.DataFrame(traffic).to_numpy()
cases = cases.reshape(-1, 1)

# Choose optimal KFold
print("Performing Cross Validation...")
cross_validate.k_folds_cross_validation(
    1, cases, traffic, days, pred_type='cases', model_type='ridge', Q=1, K='N/A', C=10)

# Choose optimal polynomial features
cross_validate.poly_feature_cross_validation(
    2, cases, traffic, days, pred_type='cases', model_type='ridge', folds=2, K='N/A', C=10)

# Choose optimal value for C penalty
cross_validate.c_penalty_cross_validation(
    3, cases, traffic, days, pred_type='cases', model_type='ridge', folds=2, Q=5, K='N/A')

# TRAFFIC ==> CASES
kf = KFold(n_splits=5)
plt.figure(5)
plt.plot(days, cases)
y = []
p = []
for train, test in kf.split(traffic):
    a = 1/2*10
    model = Ridge(alpha=a).fit(traffic[train], cases[train])
    predictions = model.predict(traffic[test])
    predictions = [round(num[0]) for num in predictions]

    plt.plot(days[test], predictions, c="lime")

    y = y + cases[test].tolist()
    p = p + predictions

evaluate.evaluate_model(
    pred_type='cases', model_type='Ridge', y=y, y_pred=p)
plt.title("Ridge Model using traffic to predict cases")
plt.xlabel("Days")
plt.ylabel("Cases")
plt.legend(["training cases", "predicted cases"])
plt.show()


# CASES ==> TRAFFIC
kf = KFold(n_splits=5)
y = []
p = []
plt.figure(5)
plt.plot(days, traffic)
for train, test in kf.split(cases):
    a = 1/2*0.0001
    model = Ridge(alpha=a).fit(cases[train], traffic[train])
    predictions = model.predict(cases[test])
    predictions = [round(num[0]) for num in predictions]

    plt.plot(days[test], predictions, c="lime")

    y = y + traffic[test].tolist()
    p = p + predictions

evaluate.evaluate_model(
    pred_type='traffic', model_type='Ridge', y=y, y_pred=p)
plt.title("Ridge Model using cases to predict traffic")
plt.xlabel("Days")
plt.ylabel("Traffic")
plt.legend(["training traffic", "predicted traffic"])
plt.show()

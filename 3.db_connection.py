import pymysql
import pandas as pd
import numpy as np
from sklearn.base import is_regressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import column_or_1d#
from sklearn.model_selection import StratifiedKFold #k폴드 교차검증
from sklearn.metrics import accuracy_score #정확도 측정
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import pickle
from sklearn.preprocessing import OneHotEncoder


opgg = pymysql.connect(host='localhost', user='root', password='1234',db='opgg_project', charset='utf8')

cursor = opgg.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM opgg_crawling_1000;"
cursor.execute(sql)

result = cursor.fetchall()

result = pd.DataFrame(result)

before_label = result.loc[:, ['recent_results']]
before_encoding = result.loc[:, ['Champion1','Champion2','Champion3','Champion4','Champion5','Champion6','Champion7','Champion8','Champion9','Champion10']]

print(before_label)
print(before_encoding)


#타겟
encoding_label = pd.get_dummies(before_label, columns=['recent_results'])
encoding_label = encoding_label['recent_results_win']
#데이터
encoding_data= pd.get_dummies(before_encoding, columns=['Champion1','Champion2','Champion3','Champion4','Champion5','Champion6','Champion7','Champion8','Champion9','Champion10'])
col_list = encoding_data.columns
print(col_list)

print(encoding_data)
print(encoding_label)

print(encoding_label.values)

dt_clf = DecisionTreeClassifier(random_state=11)
skfold = StratifiedKFold(n_splits=3)
n_iter = 0
cv_accuracy = []
print('데이터 세트 크기:', encoding_data.values.shape[0])


for train_index, test_index in skfold.split(encoding_data, encoding_label):
    n_iter += 1
    X_train, X_test = encoding_data.values[train_index], encoding_data.values[test_index]
    y_train, y_test = encoding_label.values[train_index], encoding_label.values[test_index]
    dt_clf.fit(X_train, y_train)
    pred = dt_clf.predict(X_test)
    print(y_test)
    print(type(y_test))
    
    accuracy = np.around(accuracy_score(y_test, pred), 4)
    cv_accuracy.append(accuracy)

print('교차 검증별 정확도:', np.round(cv_accuracy, 4))
print('평균 검증 정확도:', np.mean(cv_accuracy))
print(n_iter)


#시각화
# plt.figure(figsize=(10,7))
# plot_tree(dt_clf,max_depth=100, filled=True)
# plt.show()
# print('예측도 정확도: {0:4f}'.format(accuracy_score(y_test,pred)))

with open('opgg.pkl', 'wb') as fw:
    pickle.dump(dt_clf, fw)
with open('columns.pkl', 'wb') as fw:
    pickle.dump(col_list, fw)
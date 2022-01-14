from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

model = pickle.load(open('opgg.pkl','rb'))
columns = pickle.load(open('columns.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def home():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    data5 = request.form['e']
    data6 = request.form['f']
    data7 = request.form['g']
    data8 = request.form['h']
    data9 = request.form['i']
    data10 = request.form['j']
    new_data = pd.DataFrame(data =list(zip(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10)),columns=['Champion1','Champion2','Champion3','Champion4','Champion5','Champion6','Champion7','Champion8','Champion9','Champion10'])
    print(new_data)
    new_data = pd.get_dummies(new_data)
    new_data = new_data.reindex(columns = columns, fill_value=0)
    
    pred = model.predict(new_data.values)
    return render_template('after.html', data=pred[0])

if __name__ == "__main__":
    app.run(debug=True)
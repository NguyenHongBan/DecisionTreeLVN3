from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import copy

app = Flask(__name__)

dataset = pd.read_csv('tennis.csv')
X = dataset.iloc[:, 1:].values
# print(X)
attribute = ['outlook', 'temp', 'humidity', 'wind']


class Node(object):
    def __init__(self):
        self.value = None
        self.decision = None
        self.childs = None


def findEntropy(data, rows):
    yes = 0
    no = 0
    ans = -1
    idx = len(data[0]) - 1
    entropy = 0
    for i in rows:
        if data[i][idx] == 'Yes':
            yes = yes + 1
        else:
            no = no + 1

    x = yes/(yes+no)
    y = no/(yes+no)
    if x != 0 and y != 0:
        entropy = -1 * (x*math.log2(x) + y*math.log2(y))
    if x == 1:
        ans = 1
    if y == 1:
        ans = 0
    return entropy, ans


def findMaxGain(data, rows, columns):
    maxGain = 0
    retidx = -1
    entropy, ans = findEntropy(data, rows)
    if entropy == 0:
        """if ans == 1:
            print("Yes")
        else:
            print("No")"""
        return maxGain, retidx, ans

    for j in columns:
        mydict = {}
        idx = j
        for i in rows:
            key = data[i][idx]
            if key not in mydict:
                mydict[key] = 1
            else:
                mydict[key] = mydict[key] + 1
        gain = 0

        # print(mydict)
        for key in mydict:
            yes = 0
            no = 0
            for k in rows:
                if data[k][j] == key:
                    if data[k][-1] == 'Yes':
                        yes = yes + 1
                    else:
                        no = no + 1
            # print(yes, no)
            x = yes/(yes+no)
            y = no/(yes+no)
            # print(x, y)
            if x != 0 and y != 0:
                gain += (mydict[key] * -1*(x*math.log2(x) + y*math.log2(y)))/len(rows)
        # print(gain)
        gain = entropy - gain
        if gain > maxGain:
            # print("hello")
            maxGain = gain
            retidx = j

    return maxGain, retidx, ans


def buildTree(data, rows, columns):

    maxGain, idx, ans = findMaxGain(X, rows, columns)
    root = Node()
    root.childs = []
    # print(maxGain
    #
    # )
    if maxGain == 0:
        if ans == 1:
            root.value = 'Yes'
        else:
            root.value = 'No'
        return root
    root.value = attribute[idx]
    mydict = {}
    for i in rows:
        key = data[i][idx]
        if key not in mydict:
            mydict[key] = 1
        else:
            mydict[key] += 1

    newcolumns = copy.deepcopy(columns)
    newcolumns.remove(idx)
    for key in mydict:
        newrows = []
        for i in rows:
            if data[i][idx] == key:
                newrows.append(i)
        # print(newrows)
        temp = buildTree(data, newrows, newcolumns)
        temp.decision = key
        root.childs.append(temp)
    return root


def traverse(root):
    print(root.decision)
    print(root.value)

    n = len(root.childs)
    if n > 0:
        for i in range(0, n):
            traverse(root.childs[i])


def calculate():
    rows = [i for i in range(0, len(X))]
    columns = [i for i in range(0, len(X[0])-1)]
    root = buildTree(X, rows, columns)
    root.decision = 'Start'
    return root

def decision(root, myAttribute):
    if root.value == "Yes":
        return "Yes"
    else:
        if root.value == "No":  
            return "No"
        n = len(root.childs)
        if n > 0:
            for i in range(0, n):
                if(root.childs[i].decision == myAttribute[root.value]):
                    return decision(root.childs[i], myAttribute)
        return "No result"
	
  

root = calculate()

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
	myAttribute = {}
	myAttribute['outlook'] = request.form['outlook']
	myAttribute['humidity'] = request.form['humidity']
	myAttribute['temp'] = request.form['temp']
	myAttribute['wind'] = request.form['wind']
    # newResult = decision(root, myAttribute) 
    # return jsonify({'result' : newResult})
	return jsonify({'result' : decision(root, myAttribute)})

if __name__ == '__main__':
	app.run(debug=True)
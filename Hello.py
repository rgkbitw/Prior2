from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from Model import Issue
from random import random
app = Flask(__name__)
Bootstrap(app)

def getLatestData():
    B = []
    op = 0
    for i in Data:
        a = Issue(i)
        if a.state == "Open":
            op += 1
        B.append(a)
    return [B,op]

B = []
op = 0
for i in range(10):
    a = Issue({})
    a.get()
    B.append(a)
    if a.state == "Open":
        op += 1



@app.route('/<user>')
def hello_name(user):
    print(user)
    C = []
    if user == "FilterByOpen":
        for i in B:
            if i.state == "Open":
                C.append(i)
    elif user == "FilterByClosed":
        for i in B:
            if i.state == "Close":
                C.append(i)
    elif user == "refresh":
        C = getLatestData()
    else:
        ch = user[0]
        if ch == '+':
            C = sorted(B, key = lambda x : x.find(user[1:]))
        else:
            C = sorted(B, key = lambda x : x.find(user[1:]), reverse = True )
    return render_template('hello.html', issues = C, op = op , cl = len(B) - op)

if __name__ == '__main__':
   app.run(debug = True)

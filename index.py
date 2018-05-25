from flask import Flask, render_template, flash, request
import json
import uuid

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
  return render_template("index.html") 

@app.route("/home")
def home():
  return render_template("home.html") 

@app.route("/register",methods=['POST','GET'])
def register():
  data = json.loads(request.data)
  fo = open("users.txt","a")
  fo.write(data['username'])
  fo.write('|')
  fo.write(data['password'])
  fo.write('|')
  fo.write("\n")
  fo.close()
  return json.dumps({ "res": "success" })

@app.route("/login",methods=['POST','GET'])
def login():
  data = json.loads(request.data)
  username = data['username']
  password = data['password']
  fo = open("users.txt","r")
  t = fo.read().split("\n")
  x = list()
  for i in t:
      s = i.split('|')
      x.append(s)
  for i in x:
      if i[0] == username :
          if i[1] == password :
              return json.dumps({ "res": "success", "user": data['username'] })
  return json.dumps({ "res": "failed" })

@app.route("/trains",methods=['POST','GET'])
def showTrains():
    data = json.loads(request.data)
    source = data['source']
    destination = data['destination']
    fo = open('train.txt')
    t = fo.read().split("\n")
    x = list()
    
    for i in t:
        s = i.split("|")
        if s[1] == source and s[2] == destination :
            x.append(s)
    return json.dumps({"res": x})

@app.route("/reserve",methods=['POST','GET'])
def reserve():
  #Indexing of Usename And PNR into index and index1 respec
  data = json.loads(request.data) 
  username = data['user']
  train = data['train']
  date = data['date']
  pnr = str(uuid.uuid4().fields[-1])[:5]
  fr = open("index.txt")
  fo = open("index1.txt")
  ff = open("ticket.txt","a")
  t= fr.read().split("\n")
  p = fo.read().split("\n")
  fr.close()
  fo.close()
  pos = ff.tell()
  ff.write(username)
  ff.write('|')
  ff.write(train)
  ff.write('|')
  ff.write(date)
  ff.write('|')
  ff.write(pnr)
  x = [[ username, pos]]
  y = [[ pnr, pos]]
  ff.close()
  for i in t :
      s = i.split('|')
      x.append(s)
  for i in p :
      s = i.split('|')
      y.append(s)
  data = sorted(x, key=lambda y: y[0])
  data1 = sorted(y, key=lambda x: x[0])
  fw = open("index.txt","w")
  fw1 = open("index1.txt","w")
  for i in data :
      for j in i :
          fw.write(str(j))
          fw.write("|")
      fw.write("\n")
  for i in data1 :
      for j in i :
          fw1.write(str(j))
          fw1.write("|")
      fw1.write("\n")
  fw1.close()         
  return json.dumps({ "res": "done", "date": date, "train": train })

        

@app.route("/view",methods=['POST','GET'])
def view():
        username = request.form['usrename']
        fr = open("index.txt")
        t = fr.read().split("\n")
        x = list()
        for i in t:
            s = i.split('|')
            x.append(s)
        pos = list()
        for i in x:
            if i[0] == username :
                pos.append(i[1])
        fr.close()
        fr = open("ticket.txt","r")
        data= list()
        for i in pos:
            fr.seek(i,0)
            data.append(fr.readline())
        return json.dumps({"res":data})
                
def binarySearch (arr, l, r, x):
    if r >= l:
        mid = l + (r - l)/2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, l, mid-1, x)
        else:
            return binarySearch(arr, mid+1, r, x)
    else:
        return -1            


@app.route("/cancel",methods=['POST','GET'])
def cancel():
        username = request.form['username']
        pnr = request.form['pnr']
        fo = open("index1.txt")
        t = fo.read().split("\n")
        fo.close()
        x = list()
        for i in t :
            s = i.split('|')
            x.append(s)
        r = binarySearch( x, 0, len(x)-1, pnr)
        if r == -1 :
            return json.dumps({"res":"not Found"})
        pos = x[r][1]
        fo = open("index1.txt","r+b")
        fo.seek(pos)
        d = fo.readline()
        t = fo.read().split('\n')
        fo.seek(0)
        for i in t:
            if i != d:
                fo.write(i)
                fo.write("\n")
        fo.truncate()
        fo.close()
        fo = open("index.txt")
        t = fo.read().split("\n")
        fo.close()
        x = list()
        for i in t :
            s = i.split('|')
            x.append(s)
        r = binarySearch( x, 0, len(x)-1, username)
        if r == -1 :
            return json.dumps({"res":"not Found"})
        pos = x[r][1]
        fo = open("index.txt","r+b")
        fo.seek(pos)
        d = fo.readline()
        t = fo.read().split('\n')
        fo.seek(0)
        for i in t:
            if i != d:
                fo.write(i)
                fo.write("\n")
        fo.truncate()
        fo.close()                
        return json.dumps({"res":"record deleted successfully"})                    



if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True, port=4000)
from flask import Flask, render_template,redirect,url_for,request
from urllib.request import urlopen
import pysolr

app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def home():
    if request.method =="POST":
        a = request.form["sval"]
        b = request.form["POIstate"]
        c = request.form["LANGstate"]
        d = request.form["Lstate"]
        #e = request.form["Tstate"]
        print('submitted')
        return redirect(url_for("result", a=a, b=b, c=c, d=d))
    else:
        return render_template("home.html")

@app.route('/results', methods=["POST","GET"])
def result():
    filters = []
#SEARCH
    if(request.args['a'] ==""):
        srch = 'tweet_text: *'
    else:
        srch = "tweet_text: " + request.args['a']
#POINAME
    if(request.args['b'] =="Select"):
        poiname = ""
    else:
        poiname = "poi_name: " + request.args['b']
    filters.append(poiname)
#LANGUAGE
    if(request.args['c'] =="Select"):
        lang = ""
    else:
        lang = "lang: " + request.args['c']
    filters.append(lang)
#COUNTRY
    if(request.args['d'] =="Select"):
        country = ""
    else:
        country = "country: " + request.args['d']
    filters.append(country)

    print(srch)
    print(filters)
    solr = pysolr.Solr('http://34.235.148.250:8983/solr/IRF20P4/')
    result = solr.search(srch, fq=filters)
    num = result.raw_response['response']['numFound']
    top5 = []
    print(num)
    return render_template("result.html", num=num)

@app.route('/insights')
def insights():
    return render_template("insights.html")

@app.route('/solrget', methods=["POST","GET"])
def solr():

    return render_template("insights.html")



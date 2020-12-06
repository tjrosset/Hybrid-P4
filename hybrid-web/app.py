from flask import Flask, render_template,redirect,url_for,request
from urllib.request import urlopen
import pysolr

app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def home():
    if request.method =="POST":
        a = request.form["sval"]
        b = "Select"
        c = "Select"
        d = "Select"
        e = "Select"
        print('submitted')
        return redirect(url_for("result", a=a, b=b, c=c, d=d))
    else:
        return render_template("home.html")

@app.route('/results', methods=["POST","GET"])
def result():
    if request.method =="POST":
        a = request.form["sval"]
        b = request.form["POIstate"]
        c = request.form["LANGstate"]
        d = request.form["Lstate"]
        #e = request.form["Tstate"]
        print('submitted')
        return redirect(url_for("result", a=a, b=b, c=c, d=d))
    else:
        filters = []
        topposts = []
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
        result = solr.search(srch, fq=filters, rows=20)
        num = result.raw_response['response']['numFound']
        x=0
        if num<15:
            while x<num:
                tweet=[]
                tweet.append(result.raw_response['response']['docs'][x]['user.screen_name'])
                tweet.append(result.raw_response['response']['docs'][x]['full_text'])
                tweet.append(result.raw_response['response']['docs'][x]['country'])
                tweet.append(result.raw_response['response']['docs'][x]['created_at'])
                tweet.append(result.raw_response['response']['docs'][x]['retweet_count'])
                tweet.append(result.raw_response['response']['docs'][x]['favorite_count'])
                topposts.append(tweet)
                x+=1
        else:
            while x!=15:
                tweet=[]
                tweet.append(result.raw_response['response']['docs'][x]['user.screen_name'])
                tweet.append(result.raw_response['response']['docs'][x]['full_text'])
                tweet.append(result.raw_response['response']['docs'][x]['country'])
                tweet.append(result.raw_response['response']['docs'][x]['created_at'])
                tweet.append(result.raw_response['response']['docs'][x]['retweet_count'])
                tweet.append(result.raw_response['response']['docs'][x]['favorite_count'])
                topposts.append(tweet)
                x+=1
        print(num)
        return render_template("result.html", num=num , top = topposts, quey = srch)

@app.route('/insights')
def insights():
    return render_template("insights.html")




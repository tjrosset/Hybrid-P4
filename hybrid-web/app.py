from flask import Flask, render_template,redirect,url_for,request
from urllib.request import urlopen
from GoogleNews import GoogleNews
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
        return redirect(url_for("result", a=a, b=b, c=c, d=d))
    else:
        filters = []
        topposts = []
        placeholder =''
        testname = ''
    #SEARCH
        if(request.args['a'] ==""):
            srch = 'tweet_text: *'
            placeholder= ''
        else:
            srch = "tweet_text: " + request.args['a']
            placeholder = request.args['a']

    #POINAME
        if(request.args['b'] =="Select"):
            poilimit = "-poi_name: null"
            poilimit1 = "-poi_name: none"
            gpoi=''
            filters.append(poilimit)
            filters.append(poilimit1)
        else:
            poiname = "poi_name: " + request.args['b']
            gpoi = request.args['b']
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
        print("------Solr Query------")
        print(srch)
        print(filters)
    #-------------pysolr search------------
        solr = pysolr.Solr('http://18.234.178.228:8983/solr/IRF20P4/')
        result = solr.search(srch, fq=filters, rows=20)
        num = result.raw_response['response']['numFound']
        x=0
        if num<15:
            while x<num:
                tweet=[]
                tweet.append(result.raw_response['response']['docs'][x]['user.screen_name'][0])
                testname = result.raw_response['response']['docs'][x]['user.name'][0]
                tweet.append(result.raw_response['response']['docs'][x]['full_text'][0])
                tweet.append(result.raw_response['response']['docs'][x]['country'][0])
                tweet.append(result.raw_response['response']['docs'][x]['created_at'][0])
                tweet.append(result.raw_response['response']['docs'][x]['retweet_count'][0])
                tweet.append(result.raw_response['response']['docs'][x]['favorite_count'][0])
                topposts.append(tweet)
                x+=1
        else:
            while x!=15:
                tweet=[]
                tweet.append(result.raw_response['response']['docs'][x]['user.screen_name'][0])
                testname = result.raw_response['response']['docs'][x]['user.name'][0]
                tweet.append(result.raw_response['response']['docs'][x]['full_text'][0])
                tweet.append(result.raw_response['response']['docs'][x]['country'][0])
                tweet.append(result.raw_response['response']['docs'][x]['created_at'][0])
                tweet.append(result.raw_response['response']['docs'][x]['retweet_count'][0])
                tweet.append(result.raw_response['response']['docs'][x]['favorite_count'][0])
                topposts.append(tweet)
                x+=1

    #-------------google search------------
        topnews = []
        gquery = "news " + placeholder + " " + testname
        googlenews = GoogleNews()
        googlenews.get_news(gquery)
        results = googlenews.results()
        print("------Google Query------")
        print(gquery)
        #print(results[0])
        if len(results) == 0:
            print("No search results")
        else:
            y=0
            while y!=5:
                news = []
                news.append(results[y]['title'])
                news.append(results[y]['desc'])
                link = "https://" + results[y]['desc']
                news.append(link)
                news.append(results[y]['site'])
                #print(results[y]['title'])
                topnews.append(news)
                y+=1


        return render_template("result.html", num=num , top = topposts, quey = placeholder, news = topnews)

@app.route('/insights')
def insights():
    return render_template("insights.html")




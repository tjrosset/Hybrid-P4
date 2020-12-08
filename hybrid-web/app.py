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
        posters= {}
        sentiment = {}
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
                testname = result.raw_response['response']['docs'][0]['user.name'][0]
                tweet.append(result.raw_response['response']['docs'][x]['full_text'][0])
                tweet.append(result.raw_response['response']['docs'][x]['country'][0])
                tweet.append(result.raw_response['response']['docs'][x]['created_at'][0])
                tweet.append(result.raw_response['response']['docs'][x]['retweet_count'][0])
                tweet.append(result.raw_response['response']['docs'][x]['favorite_count'][0])
                tweet.append(result.raw_response['response']['docs'][x]['sentiment'][0])
                lin = 'https://twitter.com/realdonaldtrump/status/' + result.raw_response['response']['docs'][x]['id'][0]
                tweet.append(lin)
                topposts.append(tweet)

                senti = result.raw_response['response']['docs'][x]['sentiment'][0]
                if senti in sentiment.keys():
                    sentiment[senti] +=1
                else:
                    sentiment[senti]=1
                               

                name = result.raw_response['response']['docs'][x]['user.screen_name'][0]
                if name in posters.keys():
                    posters[name] +=1
                else:
                    posters[name]=1
               
                x+=1
        else:
            while x!=15:
                tweet=[]
                tweet.append(result.raw_response['response']['docs'][x]['user.screen_name'][0])
                testname = result.raw_response['response']['docs'][0]['user.name'][0]
                tweet.append(result.raw_response['response']['docs'][x]['full_text'][0])
                tweet.append(result.raw_response['response']['docs'][x]['country'][0])
                tweet.append(result.raw_response['response']['docs'][x]['created_at'][0])
                tweet.append(result.raw_response['response']['docs'][x]['retweet_count'][0])
                tweet.append(result.raw_response['response']['docs'][x]['favorite_count'][0])
                tweet.append(result.raw_response['response']['docs'][x]['sentiment'][0])
                lin = 'https://twitter.com/' + result.raw_response['response']['docs'][x]['user.screen_name'][0] + '/status/' + result.raw_response['response']['docs'][x]['id']
                #print(lin)
                tweet.append(lin)  
                topposts.append(tweet)

                senti = result.raw_response['response']['docs'][x]['sentiment'][0]
                if senti in sentiment.keys():
                    sentiment[senti] +=1
                else:
                    sentiment[senti]=1
                                    

                name = result.raw_response['response']['docs'][x]['user.screen_name'][0]
                if name in posters.keys():
                    posters[name] +=1
                else:
                    posters[name]=1
           
                x+=1

    #-------------google search------------
        topnews = []
        newsnames = {}
        gquery = "covid " + placeholder + " " + testname
        googlenews = GoogleNews(start='08-18-2020',end='09-27-2020')
        googlenews.search(gquery)
        results = googlenews.results()
        print("------Google Query------")
        print(gquery)
        #print(results[0])
        if len(results) == 0:
            print("No search results")
            temp=[["There are no news results for this query"]]
            topnews.append(temp)
        else:
            y=0
            while y!=len(results):
                news = []
                count = len(newsnames)
                x = 0
                news.append(results[y]['title'])
                news.append(results[y]['desc'])
                link = "https://" + results[y]['link']
                news.append(link)
                news.append(results[y]['media'])
                publisher = results[y]['media']
                if publisher=="":
                    publisher = "Other"
                if publisher in newsnames.keys():
                    newsnames[publisher] +=1
                else:
                    newsnames[publisher]=1
                #print(results[y]['date'])
                topnews.append(news)
                y+=1
        print(posters)
        return render_template("result.html", num=num , top = topposts, quey = placeholder, news = topnews , publishd=newsnames, posters = posters, sentiment = sentiment)

@app.route('/insights')
def insights():
    return render_template("insights.html")


if __name__ == '__main__':
    app.run()



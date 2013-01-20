import urllib, json, sys
from pprint import pprint
from flask import Flask, render_template, request
from pyechonest import config, song


config.ECHO_NEST_API_KEY="IY52OEPU4LRFUIY8R"
ALCHEMY_API_KEY="6b961c784967a94fe1829d3d065016f87bf38153"
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('ray.html')

@app.route("/text", methods=['POST', 'GET'])
def text():
    error = None
    if request.method == 'POST':
        return text_analyzed(request.form['url'])
    return render_template('text.html', error=error)

@app.route('/playlist', methods=['POST'])
def connie(URL=None):
    mood = texts(request.form['URL'])
    cate = cates(request.form['URL'])
    songlist = song.search(mood, buckets=['tracks','id:spotify-WW'], limit=True, results=5)
    foreign_ids = []
    for item in songlist:
        for t in item.get_tracks('spotify-WW'):
            foreign_ids.append(t['foreign_id'][17:])
        comma = ","
        foreign_id_string = comma.join(foreign_ids)
    return render_template("playlist.html", tracks=foreign_id_string)

def texts(name):
    global ALCHEMY_API_KEY
    analyzeURL = "http://access.alchemyapi.com/calls/url/URLGetTextSentiment?apikey=" + ALCHEMY_API_KEY + "&outputMode=json&url=" + name
    jsonResponse=json.loads(urllib.urlopen(analyzeURL).read())
    docSentiment = jsonResponse[u'docSentiment']
    mood = docSentiment[u'type']

    return mood

def cates(name):
    global ALCHEMY_API_KEY
    analyzeURL2 = "http://access.alchemyapi.com/calls/url/URLGetRankedConcepts?apikey=" + ALCHEMY_API_KEY + "&outputMode=json&url=" + name
    jsonResponse2=json.loads(urllib.urlopen(analyzeURL2).read())
    docRanked = jsonResponse2[u'docRanked']
    cate = docRanked[u'category']

    return cate



if __name__ == '__main__':
    app.run()

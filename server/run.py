from flask import Flask, render_template
import datetime
from sys import path as modules_directories
from os import path

scripts_path = path.abspath('../scripts')
modules_directories.append(scripts_path)
import authentication
import analysis
from candidates import CANDIDATES

app = Flask(__name__)

def validate_candidate(candidate):
    if candidate.capitalize() in CANDIDATES:
        return True
    return False


def validate_graph(graph):
    possible_graphs = [
        'betweenness centrality', 
        'closeness centrality', 
        'degree centrality', 
        'eigenvector centrality',
        'info',
        'pagerank',
        'hashtags'
    ]
    return graph in possible_graphs


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/charts/likes_rts")
def likes_rts_chart():
    return render_template('charts.html', chart='/static/charts/likes_and_rts.svg', title='Wykres Liczby polubień i reetweetów wpisów kandydatów')

@app.route("/charts/candidate_tweets")
def candidate_tweets_chart():
    return render_template('charts.html', chart='/static/charts/candidate_tweets.svg', title='Wykres liczby tweetów napisanych przez każdego kandydata')

@app.route("/charts/followers")
def followers_chart():
    return render_template('charts.html', chart='/static/charts/followers.svg', title='Liczba obserwujących każdego kandydata')

@app.route("/charts/friends")
def friends_chart():
    return render_template('charts.html', chart='/static/charts/friends.svg', title='Liczba przyjaciół każdego kandydata')


@app.route("/charts/retweet_count")
def retweet_count():
    return render_template('charts.html', chart='/static/charts/retweet_count.svg', title='Liczba retweetów zsumowana wg dat dla wszystkich kont kandydatów')


@app.route("/charts/tweet_count")
def tweet_count():
    return render_template('charts.html', chart='/static/charts/tweets_count.svg', title='Liczba tweetów zsumowana wg dat dla wszystkich kont kandydatów')

@app.route("/charts/favourite_count")
def favourite_count():
    return render_template('charts.html', chart='/static/charts/favourite_count.svg', title='Liczba tweetów zsumowana wg dat dla wszystkich kont kandydatów')

@app.route("/wordclouds/biedron_words")
def biedron_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Biedron_common_words.png', title='Wordcloud słów - Biedron')

@app.route("/wordclouds/bosak_words")
def bosak_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Bosak_common_words.png', title='Wordcloud słów - Bosak')

@app.route("/wordclouds/duda_words")
def duda_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Duda_common_words.png', title='Wordcloud słów - Duda')

@app.route("/wordclouds/holownia_words")
def holownia_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Holownia_common_words.png', title='Wordcloud słów - Holownia')

@app.route("/wordclouds/kidawa_words")
def kidawa_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Kidawa_common_words.png', title='Wordcloud słów - Kidawa')

@app.route("/wordclouds/kosiniak_words")
def kosiniak_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Kosiniak_common_words.png', title='Wordcloud słów - Kosiniak')

@app.route("/wordclouds/all_words")
def all_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/all_common_words.png', title='Wordcloud - wszystkie słowa')

@app.route("/wordclouds/biedron_tags")
def biedron_wordcloud_tags():
    return render_template('charts.html', chart='/static/wordclouds/tags/Biedron_tags.png', title='Wordcloud tagów - Biedron')

@app.route("/wordclouds/bosak_tags")
def bosak_wordcloud_tags():
    return render_template('charts.html', chart='/static/wordclouds/tags/Bosak_tags.png', title='Wordcloud tagów - Bosak')

@app.route("/wordclouds/duda_tags")
def duda_wordcloud_tags():
    return render_template('charts.html', chart='/static/wordclouds/tags/Duda_tags.png', title='Wordcloud tagów - Duda')

@app.route("/wordclouds/holownia_tags")
def holownia_wordcloud_tags():
    return render_template('charts.html', chart='/static/wordclouds/tags/Holownia_tags.png', title='Wordcloud tagów - Holownia')

@app.route("/wordclouds/kidawa_tags")
def kidawa_wordcloud_tags():
    return render_template('charts.html', chart='/static/wordclouds/tags/Kidawa_tags.png', title='Wordcloud tagów - Kidawa')

@app.route("/wordclouds/kosiniak_tags")
def kosiniak_wordcloud_tags():
    return render_template('charts.html', chart='/static/wordclouds/tags/Kosiniak_tags.png', title='Wordcloud tagów - Kosiniak')

@app.route("/wordclouds/all_tags")
def all_wordcloud_tags():
    return render_template('charts.html', chart='/static/wordclouds/tags/all_common_tags.png', title='Wordcloud - wszystkie tagi')

@app.route("/charts/tags/<candidate>")
def tags(candidate):
    if validate_candidate(candidate) or candidate == 'all_common':
        candidate = candidate.capitalize()
        title = f'Najpopularniejsze tagi - {candidate}'
        if candidate == 'All_common':
            title = 'Najpopularniejsze tagi - wszyscy kandydaci'
        return render_template('charts.html', chart=f'/static/charts/tags/{candidate}_tags.png', title=title)
    else:
        return 'Invalid candidate', 404

@app.route("/charts/replies/<candidate>")
def replies(candidate):
    if validate_candidate(candidate) or candidate == 'all':
        candidate = candidate.capitalize()
        title = f'Ilość odpowiedzi - {candidate}'
        if candidate == 'All':
            candidate = 'all'
            title = 'Ilość odpowiedzi - wszyscy kandydaci'
        return render_template('charts.html', chart=f'/static/charts/replies/{candidate}_replies.png', title=title)
    else:
        return 'Invalid candidate', 404

@app.route("/charts/common_words/<candidate>")
def common_words(candidate):
    if validate_candidate(candidate) or candidate == 'all':
        candidate = candidate.capitalize()
        title = f'Najpopularniejsze słowa - {candidate}'
        if candidate == 'All':
            title = 'Najpopularniejsze słowa - wszyscy kandydaci'
        return render_template('charts.html', chart=f'/static/charts/common_words/{candidate}_common_words.png', title=title)
    else:
        return 'Invalid candidate', 404

@app.route("/charts/tweets_count/<candidate>")
def tweets_count(candidate):
    if validate_candidate(candidate) or candidate == 'all':
        candidate = candidate.capitalize()
        title = f'Liczba tweetów - {candidate}'
        candidate = '_' + candidate
        if candidate == '_All':
            candidate = ''
            title = 'Liczba tweetów - wszyscy kandydaci'
        return render_template('charts.html', chart=f'/static/charts/tweets_count/tweets_count{candidate}.png', title=title)
    else:
        return 'Invalid candidate', 404

@app.route("/graphs/<graph>/<candidate>")
def graph(graph, candidate):
    if validate_graph(graph):
        if validate_candidate(candidate):
            title = f'{graph.capitalize()} - {candidate.capitalize()}'
            if graph == 'hashtags':
                chart = f'/static/graphs/{candidate}_{graph}.png'
            else:
                chart = f'/static/graphs/{candidate}_graph_{graph}.png'
            return render_template('graphs.html', chart=chart, title=title)
        else:
            return 'Invalid candidate', 404
    else:
        return 'Invalid graph', 404


if __name__ == '__main__':
    app.run(debug=True)
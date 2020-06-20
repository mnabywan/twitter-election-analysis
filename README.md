# Twitter Election Analysis

Środowisko do pozyskiwania spójnych tematycznych zbiorów danych (wg. zbiorów użytkowników lub według zbiorów słów kluczowych) z platformy Twitter. <br/> 
Aplikacja stworzona na potrzeby przedmiotu Inżynieria Oprogramowania.


## Opis
Aplikacja umożliwia pobieranie danych z Twittera na podstawie użytkowników a także słów kluczowych, hashtagów 
dotyczących wyborów prezydenckich w Polsce w 2020 roku.<br />


#### Architektura: 

![Alt text](images/archiecture.png?raw=true "Title")
<br /> <br />

Moduł persystencji pobiera informacje o tweetach i persystuje je w bazie SQLite.
Pozwala także na pobranie pełnych informacji o tweecie (wraz z tekstem) do formatu json, aby móc analizować tekst tweetów.

<br />
<br/>
Posiadając infromacje o twittach możemy wykonywać następujące analizy: 
- statystyczne - np. liczba tweetów poszczególnych kandydatów w czasie
- tekstowa - np. analiza popularnych słów używanych przez kandydatów
- społeczności - np. analiza grafu użytkowników tweetujących o danym kandydacie

<br />
Wyniki analiz w postaci wykresów, chmur słów czy grafów społeczności są wyświetlane na serwerze.


## Struktura projektu
#### Baza danych
Baza danych znajduje się w folderze [db](./db). <br />
[Twitter.db](./db/Twitter.db) to plik bazy SQLite, zawierający pobrane dane pobrane przy użyciu tweepy.
<br />
Do analizy tekstu tweetów używaliśmy tweetów zapisanych w formacie json. Z powodów ograniczeń pojemności GitHuba, nie mogliśmy umieścić używanych plików
w folderze. Aby móc analizować tweety pod kątem społeczności czy tekstu należy pobrać odpowiednie pliki z [folderu z Google Drive](https://drive.google.com/file/d/1drf4xsqVBeXQ2IzYVhHIE0Mv10AVEA-p/view?usp=sharing) i umieścić je w folderze [db](./db).

<br>

#### Moduł persystencji
Plik [persist_tweets.py](./scripts/persist_tweets.py) zawiera metody pozwalające na pobieranie tweetów, których autorami są określeni użykownicy (związani z danym kandydatem),
a także metody pozwalające na pobieranie tweetów zawierających dany hashtag.
<br /> Hahstagi i konta kandydatów są spisane w pliku [candidates.py](./scripts/candidates.py).
<br /> Pobrane tweety są persystowane w bazie SQLite. 
<br /> <br />
Plik [twitter_json_create.py](./scripts/twitter_json_create.py) pozwala na pobranie tweetów na podstawie id z bazy SQLite
do plików json. Dzięki temu w pliku json znajdują się tweety z pełną informacją o autorze, zawartością tekstu, co jest używane w analizie tekstu
i społeczności.


<br /> <br />
Używane biblioteki
- sqlite3
- tweepy


### Moduł analizy statystycznej
Plik [likes_analysis.py](./scripts/likes_analysis.py) zawiera metody pozwalające na wygenerowanie wykresów sumarycznej liczby polubień, retweetów dla poszczególnych kandydatów,
a także liczby przyjaciół i obserwujących danego konta. Powstałe wykresy są zapisywane w folderze [server/static/charts](./server/static/charts), aby móc później być wyśiwtlone.
<br /> <br />

Plik [tweets_by_candidate_analysis.py](./scripts/tweets_by_candidate_analysis.py) zawiera metody pozwalające stworzyć wykresy tweetów, polubień i retweetów w zależności od czasu
dla kont związanych z danym kandydatem. W tym celu dane pobierane są z bazy SQLite, tworzone są DataFrame'y i następnie wykres jest zapisywane w folderze [server/static/charts](./server/static/charts), aby móc później być wyśiwtlone.
<br /> <br />

Plik [account_tweets_by_candidate_analysis.py](./scripts/account_tweets_by_candidate_analysis.py) tworzy wykresy tego samego typu co [tweets_by_candidate_analysis.py]((./scripts/tweets_by_candidate_analysis.py)) z tą różnicą, że wykres dotyczy każdego kandydata z osobna.
Pozwala to zobaczyć, jaki wkład w aktywność całego sztabu konkretnego kandydata mają poszczególne konta z nim związane.

<br /> <br />
Używane biblioteki
- sqlite3
- matplotlib
- pandas

### Moduł analizy tekstowej
Plik [sentiment_anlaysis.py](./scripts/sentiment_analysis.py) zawiera metody pozwalające na analizę tekstu tweetów, bazując na tweetach zawartch w plikach json. 
Efektem analizy są wykresy najczęściej używanych słów dla każdego kandydata, wyznaczona miara podobieńtwa języka między poszczególnymi kandudatami, a także chmury słów. 
Powstałe wykresy i chmury słów są zapisywane odpowiednio w folderach [server/static/charts](./server/static/charts)
a także [server/static/wordclouds](.server/static/wordclouds). 

<br /> <br />
Używane biblioteki
- morfeusz2
- wordcould
- matplotlib
- pandas


### Moduł analizy społeczności
Plik [sna.py](./scripts/sna.py) zawiera metody pozwalające na analizę tweetów pod względem społeczności.
Efektem analizy są grafy prezentujące konta, z którymi konta kandydatów wchodziły w interakcję, a także prezentujące sieci zawierające konta, które tworzyły tweety o danym
kandydacie. Powstałe grafy i informacje o grafach są zapisywane w folderze [server/static/graphs](./server/static/graphs).

<br /> <br />
Używane biblioteki
- networkx
- numpy
- matplotlib
- pandas


### Serwer aplikacji
Wyniki otrzymane w wyniku powyższych analiz są prezentowane w formie aplikacji webowej we frameworku Flask. 
Część frontendową stanowią strony stworzone przy pomocy Bootstrapa-
frameworka CSS wypełniane przez back-end za pomocą silnika szablonów Jijnja2, który umożliwia ewaluację zmiennych wewnątrz 
przygotowanego wcześniej szkieletu HTML. Jako, że wbudowany serwer WSGI Flaska nie jest rekomendowany,
do uruchomienia aplikacji będziemy wykorzystywać serwer WSGI gunicorn.



## Instalacja
#### Linux
```bash
git clone https://github.com/mnabywan/twitter-election-analysis
export TWITTER_CONSUMER_KEY=
export TWITTER_CONSUMER_SECRET=
export TWITTER_ACCESS_KEY=
export TWITTER_ACCESS_SECRET=
python3 -m venv env
pip install -r requirements.txt
cd server
gunicorn --bind 0.0.0.0:5000 wsgi:app
```
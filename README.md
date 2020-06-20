# Twitter Election Analysis

Środowisko do pozyskiwania spójnych tematycznych zbiorów danych (wg. zbiorów użytkowników lub według zbiorów słów kluczowych) z platformy Twitter. <br/> 
Aplikacja stworzona na potrzeby przedmiotu Inżynieria Oprogramowania


##Opis
Aplikacja umożliwia pobieranie danych z Twittera na podstawie użytkowników a także słów kluczowych, hashtagów 
dotyczących wyborów prezydenckich w Polsce w 2020 roku.<br />


Architektura: 

![Alt text](images/archiecture.png?raw=true "Title")


Moduł persystencji pobiera informacje o tweetach i persystuje je w 


Pobierane informacje o twittach są persystowane w bazie SQLite. <br />
<br/>
Posiadając infromacje o twittach możemy wykonywać następujące analizy: 
- statystyczne - np. liczba tweetów poszczególnych kandydatów w czasie
- tekstowa - np. analiza popularnych słów używanych przez kandydatów
- społeczności - np. analiza grafu użytkowników tweetujących o danym kandydacie

<br />
Wyniki analiz w postaci wykresów, chmur słów czy grafów społeczności są wyświetlane na serwerze.





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
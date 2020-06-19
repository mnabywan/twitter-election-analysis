# Twitter Election Analysis


## Installation
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
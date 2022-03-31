# TweetBot

A simple Telegram Bot to Stream the tweets from any account from twitter to your telegram channel.  

# Guide
1. Get Twitter API Keys and Access Keys from [here](https://developer.twitter.com/en)
2. Ask for Twitter elevated permissions [here](https://developer.twitter.com/en/portal/products/essential), click at Elevated option and fill the forms
3. Go to [@BotFather](https://t.me/botfather) in telegram and create a Bot
4. Open keys_sample.env and fill the API Keys and Access Keys and Chat ID where you want the bot to send messages.
5. Rename `key_sample.env` to `keys.env`
6. Open `userlist.py` and add the usernames of the person's you want to Stream tweets from for Example:- `userslist = ['elonmusk','nasa']`
7. Run the Bot by executing:
```
pip3 install -r requirements.txt
python3 main.py
```
# Heroku usage
Just do all the things given in the Guide except the 6th part and follow the further steps here for Heroku deployment.
1. Create a Heroku APP
2. Git add and commit the files in the project directory and make sure you have the Heroku CLI installed.
```
git add.  -f
git commit -m "Initial Commit"
git push heroku HEAD:master --force
```
3. Then go to the app page in your heroku dashboard and turn on the dynos.

# Sample Channel
This channel is just a sample channel that streams the tweets from the Twitter accounts which are usually regular with Manchester United football club latest news and stuff.

Just visit [This Telegram Channel](https://t.me/notachannelyouwannavisitv2) to check how the bot works

# TweetBot

A simple Telegram Bot to Stream the tweets from any account from twitter to your telegram channel.This bot has been rewritten in rust if you still want 
to use the old source you can do that from checking out python branch

# Guide
1. Get Twitter API Keys and Access Keys from [here](https://developer.twitter.com/en)
2. Ask for Twitter elevated permissions [here](https://developer.twitter.com/en/portal/products/essential), click at Elevated option and fill the forms
3. Go to [@BotFather](https://t.me/botfather) in telegram and create a Bot
4. Open keys_sample.env and fill the API Keys and Access Keys and Chat ID where you want the bot to send messages.
5. Rename `key_sample.env` to `.env`
6. Install Rust by running the following command
```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
7. Run the Bot by executing:
```shell
cargo run --release
```
# Heroku usage
Just do all the things given in the Guide except the 6th & 7th part and follow the further steps here for Heroku deployment.
1. Create a Heroku APP
2. Install Heroku Rust buildpack from [here](https://github.com/emk/heroku-buildpack-rust.git).
3. Git add and commit the files in the project directory and make sure you have the Heroku CLI installed.
```shell
git add.  -f
git commit -m "Initial Commit"
git push heroku HEAD:master --force
```
4. Then go to the app page in your heroku dashboard and turn on the dynos.

# Sample Channel
This channel is just a sample channel that streams the tweets from the Twitter accounts which are usually regular with Manchester United football club latest news and stuff.

Just visit [This Telegram Channel](https://t.me/utdupdate_s) to check how the bot works

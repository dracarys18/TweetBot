use crate::error::TweetResult;
use egg_mode::KeyPair;
use egg_mode::Token;
use std::path::PathBuf;
use teloxide::prelude::{AutoSend, RequesterExt};
use teloxide::Bot;

#[derive(Debug)]
pub struct Config {
    pub accounts: Vec<String>,
    pub chat_id: i64,
    pub keywords: Vec<String>,
    token: Token,
    bot: AutoSend<Bot>,
}

impl Config {
    pub fn new() -> TweetResult<Self> {
        //Only run dotenv stuff if .env exists
        if PathBuf::from("./.env").exists() {
            dotenv::dotenv()?;
        }
        let accounts: Vec<String> = std::env::var("ACCOUNTS")
            .expect("Missing ACCOUNTS")
            .split(',')
            .map(|s| s.to_string())
            .collect();
        assert!(!accounts.is_empty());
        let chat_id = std::env::var("CHAT_ID")
            .expect("Missing CHAT_ID")
            .parse::<i64>()
            .expect("Invalid Chat ID");
        let consumer_key = std::env::var("CONSUMER_KEY").expect("Missing Consumer Key");
        assert!(!consumer_key.is_empty());
        let consumer_secret = std::env::var("CONSUMER_SECRET").expect("Missing Consumer Secret");
        assert!(!consumer_secret.is_empty());
        let access_token = std::env::var("ACCESS_TOKEN").expect("Missing Access token");
        assert!(!access_token.is_empty());
        let access_token_secret =
            std::env::var("ACCESS_TOKEN_SECRET").expect("Missing Acces token Secret");
        assert!(!access_token_secret.is_empty());
        let keywords: Vec<String> = std::env::var("KEYWORDS")
            .unwrap_or_default()
            .split(',')
            .map(|s| s.to_lowercase())
            .collect();
        let con_token = KeyPair::new(consumer_key, consumer_secret);
        let access_token = KeyPair::new(access_token, access_token_secret);
        let token = Token::Access {
            consumer: con_token,
            access: access_token,
        };
        let bot = Bot::from_env().auto_send();
        Ok(Self {
            accounts,
            chat_id,
            keywords,
            token,
            bot,
        })
    }
    pub fn token(&self) -> &Token {
        &self.token
    }
    pub fn bot(&self) -> &AutoSend<Bot> {
        &self.bot
    }
}

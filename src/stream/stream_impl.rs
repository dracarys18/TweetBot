use crate::config::Config;
use crate::error::TweetResult;
use crate::utils::{get_tweet_url, get_url_entity};
use egg_mode::stream::{filter, StreamMessage};
use futures::TryStreamExt;
use teloxide::prelude2::*;
use teloxide::types::ParseMode;
use teloxide::utils::html::escape;

pub async fn stream_tweets(config: &Config, to_follow: Vec<u64>) -> TweetResult<()> {
    let token = config.token();
    let bot = config.bot();
    let stream = filter().follow(&to_follow).start(token);
    stream
        .try_for_each(|t| async move {
            println!("here");
            if let StreamMessage::Tweet(tweet) = t {
                let tweeter_name = &tweet.user.as_ref().expect("Invalid User").name;
                let tweet_url = get_tweet_url(&tweet).await.unwrap_or_default();
                let text = escape(&tweet.text);
                let urls = get_url_entity(&tweet).await.unwrap_or_default();
                let message = format!(
                    "{}\n{}\nVia |<a href='{}'>{}</a>|",
                    text, urls, tweet_url, tweeter_name
                );
                //Don't send retweeted tweets
                if matches!(tweet.retweeted, Some(false)) {
                    bot.send_message(config.chat_id, message)
                        .parse_mode(ParseMode::Html)
                        .await
                        .expect("Failed to send a message");
                }
            }
            Ok(())
        })
        .await?;
    Ok(())
}

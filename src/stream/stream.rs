use crate::config::Config;
use crate::error::TweetResult;
use egg_mode::stream::{filter, StreamMessage};
use futures::TryStreamExt;
use teloxide::prelude2::Requester;

pub async fn stream_tweets(config: &Config, to_follow: Vec<u64>) -> TweetResult<()> {
    let token = config.token();
    let bot = config.bot();
    let stream = filter().follow(&to_follow).start(token);
    stream
        .try_for_each_concurrent(None, |t| async move {
            println!("here");
            if let StreamMessage::Tweet(tweet) = t {
                //Don't send retweeted tweets
                if tweet.retweeted.eq(&Some(false)) {
                    bot.send_message(config.chat_id, tweet.text)
                        .await
                        .expect("Failed to send a message");
                }
            }
            Ok(())
        })
        .await?;
    Ok(())
}

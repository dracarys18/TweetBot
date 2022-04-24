use crate::config::Config;
use crate::error::TweetResult;
use crate::utils::{get_tweet_url, tweet_has_media, tweet_has_url};
use egg_mode::stream::{filter, StreamMessage};
use futures::TryStreamExt;
use teloxide::prelude::*;
use teloxide::types::{ChatId, ParseMode};
use teloxide::utils::html::escape;

pub async fn stream_tweets(config: &Config, to_follow: &[u64]) -> TweetResult<()> {
    let token = config.token();
    let bot = config.bot();
    let stream = filter().follow(to_follow).start(token);
    eprintln!("Started the stream");
    stream
        .try_for_each(|t| async move {
            if let StreamMessage::Tweet(tweet) = t {
                let tweeter = tweet.user.as_ref().expect("Invalid User");
                let name = &tweeter.name;
                let _user_id = tweeter.id;
                let tweet_url = get_tweet_url(&tweet).await.unwrap_or_default();
                let text = escape(&tweet.text);
                let message = format!("{}\n\nVia |<a href='{}'>{}</a>|", text, tweet_url, name);
                //Don't send retweeted tweets and only send if the reply is from the current user (in case of threads)
                if (!text.starts_with("RT @") && matches!(tweet.in_reply_to_user_id, None))
                    || (!text.starts_with("RT @")
                        && (to_follow.contains(&_user_id))
                        && tweet.in_reply_to_user_id.unwrap().eq(&_user_id))
                {
                    let preview = !tweet_has_media(&tweet).await || tweet_has_url(&tweet).await;
                    let contains_keyword = text
                        .to_lowercase()
                        .split_whitespace()
                        .any(|w| config.keywords.contains(&w.to_string()));
                    if (config.keywords.is_empty() || config.keywords.eq(&vec![""]))
                        || contains_keyword
                    {
                        bot.send_message(ChatId(config.chat_id), message)
                            .parse_mode(ParseMode::Html)
                            .disable_web_page_preview(preview)
                            .await
                            .expect("Failed to send a message");
                        eprintln!("Sent {} to {},", tweet_url, config.chat_id);
                    }
                }
            }
            Ok(())
        })
        .await?;
    Ok(())
}

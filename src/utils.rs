use crate::TweetResult;
use egg_mode::tweet::Tweet;
use egg_mode::Token;

pub async fn get_account_ids(token: &Token, users_list: Vec<String>) -> TweetResult<Vec<u64>> {
    let account_ids: Vec<u64> = egg_mode::user::lookup(users_list, token)
        .await?
        .into_iter()
        .map(|u| u.response.id)
        .collect();
    Ok(account_ids)
}

pub async fn tweet_has_media(tweet: Tweet) -> bool {
    tweet.extended_entities.is_some() || tweet.entities.media.is_some()
}

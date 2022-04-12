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

pub async fn get_tweet_url(tweet: &Tweet) -> Option<String> {
    let tweet_id = tweet.id;
    let screen_name = &tweet.user.as_ref()?.screen_name;
    Some(format!(
        "https://twitter.com/{}/status/{}",
        screen_name, tweet_id
    ))
}
pub async fn tweet_has_url(tweet: &Tweet) -> bool {
    !tweet.entities.urls.is_empty()
}
pub async fn get_url_entity(tweet: &Tweet) -> Option<String> {
    let urls = tweet.entities.urls.clone();
    if urls.is_empty() {
        None
    } else {
        urls.into_iter()
            .map(|url| Some(format!("{}\n", url.expanded_url?)))
            .collect()
    }
}

pub async fn get_media_urls(tweet: &Tweet) -> Option<Vec<String>> {
    return if let Some(ext_entity) = tweet.extended_entities.as_ref() {
        Some(
            ext_entity
                .media
                .iter()
                .map(|e| e.media_url_https.clone())
                .collect(),
        )
    } else {
        Some(
            tweet
                .entities
                .media
                .as_ref()?
                .iter()
                .map(|m| m.media_url_https.clone())
                .collect(),
        )
    };
}
pub async fn tweet_has_media(tweet: &Tweet) -> bool {
    tweet.extended_entities.is_some() || tweet.entities.media.is_some()
}

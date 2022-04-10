use crate::config::Config;
use crate::error::TweetResult;
use crate::stream::stream_impl::stream_tweets;
use crate::utils::get_account_ids;

mod config;
mod error;
mod stream;
mod utils;

async fn run_bot() -> TweetResult<()> {
    let config = Config::new()?;
    let to_follow = get_account_ids(config.token(), config.accounts.clone()).await?;
    stream_tweets(&config, &to_follow).await?;
    Ok(())
}
#[tokio::main]
async fn main() -> TweetResult<()> {
    run_bot().await?;
    Ok(())
}

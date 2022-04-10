use std::panic::Location;
use thiserror::Error;

pub type TweetResult<T> = Result<T, TweetError<'static>>;

#[derive(Debug)]
pub struct TweetError<'l> {
    kind: TweetErrorKind,
    location: Location<'l>,
}

#[derive(Debug, Error)]
pub enum TweetErrorKind {
    #[error("Tweet Error {0:?}")]
    TweetError(#[from] egg_mode::error::Error),
    #[error("Dotenv Error {0:?}")]
    DotEnvError(#[from] dotenv::Error),
}

impl<'e> TweetError<'e> {
    #[track_caller]
    pub fn new(kind: TweetErrorKind) -> Self {
        Self {
            kind,
            location: *Location::caller(),
        }
    }
}

impl std::fmt::Display for TweetError<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Error: {} at {}#{}:{}",
            self.kind,
            self.location.file(),
            self.location.line(),
            self.location.column(),
        )
    }
}

impl std::error::Error for TweetError<'_> {}

impl<E> From<E> for TweetError<'_>
where
    E: Into<TweetErrorKind>,
{
    #[track_caller]
    fn from(error: E) -> Self {
        Self {
            kind: error.into(),
            location: *Location::caller(),
        }
    }
}

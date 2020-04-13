library(tidyverse)
library(wordcloud)
library(tidytext)
bad_data = read_csv('./data/bad_terms_df.csv')
good_data = read_csv('./data/good_terms_df.csv')
original_df = read_csv('./data/AppleStore.csv')

# Join DFs on app ID
bad_df = inner_join(bad_data, original_df, by = c('X1' = 'id')) %>%
  select(X1, prime_genre, price, size_bytes, track_name, words)

good_df = inner_join(good_data, original_df, by = c('X1' = 'id')) %>%
  select(X1, prime_genre, price, track_name, words)

# Tokenize the csv of tokens created by spacy (lazy)
bad_tokens = bad_df %>%
  unnest_tokens(output = token_words, input = words)

good_tokens = good_df %>%
  unnest_tokens(output = token_words, input = words)

# WordCloud of all bad
bad_tokens %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(6,.3),
      random.order = FALSE,
      max.words = 150,
      colors=brewer.pal(8,"Dark2")
    )
  )

# WordCloud of all good
good_tokens %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(8,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )

# Sample WordCloud for 1 app's bad reviews (evernote)
bad_tokens %>%
  filter(str_detect(track_name, "Evernote")) %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(8,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )

# Bad Token Histogram
bad_tokens %>%
  count(token_words, sort = TRUE) %>%
  filter(n>10000) %>%
  ggplot(aes(x = reorder(token_words, n), y = n)) +
  geom_col() +
  coord_flip() + 
  labs(x='', y='') +
  theme_classic()

#### Break by Genres

# Games
bad_tokens %>%
  filter(prime_genre == 'Games') %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(8,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )

# Education
bad_tokens %>%
  filter(prime_genre == 'Education') %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(5,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )
# Entertainment
bad_tokens %>%
  filter(prime_genre == 'Entertainment') %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(5,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )
# Photo & Video
bad_tokens %>%
  filter(prime_genre == 'Photo & Video') %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(5,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )

#### Paid vs Free
# Paid
bad_tokens %>%
  filter(price > 0) %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(4,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )
# Free
bad_tokens %>%
  filter(price == 0) %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(5,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2")
    )
  )

#### Size of App

# Over 1GB
bad_tokens %>%
  filter( size_bytes > 1000000000) %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(5,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2"),
      main='Title'
    )
  )

# Under 1GB
bad_tokens %>%
  filter( size_bytes < 1000000000) %>%
  count(token_words, sort = TRUE) %>%
  with(
    wordcloud(
      token_words,
      n,
      scale = c(5,.3),
      random.order = FALSE,
      max.words = 50,
      colors=brewer.pal(8,"Dark2"),
      main='Title'
    )
  )
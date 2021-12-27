library(tidyverse)
library(tidytext)
library(janeaustenr)

#studio_album_tracks <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-12-14/studio_album_tracks.csv')
#related_artists <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-12-14/related_artists.csv')
lyrics <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-12-14/lyrics.csv')

lyrics %>%
  dplyr:Ldistinct(song_name)

song_words <- lyrics %>%
  tidytext::unnest_tokens(word, line) %>%
  dplyr::count(song_name, word, sort = TRUE)

total_words <- song_words %>% 
  dplyr::group_by(song_name) %>% 
  dplyr::summarize(total = sum(n))

song_words <- dplyr::left_join(song_words, total_words)

song_tf_idf <- song_words %>%
  tidytext::bind_tf_idf(word, song_name, n)

song_tf_idf %>%
  dplyr::select(-total) %>%
  dplyr::arrange(dplyr::desc(tf_idf))

song_tf_idf_dat <- song_tf_idf %>%
  dplyr::arrange(song_name, dplyr::desc(tf_idf)) %>%
  dplyr::group_by(song_name) %>%
  dplyr::top_n(n = 5) %>%
  dplyr::ungroup() %>%
  dplyr::mutate(word = tidytext::reorder_within(word, tf_idf, song_name))

ggplot(song_tf_idf_dat, aes(x = tidytext::reorder_within(word, tf_idf, song_name),
                            y = tf_idf,
                            fill = song_name)) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  tidytext::scale_x_reordered() +
  facet_wrap(~song_name, scales = "free")

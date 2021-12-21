library(tidyverse)
library(tidymodels)
library(ggdark)

starbucks <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-12-21/starbucks.csv')

starb <- starbucks %>%
  dplyr::select(-product_name, -milk) %>%
  dplyr::mutate(
    fiber_g = as.numeric(fiber_g),
    trans_fat_g = as.numeric(trans_fat_g),
    size = fct_relevel(size, "tall")
  )

mod_base <- lm(caffeine_mg ~ ., data = starb)
mod_base

summary(mod_base)

coefs <- broom::tidy(mod_base) %>%
  dplyr::mutate(
    lower = estimate - 1.96 * std.error,
    upper = estimate + 1.96 * std.error,
  )

ggplot(coefs, aes(x = forcats::fct_reorder(term, estimate), y = estimate)) +
  geom_point() +
  geom_hline(yintercept = 0) + 
  ggtitle("What Variables Contribute to Caffeine",
        sub = "Moneyball that drink!") +
  xlab("Variable") +
  ylab("Coefficient") +
  coord_flip() +
  ggdark::dark_theme_minimal(base_size = 10) +
  theme(plot.title.position = "plot")

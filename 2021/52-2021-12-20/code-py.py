import pandas as pd
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
from plotnine import ggplot, geom_point, aes, ggtitle, geom_hline, xlab, ylab, coord_flip, theme_xkcd

starbucks_py = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-12-21/starbucks.csv")

starb_py = (starbucks_py
    .drop(["product_name", "milk"], axis="columns")
    .assign(
      fiber_g=pd.to_numeric(starb_py.fiber_g),
      trans_fat_g=pd.to_numeric(starb_py.trans_fat_g)
    )
)

mod_py = smf.ols(formula="".join(['caffeine_mg ~ ',
                                  " + ".join(starb_py.columns[:-1])]),
    data=starb_py)
mod_fit = mod_py.fit()
mod_fit.summary()


coefs = (pd.DataFrame(mod_fit.params)
    .reset_index()
    .rename(columns={"index":"variable", 0:"coefficient"})
    .sort_values(by=["coefficient"])
)

(ggplot(aes(x="variable", y="coefficient"), coefs) +
  geom_point() +
  geom_hline(yintercept = 0) + 
  ggtitle("What Variables Vontribute to Caffeine") +
  xlab("Variable") +
  ylab("Coefficient") +
  coord_flip() +
  theme_xkcd()
)
  
plt.show()


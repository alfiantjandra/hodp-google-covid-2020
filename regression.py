import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("covid_data/us_increase.csv")

df['date'] = pd.to_datetime(df['date'])
mask = (df['date'] > '2020-09-29') & (df['date'] <= '2020-12-28')
df = df.loc[mask]
df.set_index('date', inplace=True)
df['cases'] = df['cases'].div(1000)  # cases in thousands

keywords = ["loss of taste", "covid symptoms", "loss of smell", "face mask", "coronavirus vaccine", "covid testing"]
for word in keywords:
    df_rsv = pd.read_csv(f"US_google_trends/{word}.csv", index_col="date")
    df = pd.concat([df, df_rsv], axis=1)
    plt.figure(figsize=(10, 7.5))
    sns.regplot(x=word, y="cases", data=df, color='#C63F3F', scatter_kws={'s': 8})  # ci=None
    plt.ylabel("Increase in cases, thousands")
    plt.xlabel(f"{word} RSV")
    plt.ylim(0, 310)
    plt.yticks(np.arange(50, 301, step=50))
    plt.text(0.95, 285, f"R = {df.corr().loc['cases', word]:.2f}", fontsize=18,
             bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10},
             horizontalalignment='right')
    plt.show()

print(df.corr())

def df_shifted(df, target=None, lag=0):
    if not lag and not target:
        return df
    new = {}
    for c in df.columns:
        if c == target:
            new[c] = df[target]
        else:
            new[c] = df[c].shift(periods=lag)
    return pd.DataFrame(data=new)


for word in keywords:
    points = []
    for i in range(-14, 15):
        new_df = df_shifted(df, 'cases', lag=i)
        points.append((i, new_df.corr().loc['cases', word]))

    plt.figure(figsize=(6, 3))
    plt.plot(*zip(*points), color='r')
    plt.ylabel("Correlation")
    plt.xlabel("Lag/Lead")
    # plt.yticks(np.arange(0.25, 1.01, step=0.25)) perhaps use consistent ticks
    x, y = zip(*points)
    plt.title(f"{word.title()}, max: {max(y):.3f}")
    plt.show()

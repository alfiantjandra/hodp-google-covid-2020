import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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
    sns.regplot(x=word, y="cases", data=df, color='#C63F3F', scatter_kws={'s': 8})  # ci=None
    plt.ylabel("Cases (in thousands)")
    plt.xlabel(f"{word} RSV")
    plt.ylim(0, 305)
    plt.yticks(np.arange(50, 301, step=50))
    plt.show()

print(df.iloc[15: -15].corr())


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
        points.append((i, new_df.iloc[15: -15].corr().loc['cases', word]))

    plt.figure(figsize=(6, 2))
    plt.plot(*zip(*points), color='r')
    plt.ylabel("Correlation")
    plt.xlabel("Lag/Lead")
    # plt.yticks(np.arange(0.25, 1.01, step=0.25)) perhaps use consistent ticks
    x, y = zip(*points)
    plt.title(f"{word.title()}, max: {max(y)}")
    plt.show()

# X = df["coronavirus"].to_numpy().reshape((-1, 1))
# y = df["cases"].to_numpy()
#
# model = LinearRegression().fit(X, y)
# print("correlation: ", np.sqrt(model.score(X, y)))
# print("intercept: ", model.intercept_)
# print("slope: ", model.coef_)

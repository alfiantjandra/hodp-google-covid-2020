import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

df = pd.read_csv("covid_data/us_total.csv")

df['date'] = pd.to_datetime(df['date'])
mask = (df['date'] > '2020-09-29') & (df['date'] <= '2020-12-28')
df = df.loc[mask]
df.set_index('date', inplace=True)

keywords = ["coronavirus"]
for word in keywords:
    df_rsv = pd.read_csv(f"google/us_{word}.csv", index_col="date")
    df = pd.concat([df, df_rsv], axis=1)

print(df.iloc[15: -15].corr())
sns.regplot(x="coronavirus", y="cases", data=df)  # ci=None
plt.show()


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

    plt.plot(*zip(*points))
    plt.ylabel("Correlation")
    plt.xlabel("Lag/Lead")
    plt.title(word.title())
    plt.show()

# X = df["coronavirus"].to_numpy().reshape((-1, 1))
# y = df["cases"].to_numpy()
#
# model = LinearRegression().fit(X, y)
# print("correlation: ", np.sqrt(model.score(X, y)))
# print("intercept: ", model.intercept_)
# print("slope: ", model.coef_)

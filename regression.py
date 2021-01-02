import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

keywords = ["coronavirus"]
df = pd.read_csv("google/us.csv", index_col="date")
for word in keywords:
    df_rsv = pd.read_csv(f"google/us_{word}.csv", index_col="date")
    df = pd.concat([df, df_rsv], axis=1)

print(df.head())
df.plot(kind="scatter", x="coronavirus", y="cases", color="red")
plt.show()

# model = LinearRegression().fit(df["cases"].reshape((-1, 1)), df["coronavirus"])
# print("score: ", model.score(df["cases"], df["coronavirus"]))


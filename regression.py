import numpy as np
from numpy import linalg as LA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# plotting total cases/deaths in the US
#
# total_df = pd.read_csv("covid_data/us_total.csv")
# total_df['date'] = pd.to_datetime(total_df['date'])
# total_df.set_index('date', inplace=True)
# ax = total_df.plot(logy=True, grid=True, color=['#C63F3F', '#83BFCC'])
# ax.set(xlabel="Date", ylabel="Cases/Deaths", title="COVID-19 in the US")
# plt.minorticks_off()
# plt.show()

df = pd.read_csv("covid_data/us_increase.csv")
state_df = pd.read_csv("covid_data/us_states_increase.csv")
df['date'] = pd.to_datetime(df['date'])
mask = (df['date'] > '2020-09-29') & (df['date'] <= '2020-12-28')
df = df.loc[mask]
df.set_index('date', inplace=True)
df['cases'] = df['cases'].div(1000)  # cases in thousands

state_mask = (state_df['date'] > '2020-09-29') & (state_df['date'] <= '2020-12-28')
state_df['date'] = pd.to_datetime(state_df['date'])
state_df = state_df.loc[state_mask]
state_df.set_index('date', inplace=True)


keywords = ["loss of taste", "covid symptoms", "loss of smell", "face mask", "coronavirus vaccine", "covid testing"]

# plotting scatterplot/linear regression for each keyword
for word in keywords:
    df_rsv = pd.read_csv(f"US_google_trends/{word}.csv", index_col="date")
    df_rsv.index = pd.to_datetime(df_rsv.index)
    df = pd.concat([df, df_rsv], axis=1)
    state_df = pd.concat([state_df, df_rsv], axis=1)
    plt.figure(figsize=(10, 7.5))
    ax = sns.regplot(x=word, y="cases", data=df, color='#C63F3F', scatter_kws={'s': 12})  # ci=None
    ax.set(xlabel=f"{word} RSV", ylabel="Increase in cases (thousands)")
    ax.xaxis.label.set_size(16)
    ax.yaxis.label.set_size(16)
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


states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]  # include territories such as PR?
# NJ, PA, MD best states, MT, IA, WI, SD worst

MAX_DAY = 14

best_states_L1 = {}
best_states_L2 = {}
worst_states_L1 = {}
worst_states_L2 = {}

for word in keywords:
    points = []
    for i in range(MAX_DAY + 1):  # positive i means RSV from i days earlier is compared with current cases
        new_df = df_shifted(df, 'cases', lag=i)
        points.append(new_df.corr().loc['cases', word])

    plt.figure(figsize=(6, 3))
    plt.plot(np.arange(MAX_DAY + 1), points, color='r')
    plt.ylabel("Correlation")
    plt.xlabel("Lag/Lead")
    # plt.yticks(np.arange(0.25, 1.01, step=0.25))  # perhaps use consistent ticks
    # plt.ylim(0, 1)
    plt.title(f"{word.title()}, max: {max(points):.3f}, argmax: {np.argmax(points)}")

    for state in states:
        state_points = []
        for i in range(MAX_DAY + 1):
            new_df = df_shifted(state_df.loc[:, [state, word]], state, lag=i)
            state_points.append(new_df.corr().loc[state, word])
        best_states_L1[state] = LA.norm(np.array(points) - np.array(state_points), 1)
        best_states_L2[state] = LA.norm(np.array(points) - np.array(state_points), 2)
        worst_states_L1[state] = LA.norm(state_points, 1)
        worst_states_L2[state] = LA.norm(state_points, 2)
        plt.plot(np.arange(MAX_DAY + 1), state_points, color='grey', alpha=0.3)
    d = {k: v for k, v in sorted(best_states_L2.items(), key=lambda item: item[1])}
    print(d)
    plt.show()

import pandas as pd
import plotly.express as px

df = pd.read_csv("state_correlation.csv")
df.set_index("keyword", inplace=True)
df.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
df = df.T
df.index.names = ['states']
df.reset_index(inplace=True)

for keyword in df.columns:
    if keyword != "states":
        state_df = df[["states", keyword]]

        state_df = state_df.rename(columns={keyword: "R-value"})

        fig = px.choropleth(state_df,  # Input pandas DataFrame
                            locations="states",  # DataFrame column with locations
                            color="R-value",  # DataFrame column with values
                            color_continuous_scale=['#F1D3CF', '#760000'],
                            # hover_name="states",
                            hover_data={"states": False, "R-value": True},
                            locationmode="USA-states")

        fig.update_layout(title_text=f'Correlation by state - keyword "{keyword}"',
                          geo_scope="usa")

        fig.write_json(f'json/{keyword}.json')
        fig.show()

compiled_df = pd.DataFrame({'states': [], 'R-value': [], 'keyword': []})
for index, row in df.iterrows():
    for keyword in df.columns:
        if keyword != "states" and keyword != "loss of taste" and keyword != "face mask":
            series = pd.Series([row['states'], row[keyword], keyword], index=compiled_df.columns)
            compiled_df = compiled_df.append(series, ignore_index=True)

fig = px.choropleth(compiled_df,  # Input pandas DataFrame
                    locations="states",  # DataFrame column with locations
                    color="R-value",  # DataFrame column with values
                    facet_col="keyword",
                    facet_col_wrap=2,
                    color_continuous_scale=['#F1D3CF', '#760000'],
                    # hover_name="states",
                    hover_data={"states": False, "R-value": True},
                    locationmode="USA-states",
                    scope='usa')

fig.update_layout(title_text='Correlation by state based on keywords')

fig.write_json('json/subplot.json')
fig.show()

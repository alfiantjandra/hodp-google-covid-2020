import numpy as np
import pandas as pd
import plotly.express as px

d = {"states": ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "GU",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"], "r-value": np.random.rand(53)}

state_df = pd.DataFrame(data=d)

fig = px.choropleth(state_df,  # Input pandas DataFrame
                    locations="states",  # DataFrame column with locations
                    color="r-value",  # DataFrame column with values
                    color_continuous_scale=['#F1D3CF', '#760000'],
                    # hover_name="states",
                    hover_data={"states": False, "r-value": True},
                    locationmode="USA-states")

fig.update_layout(title_text="R-values by State",
                  geo_scope="usa")

fig.show()

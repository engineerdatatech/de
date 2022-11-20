import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# get cumulative confirmed cases in SG
# output will be list of dictionaries
url = "https://api.covid19api.com/country/singapore/status/confirmed"
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
response = json.loads(response.text)

# convert list of dictionaries to pandas dataframe
cases = pd.DataFrame.from_records(response)
cases.columns = ["country", "country_code", "province",
                 "city", "city_code", "lat", "lon", 
                 "cases", "status", "date"]
cases["date"] = pd.to_datetime(cases["date"], format="%Y-%m-%dT%H:%M:%SZ")

# plot using seaborn
sns.set_theme(style="darkgrid")

plt.figure(figsize=(15,10))
plt.ticklabel_format(style='plain', axis='y')

# to set first of the month as the major tick
months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%d %b %y')

lineplot = sns.lineplot(x="date", y="cases", data=cases)
lineplot.xaxis.set_major_locator(months)
lineplot.xaxis.set_major_formatter(months_fmt)
lineplot.set_title(f"Singapore's Covid Cases")

plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Number of Cases")
plt.tight_layout()

fig = lineplot.get_figure()
fig.savefig("singapore_covid_cases.png")
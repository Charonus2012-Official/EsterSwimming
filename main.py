import requests as rqsts
import pandas as pd
import json
import streamlit as st


name = "Ester Pilátová"

search = rqsts.get(f"https://vysledky.czechswimming.cz/cz.zma.csps.portal.rest/api/public/search?query={name}").json()

user_id = search[0]["userId"]

user = rqsts.get(f"https://vysledky.czechswimming.cz/cz.zma.csps.portal.rest/api/public/user-profiles/{int(user_id)}").json()

raw_results = rqsts.get(f"https://vysledky.czechswimming.cz/cz.zma.csps.portal.rest/api/public/user-profiles/{int(user_id)}/outputs?mastersOnly=false").json()

results = pd.DataFrame(raw_results)


st.write(f"# {user["firstName"]} {user["lastName"]}")



results["date"] = pd.to_datetime(results["date"]).dt.strftime("%d.%m.%Y")

results["time"] = (results['time'] / 1000).astype(str) + ' s'

results["poolLength"] = results["poolLength"].astype(str) + ' m'

columns_to_keep = [
    "disciplineTitle",
    "time",
    "points",
    "poolLength",
    "date",
    "competitionLocation"
]

results = results[columns_to_keep]

column_rename = {
    'disciplineTitle': 'Disciplína',
    'competitionLocation': 'Místo konání',
    'date': 'Datum',
    'poolLength': 'Bazén',
    'points': 'Body',
    'time': 'Čas'
}

results = results.rename(columns=column_rename)

pool25 = results[results["Bazén"] == "25 m"]
pool50 = results[results["Bazén"] == "50 m"]



height25 = len(pool25) * 35 + 38

height50 = len(pool50) * 35 + 38


st.write("## Bazén 50m")
st.dataframe(pool50, use_container_width=True, height=height50, hide_index=True)
st.write("## Bazén 25m")
st.dataframe(pool25, use_container_width=True, height=height25, hide_index=True)

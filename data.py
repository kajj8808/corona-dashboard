import pandas as pd
#df => dataFrame

conditions = ["confirmed" , "deaths" , "recovered"]

###############################################################################

daily_df = pd.read_csv("data/daily_reports.csv")

totals_df = daily_df[["Confirmed" , "Deaths" , "Recovered"]].sum().reset_index(name = "count")
totals_df = totals_df.rename(columns = {"index" : "condition"})

###############################################################################

countries_df = daily_df[["Country_Region","Confirmed" , "Deaths" , "Recovered"]]
countries_df = countries_df.groupby("Country_Region").sum().sort_values(by = "Confirmed" , ascending=False).reset_index()

###############################################################################

def make_global_df():
    def make_df(condition):
        df = pd.read_csv(f"data/time_{condition}.csv")
        #reset_index 를 해주면 dataFrame 으로 변경되서 화면에 뛰울수있게됨 아니면 시리어스 로됨 인덱스모양으로...
        df = df.drop(["Province/State" , "Country/Region" , "Lat" , "Long"] , axis = 1).sum().reset_index(name = condition)
        df = df.rename(columns={"index" : "date"})
        return df
    final_df = None;

    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else :
            final_df = final_df.merge(condition_df)
    return final_df

global_df = make_global_df()

###############################################################################

def make_country_df(country):
    
    def make_df(condition):
        df = pd.read_csv("data/time_confirmed.csv")
        df = df.loc[df["Country/Region"] == country]
        df = df.drop(columns = ["Province/State" , "Country/Region" , "Lat" , "Long"]).sum().reset_index(name = condition)
        df = df.rename(columns = {"index" : "date"})
        return df
    final_df = None

    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else :
            final_df = final_df.merge(condition_df)
    return final_df

country_df = make_country_df("Korea, South")


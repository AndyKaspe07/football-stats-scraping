import pandas as pd
import datetime
try:
    from googlesearch import search
except ImportError:
    print("No module named google found")


def get_player_code(name, surname):
    
    query = name + surname + "fbref"
    
    for i in search(query, tld = "com", num = 1, stop = 1):
        return str(i)[29:37]
    



name = input("Enter players' first name") 
surname = input("Enter players' second name")

code = get_player_code(name, surname)


games = int(input("How many games would you like to see the stats for?"))
today = datetime.date.today()
thisYear = today.year
nextYear = thisYear + 1


url = "https://fbref.com/en/players/" + code + "/matchlogs/" + str(thisYear) + "-" + str(nextYear) + "/misc/" + name + "-" + surname + "-Match-Logs"



stats = pd.read_html(url)

DataFrame = stats[0] #extract first table from webpage


def processing(df):
    """
    Pre-Processing function
    Parameter: Raw dataframe 
    Return: Cleaned dataframe with relevant data
    """
    df = df.iloc[:,[0, 1, 2, 4, 5, 7, 8, 10, 11, 14]] #Select relevant columns (date, minutes, fouls etc.)
    index = df.columns.droplevel(0) #Remove multi-indexing
    df.columns = index #Set new column titles
    df = df.drop(df[df["Min"] == "On matchday squad, but did not play"].index) #Remove games where player did not play 
    df = df.drop(df[df["Comp"] == 'Friendlies (M)'].index) #Filter for friendlies
    df = df.dropna() #Removing missing values
    df["Fls"] = pd.to_numeric(df["Fls"]) #Convert to integer data types
    df["Min"] = df["Min"].astype("int")
    df = df.loc[df["Min"] >= 60]

    return df

cleaned = processing(DataFrame)

print("Here are the last", games, "matches in which ", name, " ", surname, " played 60+ mins:")

print(cleaned.tail(games))
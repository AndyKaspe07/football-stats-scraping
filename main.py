import pandas as pd
import datetime
try:
    from googlesearch import search
except ImportError:
    print("No module named google found")

# This method gets the fbref player code using the URL 
def get_player_code(name, surname):
    
    query = name + surname + "fbref"
    
    for i in search(query, tld = "com", num = 1, stop = 1):
        return str(i)[29:37]

# Cleans the pandas dataframe that has been passed through 
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

# This method returns the current and next year as a tuple
def getYear():
    today = datetime.date.today()
    this = today.year
    next = thisYear + 1

    return (str(this), str(next))

# Get inputs
name = input("Enter players' first name") 
surname = input("Enter players' second name")
games = int(input("How many games would you like to see the stats for?"))

code = get_player_code(name, surname)
thisYear, nextYear = getYear()

url = "https://fbref.com/en/players/" + code + "/matchlogs/" + thisYear + "-" + nextYear + "/misc/" + name + "-" + surname + "-Match-Logs"



stats = pd.read_html(url)
DataFrame = stats[0] #extract first table from webpage
cleaned = processing(DataFrame)

#Output
print("Here are the last", games, "matches in which ", name, " ", surname, " played 60+ mins:")
print(cleaned.tail(games))
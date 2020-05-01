import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%
#merging data and choosing relevant columns 

odds1 = pd.read_csv('Season_14.15.csv', delimiter = ",")
odds2 = pd.read_csv('Season_15.16.csv', delimiter = ",")
odds3 = pd.read_csv('Season_16.17.csv', delimiter = ",")
odds4 = pd.read_csv('Season_17.18.csv', delimiter = ",")
odds5 = pd.read_csv('Season_18.19.csv', delimiter = ";")


odds_all = odds1.append(odds2, sort=False).append(odds3, sort=False).append(odds4, sort=False).append(odds5, sort=False)
print(odds_all)

relevant_columns = ["Date", "HomeTeam", "AwayTeam", "FTR", 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA']
odds_all = odds_all[relevant_columns]
odds_all.dropna(inplace=True)


odds_all.to_csv("new_file.csv") 
# %%
start_budget=1000
num_of_games= 3
type_of_score = 'min' #MIN or MAX ODDS
bet_side = 'B365H' # H or A or D

matchweeks = np.array_split(odds_all, 190)


def games_in_matchweek(num_of_games, type_of_score, bet_side):
    method_odds=[]
    for x in matchweeks:
        if type_of_score == "max":
            matches = x.nlargest(num_of_games, bet_side)
            print(matches)
            method_odds.append(pd.DataFrame.as_matrix(matches))
        elif type_of_score == "min":
            matches = x.nsmallest(num_of_games, bet_side)
            print(matches)
            method_odds.append(pd.DataFrame(matches))
    return method_odds

def cumulating_odds(method_odds):
    cumulated_odds=[]
    for x in method_odds:
        x = list(x[bet_side])
        x = np.prod(np.array(x))
        cumulated_odds.append(x)
    return cumulated_odds

def bet_values(minimum, middle, maximum):
    bet_values = []
    for odd in cumulated_odds:
        if odd < minimum:
            bet_value=100
        elif odd > minimum and odd < middle:
            bet_value=70
        elif odd > middle and odd < maximum:
            bet_value=50
        else:
            bet_value=20
        bet_values.append(bet_value)    
    return bet_values

def win_or_lose(bet_side, num_of_games):
    result_list = [bet_side[-1]]*num_of_games
    win_not = []
    for x in method_odds:
        if result_list == list(x['FTR']):
            win_not.append(1)
        else:
            win_not.append(0)
    return win_not

method_odds = games_in_matchweek(num_of_games, type_of_score, bet_side)
cumulated_odds = cumulating_odds(method_odds)
bet_values = bet_values(4.5, 9, 13.5)
w_l = win_or_lose(bet_side, num_of_games)

dic = {"cumulated_odds": cumulated_odds, "bet_value": bet_values, "win_or_loss": w_l}
df_final = pd.DataFrame(dic)

df_final.loc[df_final["win_or_loss"] == 1, "result_of_bet"] = (df_final["cumulated_odds"]
                                     * df_final["bet_value"] * df_final["win_or_loss"])
df_final.loc[df_final["win_or_loss"] == 0, '"result_of_bet"'] = (-df_final["bet_value"])

#df_final['current_score'].loc[df_final["result_of_bet"]]
# %%
#Wykresy         
        
plt.hist(df_final["cumulated_odds"], 40, color="red")
plt.title('Rozkład kursów 1 metody')
plt.xlabel('Wysokosc skumulowanego kursu')
plt.grid(True)
plt.show()

"""
plt.plot(range(0,190), )
plt.title('Budżet 3 metod w poszczególnych kolejkach')
plt.ylabel('Budżet')
plt.xlabel('Numer kolejki')
plt.grid(True)
plt.show()
"""
# %%
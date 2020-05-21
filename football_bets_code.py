# %% 
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


relevant_columns = ["Date", "HomeTeam", "AwayTeam", "FTR", 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA']
odds_all = odds_all[relevant_columns]
odds_all.dropna(inplace=True)

odds_all.to_csv("new_file.csv") 

#dividing data into matchweeks (10 matches)
matchweeks = np.array_split(odds_all, 190)
# %%
def games_in_matchweek(num_of_games, type_of_score, bet_side):
    """Function allows user to choose num of games he wants to bet on, 
    minimum or maximum values of odds and side which he 
    guess will win (home, away or draw). It returns a data frame of matches 
    which satisfiy given conditions"""
    method_odds=[]
    for x in matchweeks:
        if type_of_score == "max":
            matches = x.nlargest(num_of_games, bet_side)
            method_odds.append(pd.DataFrame(matches))
        elif type_of_score == "min":
            matches = x.nsmallest(num_of_games, bet_side)
            method_odds.append(pd.DataFrame(matches))
    return method_odds

def cumulating_odds(method_odds):
    """Function calculate cumulated odds based on matches selected
    in games_in_matchweek() function"""
    cumulated_odds=[]
    for x in method_odds:
        x = list(x[bet_side])
        x = np.prod(np.array(x))
        cumulated_odds.append(x)
    return cumulated_odds

def bet_values(minimum, middle, maximum):
    """Function calculates bets value based on cumulated odds"""
    all_bet_values = []
    for odd in cumulated_odds:
        if odd < minimum:
            bet_value=start_budget * 0.01
        elif odd > minimum and odd < middle:
            bet_value=start_budget * 0.007
        elif odd > middle and odd < maximum:
            bet_value=start_budget * 0.005
        else:
            bet_value=start_budget * 0.003
        all_bet_values.append(bet_value)    
    return all_bet_values

def win_or_lose(bet_side, num_of_games):
    """Function checks whether ticket won or lost"""
    result_list = [bet_side[-1]]*num_of_games
    win_not = []
    for x in method_odds:
        if result_list == list(x['FTR']):
            win_not.append(1)
        else:
            win_not.append(0)
    return win_not

    
def score_data_frame(cumulated_odds, bet_values, w_l):
    """Function creates data frame of data calculated in previous functions"""
    dic = {"cumulated_odds": cumulated_odds, "bet_value": bet_values, "win_or_loss": w_l}
    df_final = pd.DataFrame(dic)
    df_final.loc[df_final["win_or_loss"] == 1, "result_of_bet"] = (df_final["cumulated_odds"] 
                                            * df_final["bet_value"] * df_final["win_or_loss"])
    df_final.loc[df_final["win_or_loss"] == 0, "result_of_bet"] = (-df_final["bet_value"])
    df_final['score_in_time'] = ""
    df_final['score_in_time'].iloc[0] = start_budget+df_final["result_of_bet"].iloc[0]
    for x in range(0,189):
        df_final['score_in_time'].iloc[x+1]=(df_final['score_in_time'].iloc[x]
                                        +df_final["result_of_bet"].iloc[x+1])
    return df_final

def line_plot_all_methodes(methodes=[],labels=[]):
    """Function creates line plot of score in time of all chosen bet methodes"""
    
    for (x,y) in zip(methodes,labels):
        plt.plot(range(0,190), x, label=y)
    
    plt.title("Score in time")
    plt.xlabel("Matchweek number")
    plt.ylabel("Amount of money")
    plt.legend()
   
    
# %%
def generating_plots(data_plot_1, data_plot_2, data_plot_3, data_plot_4, start_budget):
    """
    Function generates a summary of a given method
    example:
    data_plot_1 = min_H_2["cumulated_odds"]
    data_plot_2 = min_H_2["win_or_loss"].value_counts(normalize=True)
    data_plot_3 = min_H_2["bet_value"].value_counts(normalize=True)
    data_plot_4 = min_H_2['score_in_time']
    """
    plt.style.use('seaborn')
    fig, axis = plt.subplots(2, 2)
    plt.grid(True)
    plt.tight_layout()
    
    axis[0, 0].hist(data_plot_1, bins=10, color="purple", label='Cumulated odds', alpha=0.5)
    axis[0, 0].set_title('Dispersion of cumulated odds')
    axis[0, 0].set_xlabel('Cumulated odds')
    axis[0, 0].set_ylabel('Number of odds in particular bins')
    axis[0, 0].grid(False)
    axis[0, 0].legend()
    
    #dodać linie znacząca początkowy budżet 
    axis[0, 1].plot(range(0,190), data_plot_4, label='budget in time')
    axis[0, 1].axhline(start_budget, color='red')
    axis[0, 1].set_title('Budget over time')
    axis[0, 1].set_ylabel('Budget')
    axis[0, 1].set_xlabel('Unit of time')
    axis[0, 1].legend()
    
    axis[1, 0].pie(data_plot_3, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
    axis[1, 0].set_title('Share of particular bet values')
    axis[1, 0].legend(data_plot_3.index, loc=(0.9, 0.70))
    
    
    axis[1, 1].pie(data_plot_2, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
    axis[1, 1].set_title('Percentage of won and failed tickets')
    axis[1, 1].legend(data_plot_2.index, labels=['failed', 'won'], loc=(0.75,0.8))
    
    plt.tight_layout()
    plt.show()
    
    return fig, axis
# %%
#Example of a bet method 
start_budget=10000
num_of_games= 5
type_of_score = 'min' #MIN or MAX ODDS
bet_side = 'B365H' # H or A or D    

method_odds = games_in_matchweek(num_of_games, type_of_score, bet_side)
cumulated_odds = cumulating_odds(method_odds)
all_bet_values = bet_values(15, 20, 25)
w_l = win_or_lose(bet_side, num_of_games)
min_H_5 = score_data_frame(cumulated_odds, all_bet_values, w_l)
generating_plots(min_H_5["cumulated_odds"],
                 min_H_5["win_or_loss"].value_counts(normalize=True),
                 min_H_5["bet_value"].value_counts(normalize=True), 
                 min_H_5['score_in_time'], 10000)
# %%
#Example of a bet method 
start_budget=3000
num_of_games= 3
type_of_score = 'max' #MIN or MAX ODDS
bet_side = 'B365H' # H or A or D    

method_odds = games_in_matchweek(num_of_games, type_of_score, bet_side)
cumulated_odds = cumulating_odds(method_odds)
all_bet_values = bet_values(4.5, 9, 13.5)
w_l = win_or_lose(bet_side, num_of_games)
min_H_3 = score_data_frame(cumulated_odds, all_bet_values, w_l)
generating_plots(min_H_3["cumulated_odds"],
                 min_H_3["win_or_loss"].value_counts(normalize=True),
                 min_H_3["bet_value"].value_counts(normalize=True), 
                 min_H_3['score_in_time'], 3000)
# %%
#Example of a bet method 
start_budget=3000
num_of_games= 2
type_of_score = 'max' #MIN or MAX ODDS
bet_side = 'B365H' # H or A or D    

method_odds = games_in_matchweek(num_of_games, type_of_score, bet_side)
cumulated_odds = cumulating_odds(method_odds)
all_bet_values = bet_values(4.5, 9, 13.5)
w_l = win_or_lose(bet_side, num_of_games)
max_H_2 = score_data_frame(cumulated_odds, all_bet_values, w_l)
generating_plots(max_H_2["cumulated_odds"], 
                 max_H_2["win_or_loss"].value_counts(normalize=True), 
                 max_H_2["bet_value"].value_counts(normalize=True), 
                 max_H_2['score_in_time'], 3000)


#%%
#Generating line plots of score in time of all methodes 
line_plot_all_methodes([min_H_5['score_in_time'], max_H_2['score_in_time'], 
                min_H_3['score_in_time']],
                labels=['min_H_5', 'max_H_2', 'min_H_3'])

# %%

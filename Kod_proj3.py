#before running the code please set working directory 


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


print( os.getcwd() )
os.chdir(r'C:\Users\Michałcfc\Desktop\Studia\Magisterka\II_semestr\ZMW\PROJ3\dane')



# %%
#przygotowanie danych, połącznie csv i wybór kolumn 

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
#metoda zakładająca postawienie zakładu na cztery najniższe kursy domowe w każdej kolejce 

start_budget=1000
actual_budget1=[]
lowest_odds=[]
cumulated_odds1=[]
lowest_odds_FTR=[]
bet_value=0
bet_value_cumulated_odd=[]


#podział data frame na kolejki po 10 meczów 
matchweeks = np.array_split(odds_all, 190)

#obliczenie skumuluwanych kursów dla 1 metody 
for i in    matchweeks:
    k = i.nsmallest(4,"B365H") #wybiera 4 najniższe domowe kursy 
    lowest_odds.append(pd.DataFrame.as_matrix(k.iloc[0:4,4:5]))
for x in lowest_odds:
    cumulated_odds1.append(x.item(0,0)*x.item(1,0)*x.item(2,0)*x.item(3,0))

#przedziały pozwalające wybrać wysokosc zakładu w zależnosci od skumulowanego kursu
minimum=4.5
middle=9
maximum=13.5

#kurs*kwota w widełkach 
bet_values = [] # DODANE
    
for odd in cumulated_odds1:
    if odd < minimum:
        bet_value=40
    elif odd > minimum and odd < middle:
        bet_value=30
    elif odd > middle and odd <maximum:
        bet_value=20
    else:
        bet_value=100
    bet_values.append(bet_value)     # DODANE
    bet_value_cumulated_odd.append(bet_value*odd)

#data.farame -> wycinki z odpowiednimi kursami i kolumną FTR  
for i in matchweeks:
    k = i.nsmallest(4,"B365H")
    lowest_odds_FTR.append(k)   
        

#obliczenie budżetu na przestrzeni czasu 
for i in range(190):
    x = lowest_odds_FTR[i]
    
    dfTOlist = list(x['FTR'])
    if dfTOlist == ['H', 'H', 'H', 'H']:
        bet = bet_value_cumulated_odd[i]
        actual_budget1.append(round(start_budget+bet, 2))
        start_budget=actual_budget1[-1]
    else:
        actual_budget1.append(round(start_budget-bet_values[i],2))
        start_budget=actual_budget1[-1]
        
  






# %%
#metoda zakładająca postawienie zakładu na dwa najniższe wyjazdowe kursy w każdej kolejce 
#wszystkie częsci kody działają analogicznie do pierwszej metody 

start_budget2A=1000
actual_budget2A=[]
lowest_odds2A=[]
cumulated_odds2A=[]
lowest_odds_FTR2A=[]
bet_value_2A=0
bet_value_cumulated_odd2A=[]



matchweeks = np.array_split(odds_all, 190)


for i in    matchweeks:
    k = i.nsmallest(2,"B365A") 
    lowest_odds2A.append(pd.DataFrame.as_matrix(k.iloc[0:2,6:7]))
for x in lowest_odds2A:
    cumulated_odds2A.append(x.item(0,0)*x.item(1,0))


minimum2A=4.5
middle2A=9
maximum2A=13.5



bet_values2A = [] 
    
for odd in cumulated_odds2A:
    if odd < minimum2A:
        bet_value_2A=40
    elif odd > minimum2A and odd < middle2A:
        bet_value_2A=30
    elif odd > middle2A and odd <maximum2A:
        bet_value_2A=20
    else:
        bet_value_2A=100
    bet_values2A.append(bet_value_2A)     
    bet_value_cumulated_odd2A.append(bet_value_2A*odd)


for i in matchweeks:
    k = i.nsmallest(2,"B365A")
    lowest_odds_FTR2A.append(k) 
        

for i in range(190):
    x = lowest_odds_FTR2A[i]
    
    dfTOlist = list(x['FTR'])
    if dfTOlist == ['A', 'A']:
        bet = bet_value_cumulated_odd2A[i]
        actual_budget2A.append(round(start_budget2A+bet, 2))
        start_budget2A=actual_budget2A[-1]
    else:
        actual_budget2A.append(round(start_budget2A-bet_values2A[i],2))
        start_budget2A=actual_budget2A[-1]







# %%
#metoda zakładająca postawienie zakładu na dwa najniższe domowe kursy w każdej kolejce 
#wszystkie częsci kody działają analogicznie do pierwszej metody 

start_budget2H=1000
actual_budget2H=[]
lowest_odds2H=[]
cumulated_odds2H=[]
lowest_odds_FTR2H=[]
bet_value_2H=0
bet_value_cumulated_odd2H=[]



matchweeks = np.array_split(odds_all, 190)


for i in    matchweeks:
    k = i.nsmallest(2,"B365H") 
    lowest_odds2H.append(pd.DataFrame.as_matrix(k.iloc[0:4,4:5]))
for x in lowest_odds2H:
    cumulated_odds2H.append(x.item(0,0)*x.item(1,0))


minimum2H=4.5
middle2H=9
maximum2H=13.5



bet_values2H = []
    
for odd in cumulated_odds2H:
    if odd < minimum2H:
        bet_value_2H=40
    elif odd > minimum2H and odd < middle2H:
        bet_value_2H=30
    elif odd > middle2H and odd <maximum2H:
        bet_value_2H=20
    else:
        bet_value_2H=100
    bet_values2H.append(bet_value_2H)     
    bet_value_cumulated_odd2H.append(bet_value_2H*odd)

 
for i in matchweeks:
    k = i.nsmallest(2,"B365H")
    lowest_odds_FTR2H.append(k)   
        

for i in range(190):
    x = lowest_odds_FTR2H[i]
    
    dfTOlist = list(x['FTR'])
    if dfTOlist == ['H', 'H']:
        bet = bet_value_cumulated_odd2H[i]
        actual_budget2H.append(round(start_budget2H+bet, 2))
        start_budget2H=actual_budget2H[-1]
    else:
        actual_budget2H.append(round(start_budget2H-bet_values2H[i],2))
        start_budget2H=actual_budget2H[-1]



# %%
#Wykresy         
        
plt.hist(cumulated_odds1, 40, density=True, color="red")
plt.title('Rozkład kursów 1 metody')
plt.xlabel('Wysokosc skumulowanego kursu')
plt.grid(True)
plt.show()


plt.plot(range(0,190), actual_budget1)
plt.plot(range(0,190), actual_budget2A)
plt.plot(range(0,190), actual_budget2H)
plt.title('Budżet 3 metod w poszczególnych kolejkach')
plt.ylabel('Budżet')
plt.xlabel('Numer kolejki')
plt.grid(True)
plt.show()

# %%
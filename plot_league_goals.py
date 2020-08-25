#this code plots a histogram of the goals scored in a PL season as a funciton of game minute

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from scipy import stats

##### decide whether or not to save the figure that results from this code #####
save_fig=0

##### read in the data file containing the goals data from the season of choice #####
season_span='19_20'
in_file=season_span + '_PL_goals_web_data.csv'
match_results_df=pd.read_csv(in_file)

##### make a list containing the minute that each goal was scored this season #####
goal_minutes=[] #initialize an empty list
total_goals_in_match=[]
victory_margin=[]
for index, row in match_results_df.iterrows():
    if len(row["home goal times"]) > 2: #a goal was scored by the home team
        goal_times=row["home goal times"][1:-1].split(',')
        for minute in goal_times:
            goal_minutes.append(int(minute.strip()[1:-1]))
    if len(row["away goal times"]) > 2: #a goal was scored by the home team
        goal_times=row["away goal times"][1:-1].split(',')
        for minute in goal_times:
            goal_minutes.append(int(minute.strip()[1:-1]))
    total_goals_in_match.append( int(row["home final score"]) + int(row["away final score"]) )
    victory_margin.append( abs(int(row["home final score"]) - int(row["away final score"])) )

#print( total_goals_in_match )
#print( victory_margin )

##### goal times data for each match this season #####
goal_times_bin_settings=range(1,92)
[bin_counts, bin_edges]=np.histogram(goal_minutes, bins=goal_times_bin_settings)

avg_goals_per_minute=(sum(bin_counts[0:44]) + sum(bin_counts[45:89])) / (len(bin_counts[0:44]) + len(bin_counts[45:89])) #calculate the average number of goals scored throughout the season per minute, excluding stoppage time
print('\t' + str(len(goal_minutes)) + " goals were scored in PL season " + season_span + '.')
print('\t\t' + str(sum(bin_counts[0:44]) + sum(bin_counts[45:89])) + " of them were scored outside of stoppage time.")
print("\ton average, {:0.2f} goals were scored per combined game minute, excluding stoppage time.".format(avg_goals_per_minute)) #':' introduces format spec, 0 enables sign-aware zero-padding for numeric types, .2 sets the precision to 2 decimal places, and f displays the number as a fixed-point number

##### use a chi-square goodness of fit test to determine if goals are scored uniformly throught matches #####
#https://stats.stackexchange.com/questions/110718/chi-squared-test-with-scipy-whats-the-difference-between-chi2-contingency-and
X_square_alpha=0.05 #we will reject the null hypothesis that goals are evenly distributed if the X squared p-value is less than this
goals_per_min_no_stoppage=np.concatenate((bin_counts[0:44], bin_counts[45:89]), axis=0)
X_square_statistic, X_square_p_value=stats.chisquare(goals_per_min_no_stoppage) #I am going to use the scipy package to calculate the p-value for me
if X_square_p_value < X_square_alpha:
    print('\tGoals do NOT occur with equal probability throughout these matches')
else:
    print('\tGoals occur with equal probability throughout these matches')
print('\t\tChi-square p-value: {:0.3f}'.format(X_square_p_value))
#X_square_val=sum( [( (count-avg_goals_per_minute)**2 )/avg_goals_per_minute for count in bin_counts[0:44]] ) + sum( [( (count-avg_goals_per_minute)**2 )/avg_goals_per_minute for count in bin_counts[45:89]] )
#X_square_deg_free=len(bin_counts[0:44]) + len(bin_counts[45:89]) - 1
#print(X_square_val)

##### total number of goals scored in each match #####
tot_goals_bin_settings=range(0,12)
tot_goals_bin_settings=[edge - 0.5 for edge in tot_goals_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
if max(total_goals_in_match) > 10:
    print("WARNING: default bin range was insufficient, so it was adjusted")
    tot_goals_bin_settings=range(0,max(total_goals_in_match)+2)
    tot_goals_bin_settings=[edge - 0.5 for edge in tot_goals_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
avg_goals_per_match=sum(total_goals_in_match)/len(match_results_df)
print("\ton average, {:0.2f} goals were scored in each match this season.".format(avg_goals_per_match))

##### margin of victory for each match #####
vic_marg_bin_settings=range(0,12)
vic_marg_bin_settings=[edge - 0.5 for edge in vic_marg_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
if max(victory_margin) > 10:
    print("WARNING: default bin range was insufficient, so it was adjusted")
    vic_marg_bin_settings=range(0,max(victory_margin)+2)
    vic_marg_bin_settings=[edge - 0.5 for edge in vic_marg_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
victory_margin_games_with_winner=[x for x in victory_margin if x > 0]
avg_victory_margin_per_match=sum(victory_margin_games_with_winner)/len(victory_margin_games_with_winner)
avg_goal_difference_per_match=sum(victory_margin)/len(victory_margin)
print("\ton average, the margin of victory was {:0.2f} goals for matches with a victor this season.".format(avg_victory_margin_per_match))

##### fit a Poisson probability mass function to the binned data #####
#define the probability mass function
def Poisson_pmf(lam, k): #lambda is the mean value of occurrences per time interval, k is the number of occurrences per time interval
    return((lam**k) * (2.718**(-lam)) / np.math.factorial(k))

#make some realistic k values and calculate the pmf at those k values, then multiply by the total number of matches this season
Poisson_pmf_goals_per_match_df=pd.DataFrame( {'k values':np.arange(11)} )
Poisson_pmf_goals_per_match_df['Poisson counts']=Poisson_pmf_goals_per_match_df.apply(lambda row: Poisson_pmf(avg_goals_per_match, row['k values']), axis=1) * len(match_results_df)

##### plot the results of your analysis #####
fig, axes=plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
fig.suptitle('Season: ' + season_span)

axes[0].set_title('when goals were scored')
axes[0].set_xlabel('minute', fontsize=14, color='black')
axes[0].set_ylabel('goals scored', fontsize=14, color='black')
axes[0].set_xlim(1, 91)
axes[0].set_ylim(0, max(bin_counts)+5)
axes[0].hist([x for x in goal_minutes if x < 45], density=False, bins=goal_times_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes[0].hist([x for x in goal_minutes if x > 45 and x < 90], density=False, bins=goal_times_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes[0].hist([x for x in goal_minutes if x == 45 or x == 90], density=False, bins=goal_times_bin_settings, color=(0.69,0.23,0.56))  #`density=True` makes probabilities, `density=False` uses raw counts
axes[0].plot([0,90], [avg_goals_per_minute, avg_goals_per_minute], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored

axes[1].set_title('goals scored per match')
axes[1].set_xlabel('goals scored', fontsize=14, color='black')
axes[1].set_ylabel('matches', fontsize=14, color='black')
axes[1].set_xlim(-0.5, 10.5)
axes[1].set_ylim(0, 120)
axes[1].plot([avg_goals_per_match, avg_goals_per_match], [0,380], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored in a match
axes[1].hist(total_goals_in_match, density=False, bins=tot_goals_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes[1].plot(Poisson_pmf_goals_per_match_df['k values'], Poisson_pmf_goals_per_match_df['Poisson counts'], marker='o', linestyle='', color=(0.07,0.41,0.98))

axes[2].set_title('final goal difference per match')
axes[2].set_xlabel('goal difference', fontsize=14, color='black')
axes[2].set_ylabel('matches', fontsize=14, color='black')
axes[2].set_xlim(-0.5, 10.5)
axes[2].set_ylim(0, 200)
axes[2].plot([avg_goal_difference_per_match, avg_goal_difference_per_match], [0,380], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored in a match
axes[2].hist(victory_margin, density=False, bins=vic_marg_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts

fig.tight_layout()

#save the figure if you like
if save_fig:
    figure_name='plots/PL goals_' + season_span + '.pdf'
    plt.savefig(figure_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')

plt.show()

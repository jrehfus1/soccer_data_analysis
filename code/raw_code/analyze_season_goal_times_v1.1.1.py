################################################################################
#author: JER
#date of last modification: 201022
#summary of last modification: separated this script from other season-spanning analyses of goals data for clarity

################################################################################
##### description #####
#this script generates four plots, based on goals data from a single EPL season
#   1) histogram of the game times at which all goals were scored from all matches during the season
#       a Chi-square test is used to determine whether or not goals are scored uniformly throughout matches
#   2) histogram of the game times at which all goals were scored by the home team and away team from all matches during the season
#   3) histogram of the game times at which game-winning goals were scored from all matches during the season

################################################################################
##### import packages #####
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

################################################################################
##### decide whether or not to save the figures that this script produces #####
save_figs = False
out_path_figs = '../../figures/exploratory_figures/'

################################################################################
##### read in the data file containing the goals data from the season of choice #####
#season_span = '19_20'
season_span = input('\n=== Enter season span (eg. 19_20): ')
in_file = season_span + '_PL_goals_web_data.csv'
in_path = '../../data/raw_data/'
match_results_df = pd.read_csv(in_path+in_file)

################################################################################
##### compile the times at which goals were scored this season #####
home_goal_minutes = [] #make a list containing the times at which goals were scored by the home team this season
away_goal_minutes = [] #make a list containing the times at which goals were scored by the away team this season
winning_goal_minutes = [] #make a list containing the times at which tieing goals were scored
winning_goal_minutes = [] #make a list containing the times at which winning goals were scored
for index, row in match_results_df.iterrows():

    tie_test = False
    home_team_won = False
    away_team_won = False
    game_goal_difference = row['home final score'] - row['away final score']
    if game_goal_difference == 0:
        tie_test = True
    else:
        if game_goal_difference > 0:
            home_team_won = True
        else:
            away_team_won = True

    curr_game_home_goal_minutes = [] #keep track of the times at which goals were scored by the home team
    curr_game_away_goal_minutes = [] #keep track of the times at which goals were scored by the away team
    if row['home final score'] > 0: #a goal was scored by the home team
        goal_times = row['home goal times'][1:-1].split(',')
        for minute in goal_times:
            curr_game_home_goal_minutes.append(int(minute.strip()[1:-1]))
    if row['away final score'] > 0: #a goal was scored by the away team
        goal_times = row['away goal times'][1:-1].split(',')
        for minute in goal_times:
            curr_game_away_goal_minutes.append(int(minute.strip()[1:-1]))

    #get the tieing or winning goal times in all games in which goals were scored
    if tie_test and row['home final score'] > 0: #there was a tie and goals were scored
        winning_goal_minutes.append( max(curr_game_home_goal_minutes + curr_game_away_goal_minutes)  ) #the last goal scored was the tieing one
    elif home_team_won:
        winning_goal_minutes.append( curr_game_home_goal_minutes[ -game_goal_difference ] ) #this is the goal that sealed victory for the home team
    elif away_team_won:
        winning_goal_minutes.append( curr_game_away_goal_minutes[ game_goal_difference ] ) #this is the goal that sealed victory for the away team

    home_goal_minutes = home_goal_minutes + curr_game_home_goal_minutes #record the goal minutes for the home team
    away_goal_minutes = away_goal_minutes + curr_game_away_goal_minutes #record the goal minutes for the away team

################################################################################
##### bin the goal times data for each match this season #####
goal_minutes = home_goal_minutes + away_goal_minutes

#goal_times_bin_settings = range(1,92) #use one minute bins
#goal_times_bin_settings = list( range(1,46,2)  ) + list( range(46,91,2) ) + [91] #use two minute bins for normal time, one minute for stoppage time
goal_times_bin_settings = list( range(1,46,4)  ) + list( range(46,91,4) ) + [91] #use for minute bins for normal time, one minute for stoppage time
#print( goal_times_bin_settings )

[goal_times_bin_counts, goal_times_bin_edges] = np.histogram(goal_minutes, bins=goal_times_bin_settings)
#print( goal_times_bin_counts )
first_half_rt_goal_bin_counts = goal_times_bin_counts[0:11] #bin counts for goals scored in regular time of the first half
first_half_st_goal_bin_count = goal_times_bin_counts[11] #bin count for goals scored in stoppage time of the first half
second_half_rt_goal_bin_counts = goal_times_bin_counts[12:23] #bin counts for goals scored in regular time of the second half
second_half_st_goal_bin_count = goal_times_bin_counts[23] #bin count for goals scored in stoppage time of the second half

avg_goals_per_minute = ( sum(first_half_rt_goal_bin_counts) + sum(second_half_rt_goal_bin_counts) ) / 88 #calculate the average number of goals scored throughout the season per minute, excluding stoppage time
print('  ' + str(len(goal_minutes)) + ' goals were scored in PL season ' + season_span + '.')
print('    {:0.1f} % of them were scored outside of stoppage time.'.format( 100 * ( sum(first_half_rt_goal_bin_counts) + sum(second_half_rt_goal_bin_counts) ) / sum(goal_times_bin_counts) ) )
print('  on average, {:0.2f} goals were scored per combined game minute, excluding stoppage time.'.format(avg_goals_per_minute)) #':' introduces format spec, 0 enables sign-aware zero-padding for numeric types, .2 sets the precision to 2 decimal places, and f displays the number as a fixed-point number

################################################################################
##### bin the winning goal times data for each match this season #####
[winning_goal_minutes_bin_counts, winning_goal_minutes_bin_edges] = np.histogram(winning_goal_minutes, bins=goal_times_bin_settings)

################################################################################
##### use a chi-square goodness of fit test to determine if goals are scored uniformly throught matches #####
#https://stats.stackexchange.com/questions/110718/chi-squared-test-with-scipy-whats-the-difference-between-chi2-contingency-and
X_square_alpha = 0.05 #we will reject the null hypothesis that goals are evenly distributed if the X squared p-value is less than this
goals_per_min_no_stoppage = np.concatenate( (first_half_rt_goal_bin_counts, second_half_rt_goal_bin_counts), axis=0 )
X_square_statistic, X_square_p_value = stats.chisquare(goals_per_min_no_stoppage) #I am going to use the scipy package to calculate the p-value for me
if X_square_p_value < X_square_alpha:
    print('  Goals did NOT occur with equal probability throughout these matches.')
else:
    print('  Goals DID occur with equal probability throughout these matches.')
print('    Chi-square p-value = {:0.3f}'.format(X_square_p_value))

################################################################################
##### plot the results of the goal times analysis #####
fig_01 = plt.figure(figsize=(10, 5))
fig_01.suptitle('Season: ' + season_span)
grid_01 = plt.GridSpec(1, 2)
axes_01 = []
axes_01.append( fig_01.add_subplot(grid_01[0, 0]) )
axes_01.append( fig_01.add_subplot(axes_01[0].twinx()) )
axes_01.append( fig_01.add_subplot(grid_01[0, 1]) )
axes_01.append( fig_01.add_subplot(axes_01[2].twinx()) )

axes_01[0].set_title('when goals were scored')
axes_01[0].set_xlabel('minute', fontsize=14, color='black')
axes_01[0].set_ylabel('normal time', fontsize=14, color=(0.37,0.73,0.49))
axes_01[0].set_xlim(1, 91)
axes_01[0].set_xticks( [10, 20, 30, 40, 45, 50, 60, 70, 80, 90] )
axes_01[0].set_ylim(0, 100)
axes_01[0].tick_params(axis='y', labelcolor=(0.37,0.73,0.49))
axes_01[0].set_yticks(range(0,101,10))
axes_01[0].hist([x for x in goal_minutes if x < 45], density=False, bins=goal_times_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[0].hist([x for x in goal_minutes if x > 45 and x < 90], density=False, bins=goal_times_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[0].plot([0,45], [avg_goals_per_minute * 4, avg_goals_per_minute * 4], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored
axes_01[0].plot([46,90], [avg_goals_per_minute * 4, avg_goals_per_minute * 4], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored

axes_01[1].set_ylabel('stoppage time', fontsize=14, color=(0.69,0.23,0.56))
axes_01[1].set_ylim(0, 100)
axes_01[1].tick_params(axis='y', labelcolor=(0.69,0.23,0.56))
axes_01[1].set_yticks(range(0,101,10))
axes_01[1].hist([x for x in goal_minutes if x == 45 or x == 90], density=False, bins=goal_times_bin_settings, color=(0.69,0.23,0.56))  #`density=True` makes probabilities, `density=False` uses raw counts

axes_01[2].set_title('when goals were scored')
axes_01[2].set_xlabel('minute', fontsize=14, color='black')
axes_01[2].set_ylabel('normal time', fontsize=14, color=(0.37,0.73,0.49))
axes_01[2].set_xlim(1, 91)
axes_01[2].set_xticks( [10, 20, 30, 40, 45, 50, 60, 70, 80, 90] )
axes_01[2].set_ylim(0, 50)
axes_01[2].tick_params(axis='y', labelcolor=(0.37,0.73,0.49))
axes_01[2].set_yticks(range(0,51,10))
axes_01[2].hist([x for x in home_goal_minutes if x < 45], density=False, bins=goal_times_bin_settings, color=(0.07,0.41,0.98), alpha=0.4)  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[2].hist([x for x in home_goal_minutes if x > 45 and x < 90], density=False, bins=goal_times_bin_settings, color=(0.07,0.41,0.98), alpha=0.4)  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[2].hist([x for x in away_goal_minutes if x < 45], density=False, bins=goal_times_bin_settings, color=(0.96, 0.69, 0.36), alpha=0.4)  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[2].hist([x for x in away_goal_minutes if x > 45 and x < 90], density=False, bins=goal_times_bin_settings, color=(0.96, 0.69, 0.36), alpha=0.4)  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[2].plot([0,45], [avg_goals_per_minute * 2, avg_goals_per_minute * 2], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored
axes_01[2].plot([46,90], [avg_goals_per_minute * 2, avg_goals_per_minute * 2], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored

axes_01[3].set_ylabel('stoppage time', fontsize=14, color=(0.69,0.23,0.56))
axes_01[3].set_ylim(0, 50)
axes_01[3].tick_params(axis='y', labelcolor=(0.69,0.23,0.56))
axes_01[3].set_yticks(range(0,51,10))
axes_01[3].hist([x for x in home_goal_minutes if x == 45 or x == 90], density=False, bins=goal_times_bin_settings, color=(0.07,0.41,0.98), alpha=0.4)  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[3].hist([x for x in away_goal_minutes if x == 45 or x == 90], density=False, bins=goal_times_bin_settings, color=(0.96, 0.69, 0.36), alpha=0.4)  #`density=True` makes probabilities, `density=False` uses raw counts

fig_01.tight_layout()

if save_figs: #save the figure if you like
    figure_01_name = season_span + '_PL_goal_times.pdf'
    plt.savefig(out_path_figs + figure_01_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_01_name)

################################################################################
##### plot the results of the winning goal times analysis #####
fig_02 = plt.figure(figsize=(5,5))
fig_02.suptitle('Season: ' + season_span)
grid_02 = plt.GridSpec(3, 3)
axes_02 = []
axes_02.append( fig_02.add_subplot(grid_02[:, :]) )

axes_02[0].set_title('game winners')
axes_02[0].set_xlabel('frequency', fontsize=14, color='black')
axes_02[0].set_ylabel('minute', fontsize=14, color='black')
axes_02[0].set_xlim(1, 91)
axes_02[0].set_ylim(0, 100)
axes_02[0].hist(winning_goal_minutes, density=False, bins=goal_times_bin_settings, color=(0.37,0.73,0.49))

################################################################################
##### show the figures #####
plt.show()

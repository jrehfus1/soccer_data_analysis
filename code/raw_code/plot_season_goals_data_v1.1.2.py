################################################################################
#author: JER
#date of last modification: 200923
#summary of last modification: added more informative comments

################################################################################
##### description #####
#this script generates four plots, based on goals data from a single EPL season
#   1) histogram of the time of the game at which all goals from all matches during the season were scored
#       a Chi-square test is used to determine whether or not goals are scored uniformly throughout matches
#   2) histogram of the total number of goals scored in matches
#       this histogram is also fit to a Poisson distribution
#   3) histogram of the final goal difference in matches
#   4) histogram of the final goal difference in matches from the perspective of the home team
#       a Chi-square test is used to determine whether or not the home and away teams are equally likely to win

################################################################################
##### import packages #####
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

################################################################################
##### decide whether or not to save the figures that this script produces #####
save_figs = 0
out_path_figs = '../../figures/exploratory_figures/'

################################################################################
##### read in the data file containing the goals data from the season of choice #####
#season_span = '19_20'
season_span = input('\n=== Enter season span (eg. 19_20): ')
in_file = season_span + '_PL_goals_web_data.csv'
in_path = '../../data/tidy_data/'
match_results_df = pd.read_csv(in_path+in_file)

################################################################################
##### analyze the times at which goals were scored this season #####
goal_minutes = [] #make a list containing the times at which goals were scored
for index, row in match_results_df.iterrows():
    if len(row['home goal times']) > 2: #a goal was scored by the home team
        goal_times = row['home goal times'][1:-1].split(',')
        for minute in goal_times:
            goal_minutes.append(int(minute.strip()[1:-1]))
    if len(row['away goal times']) > 2: #a goal was scored by the home team
        goal_times = row['away goal times'][1:-1].split(',')
        for minute in goal_times:
            goal_minutes.append(int(minute.strip()[1:-1]))

##### bin the goal times data for each match this season #####
goal_times_bin_settings = range(1,92)
[goal_times_bin_counts, goal_times_bin_edges] = np.histogram(goal_minutes, bins=goal_times_bin_settings)
avg_goals_per_minute = (sum(goal_times_bin_counts[0:44]) + sum(goal_times_bin_counts[45:89])) / (len(goal_times_bin_counts[0:44]) + len(goal_times_bin_counts[45:89])) #calculate the average number of goals scored throughout the season per minute, excluding stoppage time
print('  ' + str(len(goal_minutes)) + ' goals were scored in PL season ' + season_span + '.')
print('    {:0.1f} % of them were scored outside of stoppage time.'.format( 100*(sum(goal_times_bin_counts[0:44]) + sum(goal_times_bin_counts[45:89]))/len(goal_minutes) ) )
print('  on average, {:0.2f} goals were scored per combined game minute, excluding stoppage time.'.format(avg_goals_per_minute)) #':' introduces format spec, 0 enables sign-aware zero-padding for numeric types, .2 sets the precision to 2 decimal places, and f displays the number as a fixed-point number

##### use a chi-square goodness of fit test to determine if goals are scored uniformly throught matches #####
#https://stats.stackexchange.com/questions/110718/chi-squared-test-with-scipy-whats-the-difference-between-chi2-contingency-and
X_square_alpha = 0.05 #we will reject the null hypothesis that goals are evenly distributed if the X squared p-value is less than this
goals_per_min_no_stoppage = np.concatenate((goal_times_bin_counts[0:44], goal_times_bin_counts[45:89]), axis=0)
X_square_statistic, X_square_p_value = stats.chisquare(goals_per_min_no_stoppage) #I am going to use the scipy package to calculate the p-value for me
if X_square_p_value < X_square_alpha:
    print('  Goals did NOT occur with equal probability throughout these matches.')
else:
    print('  Goals DID occur with equal probability throughout these matches.')
print('    Chi-square p-value = {:0.3f}'.format(X_square_p_value))

##### plot the results of your goal times analysis #####
fig_01 = plt.figure(figsize=(5, 5))
fig_01.suptitle('Season: ' + season_span)
grid_01 = plt.GridSpec(3, 3)
axes_01 = []
axes_01.append( fig_01.add_subplot(grid_01[:, :]) )
axes_01.append( fig_01.add_subplot(axes_01[0].twinx()) )

axes_01[0].set_title('when goals were scored')
axes_01[0].set_xlabel('minute', fontsize=14, color='black')
axes_01[0].set_ylabel('normal time', fontsize=14, color=(0.37,0.73,0.49))
axes_01[0].set_xlim(1, 91)
axes_01[0].set_ylim(0, 25)
axes_01[0].tick_params(axis='y', labelcolor=(0.37,0.73,0.49))
axes_01[0].set_yticks(range(0,26,5))
axes_01[0].hist([x for x in goal_minutes if x < 45], density=False, bins=goal_times_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[0].hist([x for x in goal_minutes if x > 45 and x < 90], density=False, bins=goal_times_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes_01[0].plot([0,45], [avg_goals_per_minute, avg_goals_per_minute], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored
axes_01[0].plot([46,90], [avg_goals_per_minute, avg_goals_per_minute], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored

axes_01[1].set_ylabel('stoppage time', fontsize=14, color=(0.69,0.23,0.56))
axes_01[1].set_ylim(0, 100)
axes_01[1].tick_params(axis='y', labelcolor=(0.69,0.23,0.56))
axes_01[1].hist([x for x in goal_minutes if x == 45 or x == 90], density=False, bins=goal_times_bin_settings, color=(0.69,0.23,0.56))  #`density=True` makes probabilities, `density=False` uses raw counts

fig_01.tight_layout()

if save_figs: #save the figure if you like
    figure_01_name = season_span + '_PL_goal_times.pdf'
    plt.savefig(out_path_figs + figure_01_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_01_name)

################################################################################
##### analyze the total number of goals scored in each match #####
total_goals_in_match = match_results_df['home final score'] +  match_results_df['away final score'] #new data series with total number of goals scored for each match

tot_goals_bin_settings = range(0,12)
tot_goals_bin_settings = [edge - 0.5 for edge in tot_goals_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
if max(total_goals_in_match) > 10:
    print('WARNING: default bin range was insufficient, so it was adjusted')
    tot_goals_bin_settings = range(0,max(total_goals_in_match)+2)
    tot_goals_bin_settings = [edge - 0.5 for edge in tot_goals_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
avg_goals_per_match = sum(total_goals_in_match)/len(match_results_df)
print('  on average, {:0.2f} goals were scored in each match this season.'.format(avg_goals_per_match))

##### fit a Poisson probability mass function to the binned goals per match data #####
#define the probability mass function
def Poisson_pmf(lam, k): #lambda is the mean value of occurrences per time interval, k is the number of occurrences per time interval
    return((lam**k) * (2.718**(-lam)) / np.math.factorial(k))
#make some realistic k values and calculate the pmf at those k values, then multiply by the total number of matches this season
Poisson_pmf_goals_per_match_df = pd.DataFrame( {'k values':np.arange(11)} )
Poisson_pmf_goals_per_match_df['Poisson counts'] = Poisson_pmf_goals_per_match_df.apply(lambda row: Poisson_pmf(avg_goals_per_match, row['k values']), axis=1) * len(match_results_df)

##### plot the results of the goals scored per match analysis #####
fig_02 = plt.figure(figsize=(5, 5))
fig_02.suptitle('Season: ' + season_span)
grid_02 = plt.GridSpec(3, 3)
axes_02 = []
axes_02.append( fig_02.add_subplot(grid_02[:, :]) )

axes_02[0].set_title('goals scored per match')
axes_02[0].set_xlabel('goals scored', fontsize=14, color='black')
axes_02[0].set_ylabel('matches', fontsize=14, color='black')
axes_02[0].set_xlim(-0.5, 10.5)
axes_02[0].set_ylim(0, 120)
axes_02[0].plot([avg_goals_per_match, avg_goals_per_match], [0,380], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored in a match
axes_02[0].hist(total_goals_in_match, density=False, bins=tot_goals_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes_02[0].plot(Poisson_pmf_goals_per_match_df['k values'], Poisson_pmf_goals_per_match_df['Poisson counts'], marker='o', linestyle='', color=(0.07,0.41,0.98))

fig_02.tight_layout()

if save_figs: #save the figure if you like
    figure_02_name = season_span + '_PL_goals_per_match.pdf'
    plt.savefig(out_path_figs + figure_02_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_02_name)

################################################################################
##### analyze the goal difference data for each match #####
goal_difference = abs( match_results_df['home final score'] -  match_results_df['away final score'] ) #new data series

goal_diff_bin_settings = range(0,12)
goal_diff_bin_settings = [edge - 0.5 for edge in goal_diff_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
if max(goal_difference) > 10:
    print('WARNING: default GD bin range was insufficient, so it was adjusted')
    goal_diff_bin_settings = range(0, max(goal_difference)+2)
    goal_diff_bin_settings = [edge - 0.5 for edge in goal_diff_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values
goal_difference_games_with_winner = goal_difference[ goal_difference > 0 ] #only matches where there was a winner and a loser
avg_goal_difference_per_match = goal_difference.mean()
avg_goal_difference_per_match_with_winner = goal_difference_games_with_winner.mean()
print( '  on average, the margin of victory was {:0.2f} goals for matches with a victor.'.format(avg_goal_difference_per_match_with_winner) )
print( '    {:0.1f} % of matches were won.'.format( 100*len(goal_difference_games_with_winner)/380 ) )
#print(len(goal_difference[goal_difference>3]))

##### plot the results of your goal difference analysis #####
fig_03 = plt.figure(figsize=(5, 5))
fig_03.suptitle('Season: ' + season_span)
grid_03 = plt.GridSpec(3, 3)
axes_03 = []
axes_03.append( fig_03.add_subplot(grid_03[:, :]) )

axes_03[0].set_title('final goal difference per match')
axes_03[0].set_xlabel('goal difference', fontsize=14, color='black')
axes_03[0].set_ylabel('matches', fontsize=14, color='black')
axes_03[0].set_xlim(-0.5, 10.5)
axes_03[0].set_ylim(0, 200)
axes_03[0].plot([avg_goal_difference_per_match, avg_goal_difference_per_match], [0,380], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average # goals scored in a match
axes_03[0].plot([avg_goal_difference_per_match_with_winner, avg_goal_difference_per_match_with_winner], [0,380], linewidth=2.0, linestyle=':', color=(0.07,0.41,0.98)) #plot a line showing the average victory margin in a match
axes_03[0].hist(goal_difference, density=False, bins=goal_diff_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts

fig_03.tight_layout()

if save_figs: #save the figure if you like
    figure_03_name = season_span + '_PL_goal_difference_per_match.pdf'
    plt.savefig(out_path_figs + figure_03_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_03_name)

################################################################################
##### assess home field advantage via goal difference from the home team's perspective #####
home_team_goal_difference = match_results_df['home final score'] -  match_results_df['away final score'] #makes a new data series with home team goal diff for each match

home_goal_diff_bin_settings = range(-10,12)
home_goal_diff_bin_settings = [edge - 0.5 for edge in home_goal_diff_bin_settings ] #slide the edges back by 0.5 so that bins are centered on integer values

home_team_won = home_team_goal_difference[ home_team_goal_difference > 0 ] #only matches where the home team won
home_team_drew = home_team_goal_difference[ home_team_goal_difference == 0 ] #only matches where the home team drew
home_team_lost = home_team_goal_difference[ home_team_goal_difference < 0 ] #only matches where the home team lost
print( '      the home team won {:0.1f} % of matches.'.format(100*(home_team_goal_difference > 0).sum()/380) )
print( '      the away team won {:0.1f} % of matches.'.format(100*(home_team_goal_difference < 0).sum()/380) )
print( '      {:0.1f} % of matches ended in a draw.'.format(100*(home_team_goal_difference == 0).sum()/380) )

##### use a chi-square test to determine if the home and away team are equally likely to win #####
X_square_alpha = 0.05 #we will reject the null hypothesis that the home and away teams are equally likely to win if the X squared p-value is less than this
X_square_statistic, X_square_p_value = stats.chisquare( [(home_team_goal_difference > 0).sum(), (home_team_goal_difference < 0).sum()] )
if X_square_p_value < X_square_alpha:
    print('  The home and away teams are NOT equally likely to win the match.')
else:
    print('  The home and away teams ARE equally likely to win the match.')
print('    Chi-square p-value = {:0.3f}'.format(X_square_p_value))

##### plot the home team vs away team goals scored #####
fig_04 = plt.figure(figsize=(5, 5))
fig_04.suptitle('Season: ' + season_span)
grid_04 = plt.GridSpec(3, 3)
axes_04 = []
axes_04.append( fig_04.add_subplot(grid_04[:, :]) )

axes_04[0].set_title('home team goal difference per match')
axes_04[0].set_xlabel('home team goal difference', fontsize=14, color='black')
axes_04[0].set_ylabel('matches', fontsize=14, color='black')
axes_04[0].set_xlim(-10.5, 10.5)
axes_04[0].set_ylim(0, 100)
axes_04[0].plot([home_team_goal_difference.mean(), home_team_goal_difference.mean()], [0,380], linewidth=2.0, linestyle='--', color='gray') #plot a line showing the average goal difference for the home team in a match
axes_04[0].hist(home_team_drew, density=False, bins=home_goal_diff_bin_settings, color=(0.37,0.73,0.49))  #`density=True` makes probabilities, `density=False` uses raw counts
axes_04[0].hist(home_team_won, density=False, bins=home_goal_diff_bin_settings, color=(0.07,0.41,0.98))  #`density=True` makes probabilities, `density=False` uses raw counts
axes_04[0].hist(home_team_lost, density=False, bins=home_goal_diff_bin_settings, color=(0.69,0.23,0.56))  #`density=True` makes probabilities, `density=False` uses raw counts

fig_04.tight_layout()

if save_figs: #save the figure if you like
    figure_04_name = season_span + '_PL_home_team_goal_difference_per_match.pdf'
    plt.savefig(out_path_figs + figure_04_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_04_name)

################################################################################
##### show the figures #####
plt.show()

################################################################################
##### separate the output in the command line for legibility #####
print('\n')

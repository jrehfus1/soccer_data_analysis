#this code plots the league points, goal difference, total goals, and league position for each premier league team as a function of week

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from team_colors import team_primary_color_dict as tpcd
from team_colors import team_secondary_color_dict as tscd

##### decide whether or not to save the figure that this script produces #####
save_figs = 0

##### decide whether or not to save the data table that this script produces #####
save_created_data_frames = 1

##### read in the data file containing the goals data from the season of choice #####
#season_span = '19_20'
season_span = input('\n=== Enter season span (eg. 19_20): ')
in_file = season_span + '_PL_goals_web_data.csv'
match_results_df = pd.read_csv(in_file)
#print( match_results_df.head() )
#print( match_results_df.info() )
#print( match_results_df.shape )
#print( match_results_df.describe() )
#print( match_results_df['home team name'].describe() )
#print( match_results_df['match week'].max() )
team_names_list = match_results_df['home team name'].drop_duplicates().tolist() #make a list of the unique team names for this season

##### make an empty dataframe for league score, goal difference, and goals scored for each team for each match week #####
#this will have 38 rows and 20 columns and contain the number of league points that each team won each match week
league_scores_df = pd.DataFrame( columns=team_names_list, index=range(0, match_results_df['match week'].max()+1) )
league_scores_df.index.names = ['match week'] #change the name of the index to 'match week'
league_scores_df.loc[0, :] = 0 #every team starts the season (mw 0) with 0 league points, 0 goal difference, and 0 goals scored
#print( league_scores_df.head() )
goal_diff_df = league_scores_df.copy() #make another dataframe that will keep track of goal difference by week for each team. using .copy() unlinks the two dataframes
goals_scored_df = league_scores_df.copy() #make another dataframe that will keep track of goal difference by week for each team. using .copy() unlinks the two dataframes

league_positions_df = league_scores_df.copy() #make another dataframe that will keep track of league position by week for each team. using .copy() unlinks the two dataframes
league_positions_df.loc[0, :] = len(team_names_list)/2 #every team starts the season in the middle of the pack
#print(league_positions_df)

##### fill in the values for three of the empty dataframes you just made #####
#these three dataframes are necessary for determining the league positions
#NOTE: these are not cumulative values at first
for index, row in match_results_df.iterrows():
    #temporarily store the following data so that it only has to be accessed once
    mw = row['match week']
    htm = row['home team name']
    atm = row['away team name']
    hfs = row['home final score']
    afs = row['away final score']
    hgd = hfs-afs #goal difference for the home team
    #update the three dataframes you initiated above
    goals_scored_df.loc[ mw, htm ] = hfs
    goals_scored_df.loc[ mw, atm ] = afs
    goal_diff_df.loc[ mw, htm ] = hgd
    goal_diff_df.loc[ mw, atm ] = -hgd
    if hgd == 0: #both teams tied, so both get 1 league point
        league_scores_df.loc[ mw, htm ] = 1
        league_scores_df.loc[ mw, atm ] = 1
    elif hgd > 0: #home team won, so they get 3 league points while the away team gets 0
        league_scores_df.loc[ mw, htm ] = 3
        league_scores_df.loc[ mw, atm ] = 0
    else: #if the away team won, it got 3 league points
        league_scores_df.loc[ mw, htm ] = 0
        league_scores_df.loc[ mw, atm ] = 3
#update each of the dataframes so that each column has a running cumulative sum
league_scores_df = league_scores_df.cumsum()
goal_diff_df = goal_diff_df.cumsum()
goals_scored_df = goals_scored_df.cumsum()
#print( goal_diff_df )

##### determine the league position of each team for each match week #####
match_week_df = pd.DataFrame( data={'team name':team_names_list} ) #initialize a temporary dataframe with only the team names for now
for mw in range(1, match_results_df['match week'].max()+1): #go through each match week, except the '0th'
    #update the temporary dataframe with league points, goal difference, and total goals scored
    match_week_df['LP'] = league_scores_df.loc[mw].values.tolist()
    match_week_df['GD'] = goal_diff_df.loc[mw].values.tolist()
    match_week_df['TG'] = goals_scored_df.loc[mw].values.tolist()

    #make another temporary dataframe, this one containing the preliminary league positions for each team
    sorted_match_week_df = match_week_df.sort_values( by=['LP', 'GD', 'TG'], ascending=False ) #sort teams by league points, then goal difference, then total goals scored
    sorted_match_week_df = sorted_match_week_df.reset_index( drop=True ) #reset the index values for the sorted data, and get rid of the old index values
    sorted_match_week_df['league position'] = sorted_match_week_df.index + 1 #give preliminary league positions to each team (before correcting for ties)

    #correct the league position for any teams that are tied
    is_duplicate = sorted_match_week_df.duplicated( ['LP', 'GD', 'TG'], keep='first' )
    for index, row in sorted_match_week_df.iterrows():
        if is_duplicate[index]:
            sorted_match_week_df.loc[index, 'league position'] = sorted_match_week_df.loc[index-1, 'league position']

    #update league positions for this match week
    for index, row in sorted_match_week_df.iterrows():
        league_positions_df.loc[ mw, row['team name'] ] = row['league position']
#print(league_positions_df['Liverpool FC'])

##### rearrange the columns of each dataframe so that the plot legends will be sorted #####
orig_cols = league_scores_df.columns.tolist()

#define a function that rearranges the columns of a dataframe based on the values in the last row
def sort_by_final_values( team_values_by_mw_df, team_names_list, orig_cols ):
    final_values = team_values_by_mw_df.iloc[-1].values.tolist()
    sorted_final_team_values = sorted( final_values, reverse=True ) #sort descending (highest to lowest)
    cols_by_val = [None] * len(team_names_list) #initialize a list to keep track of the new order of column names
    for i in range(0, len(team_names_list)):
        new_idx = sorted_final_team_values.index( final_values[i] )
        #find the next highest index where no team has been assigned yet
        #this will be unchanged if no team has been assigned to the new index yet, but it will be one higher if this is the second team with this exact final value, or two higher if it is the third, etc.
        new_idx = cols_by_val.index(None, new_idx, len(cols_by_val) )
        cols_by_val[new_idx] = orig_cols[i]
    team_values_by_mw_df = team_values_by_mw_df[cols_by_val]
    return( team_values_by_mw_df )

#implement the above function to sort the columns of these dataframes
league_scores_df = sort_by_final_values( league_scores_df, team_names_list, orig_cols )
goal_diff_df = sort_by_final_values( goal_diff_df, team_names_list, orig_cols )
goals_scored_df = sort_by_final_values( goals_scored_df, team_names_list, orig_cols )

#sort the columns of the
final_league_positions = league_positions_df.loc[38].values.tolist()
cols_by_lp = []
for i in range(1, len(team_names_list)+1):
    new_lp_idx = final_league_positions.index(i)
    cols_by_lp.append( orig_cols[new_lp_idx] )
league_positions_df = league_positions_df[cols_by_lp]
#print(league_positions_df)

##### save these dataframes as csv files if you like #####
if save_created_data_frames:
    ls_csv_out_name = season_span + '_PL_league_score_data.csv'
    print( '  saving ' + ls_csv_out_name )
    league_scores_df.to_csv(ls_csv_out_name)

    gd_csv_out_name = season_span + '_PL_goal_difference_data.csv'
    print( '  saving ' + gd_csv_out_name )
    goal_diff_df.to_csv(gd_csv_out_name)

    gs_csv_out_name = season_span + '_PL_goals_scored_data.csv'
    print( '  saving ' + gs_csv_out_name )
    goals_scored_df.to_csv(gs_csv_out_name)

    lp_csv_out_name = season_span + '_PL_league_position_data.csv'
    print( '  saving ' + lp_csv_out_name )
    league_positions_df.to_csv(lp_csv_out_name)

##### plot league points data #####
fig_01 = plt.figure(figsize=(10, 5))
fig_01.suptitle('Season: ' + season_span)
grid_01 = plt.GridSpec(3, 3)
axes_01 = []
axes_01.append( fig_01.add_subplot(grid_01[:, :]) )
axes_01[0].set_title('when league points were won')
axes_01[0].set_xlabel('match week', fontsize=14, color='black')
axes_01[0].set_ylabel('league points', fontsize=14, color='black')
axes_01[0].set_xlim(0, 38)
axes_01[0].set_ylim(0, 114)
for col in league_scores_df.columns:
    #the team's data will be plotted in their chosen color, if it exists. otherwise, it will be plotted in gray
    team_plot = league_scores_df.plot(y=col, use_index=True, color=tpcd.get(col, (0.5,0.5,0.5)), linewidth=2.0, marker='h', markerfacecolor=tscd.get(col, (0.5,0.5,0.5)), markeredgewidth=1, markersize=5, ax=axes_01[0])
    if col not in tpcd.keys() | col not in tscd.keys(): #if this team name is not in one of the color dictionaries yet, print out the team name so that it can be added
        print(col)

box = axes_01[0].get_position()
axes_01[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_01[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

if save_figs: #save the figure if you like
    figure_01_name = season_span + '_PL_league_points_by_week.pdf'
    plt.savefig(figure_01_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_01_name)

##### plot goal difference data #####
fig_02 = plt.figure(figsize=(10, 5))
fig_02.suptitle('Season: ' + season_span)
grid_02 = plt.GridSpec(3, 3)
axes_02 = []
axes_02.append( fig_02.add_subplot(grid_02[:, :]) )
axes_02[0].set_title('goal difference throughout the season')
axes_02[0].set_xlabel('match week', fontsize=14, color='black')
axes_02[0].set_ylabel('goal difference', fontsize=14, color='black')
axes_02[0].set_xlim(0, 38)
axes_02[0].set_ylim(-80, 80)
for col in goal_diff_df.columns:
    #the team's data will be plotted in their chosen color, if it exists. otherwise, it will be plotted in gray
    team_plot = goal_diff_df.plot(y=col, use_index=True, color=tpcd.get(col, (0.5,0.5,0.5)), linewidth=2.0, marker='h', markerfacecolor=tscd.get(col, (0.5,0.5,0.5)), markeredgewidth=1, markersize=5, ax=axes_02[0])
    if col not in tpcd.keys() | col not in tscd.keys(): #if this team name is not in one of the color dictionaries yet, print out the team name so that it can be added
        print(col)

box = axes_02[0].get_position()
axes_02[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_02[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

if save_figs: #save the figure if you like
    figure_02_name = season_span + '_PL_goal_difference_by_week.pdf'
    plt.savefig(figure_02_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_02_name)

##### plot total goals data #####
fig_03 = plt.figure(figsize=(10, 5))
fig_03.suptitle('Season: ' + season_span)
grid_03 = plt.GridSpec(3, 3)
axes_03 = []
axes_03.append( fig_03.add_subplot(grid_03[:, :]) )
axes_03[0].set_title('goals scored throughout the season')
axes_03[0].set_xlabel('match week', fontsize=14, color='black')
axes_03[0].set_ylabel('total goals', fontsize=14, color='black')
axes_03[0].set_xlim(0, 38)
axes_03[0].set_ylim(0, 120)
for col in goals_scored_df.columns:
    #the team's data will be plotted in their chosen color, if it exists. otherwise, it will be plotted in gray
    team_plot = goals_scored_df.plot(y=col, use_index=True, color=tpcd.get(col, (0.5,0.5,0.5)), linewidth=2.0, marker='h', markerfacecolor=tscd.get(col, (0.5,0.5,0.5)), markeredgewidth=1, markersize=5, ax=axes_03[0])
    if col not in tpcd.keys() | col not in tscd.keys(): #if this team name is not in one of the color dictionaries yet, print out the team name so that it can be added
        print(col)

box = axes_03[0].get_position()
axes_03[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_03[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

if save_figs: #save the figure if you like
    figure_03_name = season_span + '_PL_total_goals_by_week.pdf'
    plt.savefig(figure_03_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_03_name)

##### plot league positions data #####
fig_04 = plt.figure(figsize=(10, 5))
fig_04.suptitle('Season: ' + season_span)
grid_04 = plt.GridSpec(3, 3)
axes_04 = []
axes_04.append( fig_04.add_subplot(grid_04[:, :]) )
axes_04[0].set_title('league position throughout the season')
axes_04[0].set_xlabel('match week', fontsize=14, color='black')
axes_04[0].set_ylabel('league position', fontsize=14, color='black')
axes_04[0].set_xlim(0, 38)
axes_04[0].set_ylim(21, 0)
axes_04[0].set_yticks(np.arange(1, 21, step=1))
for col in league_positions_df.columns:
    #the team's data will be plotted in their chosen color, if it exists. otherwise, it will be plotted in gray
    team_plot = league_positions_df.plot(y=col, use_index=True, color=tpcd.get(col, (0.5,0.5,0.5)), linewidth=2.0, marker='h', markerfacecolor=tscd.get(col, (0.5,0.5,0.5)), markeredgewidth=1, markersize=5, ax=axes_04[0])
    if col not in tpcd.keys() | col not in tscd.keys(): #if this team name is not in one of the color dictionaries yet, print out the team name so that it can be added
        print(col)

box = axes_04[0].get_position()
axes_04[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_04[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

if save_figs: #save the figure if you like
    figure_04_name = season_span + '_PL_league_positions_by_week.pdf'
    plt.savefig(figure_04_name, dpi=150, format=None, transparent=True) #facecolor='w', edgecolor='w')
    print('Saved figure ' + figure_04_name)

plt.show()

##### print a new line to demarcate the end of the output from this script #####
print('\n')

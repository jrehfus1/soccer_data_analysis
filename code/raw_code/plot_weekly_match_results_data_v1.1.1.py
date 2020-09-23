################################################################################
#author: JER
#date of last modification: 201023
#summary of last modification: added some comments to improve readability

################################################################################
##### description #####
#this script plots the league points for each premier league team as a function of match week

################################################################################
##### import packages #####
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd

################################################################################
##### decide whether or not to save the figure that this script produces #####
save_figs = 0
out_path_figs = '../../figures/exploratory_figures/'

################################################################################
##### decide whether or not to save the dataframe that this script produces #####
save_created_data_frames = 0
out_path_dfs = '../../data/tidy_data/'

################################################################################
##### read in the data file containing the goals data from the season of choice #####
#season_span = '19_20'
season_span = input('\n=== Enter season span (eg. 19_20): ')
in_file = season_span + '_PL_goals_web_data.csv'
in_path = '../../data/tidy_data/'
match_results_df = pd.read_csv(in_path + in_file)

################################################################################
##### make empty dataframes to hold various data for each team for each match week #####
#these will each have 38 rows and 20 columns and contain the number of league points that each team won each match week
league_scores_df = pd.DataFrame( columns=['match week'] )
goal_diff_df = pd.DataFrame( columns=['match week'] )
goals_scored_df = pd.DataFrame( columns=['match week'] )

################################################################################
##### fill in the values of the dataframe containing weekly values using the data imported above #####
for index, row in match_results_df.iterrows():
    #if you have not put the match week information in the new data frame yet, add it
    if len(league_scores_df.index) < row['match week']:
        league_scores_df.loc[ row['match week'], 'match week' ] = row['match week']
        goal_diff_df.loc[ row['match week'], 'match week' ] = row['match week']
        goals_scored_df.loc[ row['match week'], 'match week' ] = row['match week']
    #if both teams tied, they each got 1 league point
    if row['home final score'] == row['away final score']:
        league_scores_df.loc[ row['match week'], row['home team name'] ] = 1
        league_scores_df.loc[ row['match week'], row['away team name'] ] = 1
    #if the home team won, it got 3 league points
    elif row['home final score'] > row['away final score']:
        league_scores_df.loc[ row['match week'], row['home team name'] ] = 3
        league_scores_df.loc[ row['match week'], row['away team name'] ] = 0
    #if the away team won, it got 3 league points
    else:
        league_scores_df.loc[ row['match week'], row['home team name'] ] = 0
        league_scores_df.loc[ row['match week'], row['away team name'] ] = 3
    #deterine the goal difference for this week for each team
    goal_diff_df.loc[ row['match week'], row['home team name'] ] = row['home final score'] - row['away final score']
    goal_diff_df.loc[ row['match week'], row['away team name'] ] = row['away final score'] - row['home final score']
    goals_scored_df.loc[ row['match week'], row['home team name'] ] = row['home final score']
    goals_scored_df.loc[ row['match week'], row['away team name'] ] = row['away final score']

################################################################################
##### save the weekly league points dataframe as a csv file if you like #####
if save_created_data_frames:
    csv_out_name = season_span + '_PL_league_points_data.csv'
    print( '  saving data as: ' + csv_out_name )
    league_scores_df.to_csv(out_path_dfs + csv_out_name, index=False)

################################################################################
##### get the cumulative league score for each team for each match week
# ( league_scores_df.iloc[:, 1:].cumsum() ) #this performs the cumsum operation on every column but the 'match week' column
cum_league_scores_df=pd.concat([league_scores_df.iloc[:, 0], league_scores_df.iloc[:, 1:].cumsum()], axis=1)
cum_goal_diff_df=pd.concat([goal_diff_df.iloc[:, 0], goal_diff_df.iloc[:, 1:].cumsum()], axis=1)
cum_goals_scored_df=pd.concat([goals_scored_df.iloc[:, 0], goals_scored_df.iloc[:, 1:].cumsum()], axis=1)
#print(cum_goals_scored_df)

################################################################################
##### determine the league position of each team for each match week #####
teams_list=cum_league_scores_df.columns[1:]
league_positions_df = pd.DataFrame( columns=cum_league_scores_df.columns )
league_positions_df['match week'] = cum_league_scores_df['match week']

for index_lev1, row_lev1 in cum_league_scores_df.iterrows():
    mw = row_lev1['match week']

    #cum_league_scores_df.loc[cum_league_scores_df['match week'] == 1]
    test_LP = cum_league_scores_df.loc[ cum_league_scores_df['match week'] == mw, teams_list ]
    test_GD = cum_goal_diff_df.loc[ cum_goal_diff_df['match week'] == mw, teams_list ]
    test_TG = cum_goals_scored_df.loc[ cum_goals_scored_df['match week'] == mw, teams_list ]
    #print(test_LP)

    match_week_df = pd.DataFrame( data={'team':teams_list, 'LP':test_LP.values.tolist()[0], 'GD':test_GD.values.tolist()[0], 'TG':test_TG.values.tolist()[0]} )
    #print(match_week_df)
    sorted_match_week_df = match_week_df.sort_values( by=['LP', 'GD', 'TG'], ascending=False ) #sort teams by league points, then goal difference, then total goals scored
    sorted_match_week_df = sorted_match_week_df.reset_index( drop=True ) #reset the index values for the sorted data, and get rid of the old index values
    sorted_match_week_df['league_position']=sorted_match_week_df.index + 1 #give preliminary league positions to each team (before correcting for ties)
    #print( sorted_match_week_df )

    #correct the league position for any teams that are tied
    is_duplicate = sorted_match_week_df.duplicated( ['LP', 'GD', 'TG'], keep='first' )
    for index, row in sorted_match_week_df.iterrows():
        if is_duplicate[index]:
            sorted_match_week_df.loc[index, 'league_position'] = sorted_match_week_df.loc[index-1, 'league_position']
    #print( sorted_match_week_df )

    #update league positions for this match week
    for index, row in sorted_match_week_df.iterrows():
        league_positions_df.loc[ mw, row['team'] ]=row['league_position']
#print( league_positions_df )

################################################################################
##### make a dictionary of the colors used to plot each team's data #####
#team_color_dict={'Liverpool FC': '#FF0000', 'Chelsea FC': '#0000FF'}
team_color_dict={'AFC Bournemouth': (0.85,0.22,0.18), 'Arsenal FC': (0.91,0.25,0.20), 'Aston Villa': (0.40,0.10,0.20), 'Brighton & Hove Albion': (0.04,0.33,0.65), 'Burnley FC': (0.51,0.14,0.30), 'Cardiff City': (0.13,0.26,0.91), 'Chelsea FC': (0.03,0.14,0.51), 'Crystal Palace': (0.02,0.29,0.59), 'Everton FC': (0.15,0.27,0.53), 'Fulham FC': (0.00,0.00,0.00), 'Huddersfield Town': (0.09,0.42,0.76), 'Hull City': (0.94,0.54,0.20), 'Leeds United': (0.75,0.59,0.36), 'Leicester City': (0.00,0.18,0.54), 'Liverpool FC': (0.89,0.24,0.20), 'Manchester City': (0.60,0.78,0.92), 'Manchester United': (0.78,0.21,0.17), 'Middlesbrough FC': (0.84,0.22,0.18), 'Newcastle United': (0.00,0.00,0.00), 'Norwich City': (0.33,0.66,0.32), 'Queens Park Rangers': (0.04,0.31,0.60), 'Sheffield United': (0.91,0.24,0.20), 'Southampton FC': (0.91,0.25,0.20), 'Stoke City': (0.82,0.22,0.18), 'Sunderland AFC': (0.87,0.23,0.19), 'Swansea City': (0.00,0.00,0.00), 'Tottenham Hotspur': (0.07,0.09,0.21), 'Watford FC': (0.99,0.95,0.19), 'West Bromwich Albion': (0.13,0.18,0.38), 'West Ham United': (0.38,0.09,0.16), 'Wolverhampton Wanderers': (0.88,0.66,0.18)}

team_second_color_dict={'AFC Bournemouth': (0.00,0.00,0.00), 'Arsenal FC': (1.00,1.00,1.00), 'Aston Villa': (0.64,0.80,0.99), 'Brighton & Hove Albion': (1.00,1.00,1.00), 'Burnley FC': (0.58,0.82,0.93), 'Cardiff City': (1.00,1.00,1.00), 'Chelsea FC': (0.03,0.14,0.51), 'Crystal Palace': (0.91,0.25,0.20), 'Everton FC': (1.00,1.00,1.00), 'Fulham FC': (1.00,1.00,1.00), 'Huddersfield Town': (1.00,1.00,1.00), 'Hull City': (0.00,0.00,0.00), 'Leeds United': (0.75,0.59,0.36), 'Leicester City': (1.00,1.00,1.00), 'Liverpool FC': (0.89,0.24,0.20), 'Manchester City': (1.00,1.00,1.00), 'Manchester United': (1.00,1.00,1.00), 'Middlesbrough FC': (1.00,1.00,1.00), 'Newcastle United': (1.00,1.00,1.00), 'Norwich City': (0.97,0.93,0.19), 'Queens Park Rangers': (1.00,1.00,1.00), 'Sheffield United': (1.00,1.00,1.00), 'Southampton FC': (1.00,1.00,1.00), 'Stoke City': (1.00,1.00,1.00), 'Sunderland AFC': (1.00,1.00,1.00), 'Swansea City': (1.00,1.00,1.00), 'Tottenham Hotspur': (1.00,1.00,1.00), 'Watford FC': (0.00,0.00,0.00), 'West Bromwich Albion': (1.00,1.00,1.00), 'West Ham United': (0.28,0.69,0.90), 'Wolverhampton Wanderers': (0.00,0.00,0.00)}

################################################################################
##### plot the results of your analyses #####
fig, axes=plt.subplots(nrows=2, ncols=2, figsize=(15, 8))
fig.suptitle('Season: ' + season_span)

#plot league points as a function of match week
axes[0,0].set_title('when league points were won')
axes[0,0].set_xlabel('match week', fontsize=14, color='black')
axes[0,0].set_ylabel('league points', fontsize=14, color='black')
axes[0,0].set_xlim(1, 38)
axes[0,0].set_ylim(0, 114)
for col in cum_league_scores_df.columns:
    if col != 'match week': #do not plot the match week numbers, those are the x-axis
        #the team's data will be plotted in their chosen color, if it exists. otherwise, it will be plotted in gray
        team_plot=cum_league_scores_df.plot(x='match week', y=col, color=team_color_dict.get(col, (0.5,0.5,0.5)), linewidth=1.0, marker='h', markerfacecolor=team_second_color_dict.get(col, (0.5,0.5,0.5)), markeredgewidth=1,
        markersize=5, ax=axes[0,0])
        #if this team name is not in the color dictionary yet, print out the team name so that it can be added
        if col not in team_color_dict.keys():
            print(col)
axes[0,0].get_legend().set_visible(False)

#plot goal differential as a function of match week
axes[0,1].set_title('goal difference')
axes[0,1].set_xlabel('match week', fontsize=14, color='black')
axes[0,1].set_ylabel('goal difference', fontsize=14, color='black')
axes[0,1].set_xlim(1, 38)
axes[0,1].set_ylim(-80, 80)
for col in cum_goal_diff_df.columns:
    if col != 'match week': #do not plot the match week numbers, those are the x-axis
        #the team's data will be plotted in their chosen color, if it exists. otherwise, it will be plotted in gray
        team_plot=cum_goal_diff_df.plot(x='match week', y=col, color=team_color_dict.get(col, (0.5,0.5,0.5)), linewidth=1.0, marker='h', markerfacecolor=team_second_color_dict.get(col, (0.5,0.5,0.5)), markeredgewidth=1,
        markersize=5, ax=axes[0,1] )
axes[0,1].get_legend().set_visible(False)

#plot total goals as a function of match week
axes[1,0].set_title('total goals scored')
axes[1,0].set_xlabel('match week', fontsize=14, color='black')
axes[1,0].set_ylabel('total goals', fontsize=14, color='black')
axes[1,0].set_xlim(1, 38)
axes[1,0].set_ylim(0, 120)
for col in cum_goals_scored_df.columns:
    if col != 'match week': #do not plot the match week numbers, those are the x-axis
        #the team's data will be plotted in their chosen color, if it exists. otherwise, it will be plotted in gray
        team_plot=cum_goals_scored_df.plot(x='match week', y=col, color=team_color_dict.get(col, (0.5,0.5,0.5)), linewidth=1.0, marker='h', markerfacecolor=team_second_color_dict.get(col, (0.5,0.5,0.5)), markeredgewidth=1,
        markersize=5, ax=axes[1,0] )
axes[1,0].get_legend().set_visible(False)

#plot league positions as a function of match week
axes[1,1].set_title('corresponding league positions')
axes[1,1].set_xlabel('match week', fontsize=14, color='black')
axes[1,1].set_ylabel('league position', fontsize=14, color='black')
axes[1,1].set_xlim(1, 38)
axes[1,1].set_ylim(21, 0) #make y-axis decrease
axes[1,1].set_yticks(np.arange(1, 21, step=1)) #['Tom', 'Dick', 'Sue']
for col in league_positions_df.columns:
    if col != 'match week': #do not plot the match week numbers, those are the x-axis
        team_plot=league_positions_df.plot(x='match week', y=col, color=team_color_dict.get(col, (0.5,0.5,0.5)), linewidth=1.0, marker='h', markerfacecolor=team_second_color_dict.get(col, (0.5,0.5,0.5)), markeredgewidth=1,
        markersize=5, ax=axes[1,1],)
axes[1,1].get_legend().set_visible(False)

fig.tight_layout()

################################################################################
##### show the plots #####
plt.show()

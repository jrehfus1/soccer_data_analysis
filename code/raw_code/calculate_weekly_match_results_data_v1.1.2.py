################################################################################
#author: JER
#date of last modification: 201023
#summary of last modification: wrote initial program

################################################################################
##### description #####
#this script uses match results to calculate the following values for each premier league team as a function of week for a single season
#   1) weekly cumulative league points for each EPL team from a single season
#   2) weekly cumulative goal difference for each EPL team from a single season
#   3) weekly cumulative goals scored for each EPL team from a single season
#   4) weekly league position for each EPL team from a single season
#all four of these parameters are stored in separate dataframes and can be saved as output

################################################################################
##### import packages #####
import pandas as pd

################################################################################
##### decide whether or not to save the dataframes that this script produces #####
save_created_data_frames = 0
out_path_dfs = '../../data/tidy_data/'

################################################################################
##### read in the data file containing the goals data from the season of choice #####
season_span = input('\n=== Enter season span (eg. 19_20): ')
in_file = season_span + '_PL_goals_web_data.csv'
in_path = '../../data/raw_data/'
match_results_df = pd.read_csv(in_path + in_file)
#print( match_results_df.head() )
#print( match_results_df.info() )
#print( match_results_df.shape )
#print( match_results_df.describe() )
#print( match_results_df['home team name'].describe() )
#print( match_results_df['match week'].max() )

################################################################################
##### initialize empty dataframes to hold weekly league scores, goal differences, and goals scored for each team #####
#each of these will each have 38 rows and 20 columns
team_names_list = match_results_df['home team name'].drop_duplicates().tolist() #make a list of the unique team names for this season

league_scores_df = pd.DataFrame( columns=team_names_list, index=range(0, match_results_df['match week'].max()+1) ) #this df contains the number of league points that each team won each match week
league_scores_df.index.names = ['match week'] #change the name of the index to 'match week'
league_scores_df.loc[0, :] = 0 #every team starts the season (mw 0) with 0 league points, 0 goal difference, and 0 goals scored

goal_diff_df = league_scores_df.copy() #make another dataframe that will keep track of goal difference by week for each team. using .copy() unlinks the two dataframes
goals_scored_df = league_scores_df.copy() #make another dataframe that will keep track of goal difference by week for each team. using .copy() unlinks the two dataframes

league_positions_df = league_scores_df.copy() #make another dataframe that will keep track of league position by week for each team. using .copy() unlinks the two dataframes
league_positions_df.loc[0, :] = len(team_names_list)/2 #every team starts the season in the middle of the pack

################################################################################
##### fill in the values for three of the empty dataframes that will be used to calculate league position later #####
#NOTE: these are not cumulative values yet
for index, row in match_results_df.iterrows():
    #temporarily store the following data so that it only has to be accessed once
    mw = row['match week']
    htn = row['home team name']
    atn = row['away team name']
    hfs = row['home final score']
    afs = row['away final score']
    hgd = hfs-afs #goal difference for the home team
    #update the three dataframes you initiated above
    goals_scored_df.loc[ mw, htn ] = hfs
    goals_scored_df.loc[ mw, atn ] = afs
    goal_diff_df.loc[ mw, htn ] = hgd
    goal_diff_df.loc[ mw, atn ] = -hgd
    if hgd == 0: #both teams tied, so both get 1 league point
        league_scores_df.loc[ mw, htn ] = 1
        league_scores_df.loc[ mw, atn ] = 1
    elif hgd > 0: #home team won, so they get 3 league points while the away team gets 0
        league_scores_df.loc[ mw, htn ] = 3
        league_scores_df.loc[ mw, atn ] = 0
    else: #if the away team won, it got 3 league points
        league_scores_df.loc[ mw, htn ] = 0
        league_scores_df.loc[ mw, atn ] = 3

################################################################################
##### update each of the three dataframes so that each column has a running cumulative sum #####
league_scores_df = league_scores_df.cumsum()
goal_diff_df = goal_diff_df.cumsum()
goals_scored_df = goals_scored_df.cumsum()

################################################################################
##### determine the league position of each team for each match week based on league points, goal difference, then total goals scored #####
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

################################################################################
##### rearrange the columns of each dataframe so that the plot legends are sorted by final week values #####
orig_cols = league_scores_df.columns.tolist() #record the original columns

################################################################################
#define a function that rearranges the original columns of a dataframe based on the values in the last row
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

################################################################################
##### implement the column sorting function on the league scores, goal difference, and total goals scored dataframes #####
league_scores_df = sort_by_final_values( league_scores_df, team_names_list, orig_cols )
goal_diff_df = sort_by_final_values( goal_diff_df, team_names_list, orig_cols )
goals_scored_df = sort_by_final_values( goals_scored_df, team_names_list, orig_cols )

################################################################################
##### sort the columns of the league positions dataframe #####
final_league_positions = league_positions_df.loc[38].values.tolist()
cols_by_lp = []
for i in range(1, len(team_names_list)+1):
    new_lp_idx = final_league_positions.index(i)
    cols_by_lp.append( orig_cols[new_lp_idx] )
league_positions_df = league_positions_df[cols_by_lp]
#print(league_positions_df)

################################################################################
##### save these dataframes as csv files if you like #####
if save_created_data_frames:
    ls_csv_out_name = season_span + '_PL_league_score_data.csv'
    print( '  saving ' + ls_csv_out_name )
    league_scores_df.to_csv(out_path_dfs + ls_csv_out_name)

    gd_csv_out_name = season_span + '_PL_goal_difference_data.csv'
    print( '  saving ' + gd_csv_out_name )
    goal_diff_df.to_csv(out_path_dfs + gd_csv_out_name)

    gs_csv_out_name = season_span + '_PL_goals_scored_data.csv'
    print( '  saving ' + gs_csv_out_name )
    goals_scored_df.to_csv(out_path_dfs + gs_csv_out_name)

    lp_csv_out_name = season_span + '_PL_league_position_data.csv'
    print( '  saving ' + lp_csv_out_name )
    league_positions_df.to_csv(out_path_dfs + lp_csv_out_name)

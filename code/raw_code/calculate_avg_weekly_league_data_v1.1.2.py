################################################################################
#author: JER
#date of last modification: 201023
#summary of last modification: changed some hardcoded stuff so that it went through loops instead

################################################################################
##### description #####
#this script generates four dataframes, based on data from five consecutive EPL seasons
#   1) the mean and standard deviation of weekly league positions for teams grouped by their final league positions
#   2) the mean and standard deviation of weekly league scores for teams grouped by their final league positions
#   3) the mean and standard deviation of weekly goal difference for teams grouped by their final league positions
#   4) the mean and standard deviation of weekly total goals scored for teams grouped by their final league positions
#this script uses data files generated by 'calculate_league_points.py', so be sure to run that one first
#the data frames produced by this script are used by 'plot_avg_league_position_data.py'

################################################################################
##### import packages #####
import numpy as np
import pandas as pd

################################################################################
##### decide whether or not to save the data table that this script produces #####
save_created_data_frames = 0
out_path_dfs = '../../data/tidy_data/'

################################################################################
##### list the seasons that you want to evaluate #####
season_span_list = ['15_16', '16_17', '17_18', '18_19', '19_20']
season_span_prefix = season_span_list[0] + '_to_' + season_span_list[-1]
in_path = '../../data/tidy_data/'

################################################################################
##### import the data and store it in dataframes #####
league_positions_df_list = []
league_scores_df_list = []
goal_differences_df_list = []
goals_scored_df_list = []
for season in season_span_list:
    league_positions_df_list.append( pd.read_csv(in_path + season + '_PL_league_position_data.csv', index_col='match week') )
    league_scores_df_list.append( pd.read_csv(in_path + season + '_PL_league_score_data.csv', index_col='match week') )
    goal_differences_df_list.append( pd.read_csv(in_path + season + '_PL_goal_difference_data.csv', index_col='match week') )
    goals_scored_df_list.append( pd.read_csv(in_path + season + '_PL_goals_scored_data.csv', index_col='match week') )

################################################################################
##### reorder the data columns of each data frame so that they reflect final league position for a given season #####
#I already did this in 'plot_league_points.py' for the league positions dataframe, but I will redo it here just in case that script changes in the future
def sort_by_lp( league_positions_df, league_scores_df, goal_differences_df, goals_scored_df ):
    orig_cols = league_positions_df.columns.tolist()
    final_league_positions = league_positions_df.loc[38].values.tolist()
    cols_by_lp = []
    for i in range(1, 21):
        new_lp_idx = final_league_positions.index(i)
        cols_by_lp.append( orig_cols[new_lp_idx] )
    league_positions_df = league_positions_df[cols_by_lp]
    league_scores_df = league_scores_df[cols_by_lp]
    goal_differences_df = goal_differences_df[cols_by_lp]
    goals_scored_df = goals_scored_df[cols_by_lp]
    return( league_positions_df, league_scores_df, goal_differences_df, goals_scored_df )

season_idx = 0
while season_idx < len(season_span_list):
    [ league_positions_df_list[season_idx], league_scores_df_list[season_idx], goal_differences_df_list[season_idx], goals_scored_df_list[season_idx] ] = sort_by_lp( league_positions_df_list[season_idx], league_scores_df_list[season_idx], goal_differences_df_list[season_idx], goals_scored_df_list[season_idx] )
    season_idx += 1

################################################################################
##### change the column names so that they reflect final league position rather than the actual team name #####
league_pos_rank = list( range(1,21) ) #these will serve as the columns for each dataframe

for df in league_positions_df_list:
    df.columns = league_pos_rank

for df in league_scores_df_list:
    df.columns = league_pos_rank

for df in goal_differences_df_list:
    df.columns = league_pos_rank

for df in goals_scored_df_list:
    df.columns = league_pos_rank

################################################################################
##### append the dataframes from consecutive seasons, one below the other #####
league_positions_concat_df = pd.concat( (league_positions_df_list) )
league_scores_concat_df = pd.concat( (league_scores_df_list) )
goal_differences_concat_df = pd.concat( (goal_differences_df_list) )
goals_scored_concat_df = pd.concat( (goals_scored_df_list) )

################################################################################
##### calculate the mean and standard deviation for each final league position by match week based on the data from a group of seasons #####
league_positions_by_row_index = league_positions_concat_df.groupby(league_positions_concat_df.index) #group the concatenated dataframe by row index (match week)
league_positions_concat_df_means = league_positions_by_row_index.mean() #calculated the mean value of each column (final league position) at each grouped index (match week)
league_positions_concat_df_stds = league_positions_by_row_index.std(ddof=0) #ddof is 'delta degrees of freedom'. the default value is 1, which produces the sample std. we want the population std instead

league_scores_by_row_index = league_scores_concat_df.groupby(league_scores_concat_df.index) #group the concatenated dataframe by row index (match week)
league_scores_concat_df_means = league_scores_by_row_index.mean() #calculated the mean value of each column (final league position) at each grouped index (match week)
league_scores_concat_df_stds = league_scores_by_row_index.std(ddof=0) #ddof is 'delta degrees of freedom'. the default value is 1, which produces the sample std. we want the population std instead

goal_differences_by_row_index = goal_differences_concat_df.groupby(goal_differences_concat_df.index) #group the concatenated dataframe by row index (match week)
goal_differences_concat_df_means = goal_differences_by_row_index.mean() #calculated the mean value of each column (final league position) at each grouped index (match week)
goal_differences_concat_df_stds = goal_differences_by_row_index.std(ddof=0) #ddof is 'delta degrees of freedom'. the default value is 1, which produces the sample std. we want the population std instead

goals_scored_by_row_index = goals_scored_concat_df.groupby(goals_scored_concat_df.index) #group the concatenated dataframe by row index (match week)
goals_scored_concat_df_means = goals_scored_by_row_index.mean() #calculated the mean value of each column (final league position) at each grouped index (match week)
goals_scored_concat_df_stds = goals_scored_by_row_index.std(ddof=0) #ddof is 'delta degrees of freedom'. the default value is 1, which produces the sample std. we want the population std instead

################################################################################
##### save the dataframes containing means and standard deviations as csv files if you like #####
if save_created_data_frames:
    csv_out_name = season_span_prefix + '_PL_mean_league_position_data.csv'
    print( '  saving ' + csv_out_name )
    league_positions_concat_df_means.to_csv(out_path_dfs + csv_out_name)

    csv_out_name = season_span_prefix + '_PL_std_league_position_data.csv'
    print( '  saving ' + csv_out_name )
    league_positions_concat_df_stds.to_csv(out_path_dfs + csv_out_name)

    csv_out_name = season_span_prefix + '_PL_mean_league_score_data.csv'
    print( '  saving ' + csv_out_name )
    league_scores_concat_df_means.to_csv(out_path_dfs + csv_out_name)

    csv_out_name = season_span_prefix + '_PL_std_league_score_data.csv'
    print( '  saving ' + csv_out_name )
    league_scores_concat_df_stds.to_csv(out_path_dfs + csv_out_name)

    csv_out_name = season_span_prefix + '_PL_mean_goal_difference_data.csv'
    print( '  saving ' + csv_out_name )
    goal_differences_concat_df_means.to_csv(out_path_dfs + csv_out_name)

    csv_out_name = season_span_prefix + '_PL_std_goal_difference_data.csv'
    print( '  saving ' + csv_out_name )
    goal_differences_concat_df_stds.to_csv(out_path_dfs + csv_out_name)

    csv_out_name = season_span_prefix + '_PL_mean_goals_scored_data.csv'
    print( '  saving ' + csv_out_name )
    goals_scored_concat_df_means.to_csv(out_path_dfs + csv_out_name)

    csv_out_name = season_span_prefix + '_PL_std_goals_scored_data.csv'
    print( '  saving ' + csv_out_name )
    goals_scored_concat_df_stds.to_csv(out_path_dfs + csv_out_name)
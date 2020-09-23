################################################################################
#author: JER
#date of last modification: 201023
#summary of last modification: wrote initial program

################################################################################
##### description #####
#this script collects final week data from each team in a span of EPL seasons to look for correlations.
#a single dataframe is output, with the first column holding final league position data and each subsequent column containing a different paramter, such as:
#   1) final league position
#   2) final league points
#   3) final goal difference
#   4) final total number of goals scored
#   5) final total number of goals conceded

################################################################################
##### import packages #####
import pandas as pd

################################################################################
##### decide whether or not to save the dataframe that this script produces #####
save_created_data_frames = 0
out_path_dfs = '../../data/tidy_data/'

################################################################################
##### list the seasons that you want to evaluate #####
season_span_list = ['15_16', '16_17', '17_18', '18_19', '19_20']
season_span_prefix = season_span_list[0] + '_to_' + season_span_list[-1]
in_path = '../../data/tidy_data/'

################################################################################
##### list the parameters from the final week of each season that you wish to collect #####
data_columns_list = ['final_league_position', 'final_league_points', 'final_goal_difference', 'final_goals_scored', 'final_goals_conceded']

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
##### determine the row indexes to use for the final week values dataframe #####
row_idx_names = []
i = 0
while i < len(league_positions_df_list):
    team_names = league_positions_df_list[i].columns.tolist()
    team_season_names = [team + ' ' + season_span_list[i]  for team in team_names]
    row_idx_names += team_season_names
    i+=1
#print(len(row_idx_names))

################################################################################
##### initialize the dataframe containing final week values using the rows and columns you chose #####
final_week_values_df = pd.DataFrame( columns=data_columns_list, index=row_idx_names )
final_week_values_df.index.name = 'team_season'

################################################################################
##### fill in the values of the dataframe containing final week values using the data imported above #####
i = 0
while i < len(league_positions_df_list):
    curr_season_team_names_list = league_positions_df_list[i].columns.tolist()
    for team_name in curr_season_team_names_list: #update the row for each team for this season based on the data you imported earlier
        final_week_values_df.loc[team_name + ' ' + season_span_list[i], :] = [ league_positions_df_list[i].loc[38, team_name], league_scores_df_list[i].loc[38, team_name], goal_differences_df_list[i].loc[38, team_name], goals_scored_df_list[i].loc[38, team_name], goals_scored_df_list[i].loc[38, team_name] - goal_differences_df_list[i].loc[38, team_name] ]
    row_idx_names += team_season_names
    i+=1

################################################################################
##### save the dataframe containing final week values if you like #####
if save_created_data_frames:
    csv_out_name = season_span_prefix + '_final_week_data.csv'
    print('  saving ' + csv_out_name)
    final_week_values_df.to_csv(out_path_dfs + csv_out_name)

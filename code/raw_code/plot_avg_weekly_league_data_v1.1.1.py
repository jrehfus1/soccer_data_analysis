################################################################################
#author: JER
#date of last modification: 201022
#summary of last modification: added more informative comments

################################################################################
##### description #####
#this script generates four plots, based on data from five consecutive EPL seasons
#   1) line plot of average league position as a function of match week
#   2) line plot of average league score as a function of match week
#   3) line plot of average goal difference as a function of match week
#   4) line plot of total goals scored as a function of match week
#this script uses data files generated by 'calculate_avg_league_position_data.py', so be sure to run that one first

################################################################################
##### import packages #####
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

################################################################################
##### decide whether or not to save the figures that this script produces #####
save_figs = 0
out_path_figs = '../../figures/exploratory_figures/'

################################################################################
##### list the seasons that you want to evaluate #####
season_span_prefix = '15_16_to_19_20' #example: 15_16_to_19_20
in_path = '../../data/tidy_data/'

################################################################################
##### import the data and store it in dataframes #####
mean_league_positions_df = pd.read_csv( in_path + season_span_prefix + '_PL_mean_league_position_data.csv', index_col='match week' )
std_league_positions_df = pd.read_csv( in_path + season_span_prefix + '_PL_std_league_position_data.csv', index_col='match week' )

mean_league_scores_df = pd.read_csv( in_path + season_span_prefix + '_PL_mean_league_score_data.csv', index_col='match week' )
std_league_scores_df = pd.read_csv( in_path + season_span_prefix + '_PL_std_league_score_data.csv', index_col='match week' )

mean_goal_differences_df = pd.read_csv( in_path + season_span_prefix + '_PL_mean_goal_difference_data.csv', index_col='match week' )
std_goal_differences_df = pd.read_csv( in_path + season_span_prefix + '_PL_std_goal_difference_data.csv', index_col='match week' )

mean_goals_scored_df = pd.read_csv( in_path + season_span_prefix + '_PL_mean_goals_scored_data.csv', index_col='match week' )
std_goals_scored_df = pd.read_csv( in_path + season_span_prefix + '_PL_std_goals_scored_data.csv', index_col='match week' )

################################################################################
#make new dataframes that contain the mean + std and mean - std, respectively (useful for plotting later)
mean_league_positions_df_add_stds = mean_league_positions_df.add(std_league_positions_df)
mean_league_positions_df_subtract_stds = mean_league_positions_df.subtract(std_league_positions_df)

mean_league_scores_df_add_stds = mean_league_scores_df.add(std_league_scores_df)
mean_league_scores_df_subtract_stds = mean_league_scores_df.subtract(std_league_scores_df)

mean_goal_differences_df_add_stds = mean_goal_differences_df.add(std_goal_differences_df)
mean_goal_differences_df_subtract_stds = mean_goal_differences_df.subtract(std_goal_differences_df)

mean_goals_scored_df_add_stds = mean_goals_scored_df.add(std_goals_scored_df)
mean_goals_scored_df_subtract_stds = mean_goals_scored_df.subtract(std_goals_scored_df)

################################################################################
##### set up the color map that will be used to plot the weekly data color-coded by final league position #####
color_map = matplotlib.cm.get_cmap('viridis')
color_map_positions = list( range(0,21) ) #20 teams total
color_map_positions[:] = [x / 20 for x in color_map_positions] #normalize the color map positions so that they increment from 0 to 1 now

################################################################################
##### plot league positions data #####
fig_01 = plt.figure(figsize=(10, 5))
fig_01.suptitle('Five season average: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14])
grid_01 = plt.GridSpec(3, 3)
axes_01 = []
axes_01.append( fig_01.add_subplot(grid_01[:, :]) )
axes_01[0].set_title('league position throughout the seasaon')
axes_01[0].set_xlabel('match week', fontsize=14, color='black')
axes_01[0].set_ylabel('average league position by league position', fontsize=14, color='black')
axes_01[0].set_xlim(0, 38)
axes_01[0].set_ylim(21, 0)
axes_01[0].set_yticks(np.arange(1, 21, step=1))

cmp_idx = 0 #keep track of the color map index
for col in mean_league_positions_df.columns:
    if (cmp_idx % 2) ==0: #even number
        lp_plot = mean_league_positions_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(0.5,0.5,0.5), markeredgewidth=1, markersize=5, ax=axes_01[0])
    else: #odd number
        lp_plot = mean_league_positions_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(1.0,1.0,1.0), markeredgewidth=1, markersize=5, ax=axes_01[0])
    axes_01[0].fill_between(list( range(0,39) ), mean_league_positions_df_subtract_stds[col], mean_league_positions_df_add_stds[col], color=color_map(color_map_positions[cmp_idx]), alpha=0.2) #shade between the mean - std and the mean + std
    cmp_idx+=1
#set up the figure legend
box = axes_01[0].get_position()
axes_01[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_01[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

##### save this figure if you like #####
if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_weekly_league_position_by_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### plot league points data #####
fig_02 = plt.figure(figsize=(10, 5))
fig_02.suptitle('Five season average: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14])
grid_02 = plt.GridSpec(3, 3)
axes_02 = []
axes_02.append( fig_02.add_subplot(grid_02[:, :]) )
axes_02[0].set_title('when league points were won')
axes_02[0].set_xlabel('match week', fontsize=14, color='black')
axes_02[0].set_ylabel('average league points by league position', fontsize=14, color='black')
axes_02[0].set_xlim(0, 38)
axes_02[0].set_ylim(0, 114)

cmp_idx = 0 #keep track of the color map index
for col in mean_league_scores_df.columns:
    if (cmp_idx % 2) ==0: #even number
        ls_plot = mean_league_scores_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(0.5,0.5,0.5), markeredgewidth=1, markersize=5, ax=axes_02[0])
    else: #odd number
        ls_plot = mean_league_scores_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(1.0,1.0,1.0), markeredgewidth=1, markersize=5, ax=axes_02[0])
    axes_02[0].fill_between(list( range(0,39) ), mean_league_scores_df_subtract_stds[col], mean_league_scores_df_add_stds[col], color=color_map(color_map_positions[cmp_idx]), alpha=0.2) #shade between the mean - std and the mean + std
    cmp_idx+=1
#set up the figure legend
box = axes_02[0].get_position()
axes_02[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_02[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

##### save this figure if you like #####
if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_weekly_league_points_by_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### plot goal difference data #####
fig_03 = plt.figure(figsize=(10, 5))
fig_03.suptitle('Five season average: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14])
grid_03 = plt.GridSpec(3, 3)
axes_03 = []
axes_03.append( fig_03.add_subplot(grid_03[:, :]) )
axes_03[0].set_title('goal difference throughout the season')
axes_03[0].set_xlabel('match week', fontsize=14, color='black')
axes_03[0].set_ylabel('average goal difference by league position', fontsize=14, color='black')
axes_03[0].set_xlim(0, 38)
axes_03[0].set_ylim(-80, 80)

cmp_idx = 0 #keep track of the color map index
for col in mean_goal_differences_df.columns:
    #even positions are plotted in blue, odd in red
    if (cmp_idx % 2) ==0: #even number
        gd_plot = mean_goal_differences_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(0.5,0.5,0.5), markeredgewidth=1, markersize=5, ax=axes_03[0])
    else: #odd number
        gd_plot = mean_goal_differences_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(1.0,1.0,1.0), markeredgewidth=1, markersize=5, ax=axes_03[0])
    axes_03[0].fill_between(list( range(0,39) ), mean_goal_differences_df_subtract_stds[col], mean_goal_differences_df_add_stds[col], color=color_map(color_map_positions[cmp_idx]), alpha=0.2) #shade between the mean - std and the mean + std
    cmp_idx+=1
#set up the figure legend
box = axes_03[0].get_position()
axes_03[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_03[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

##### save this figure if you like #####
if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_weekly_goal_difference_by_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### plot total goals data #####
fig_04 = plt.figure(figsize=(10, 5))
fig_04.suptitle('Five season average: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14])
grid_04 = plt.GridSpec(3, 3)
axes_04 = []
axes_04.append( fig_04.add_subplot(grid_04[:, :]) )
axes_04[0].set_title('goals scored throughout the season')
axes_04[0].set_xlabel('match week', fontsize=14, color='black')
axes_04[0].set_ylabel('average total goals by league position', fontsize=14, color='black')
axes_04[0].set_xlim(0, 38)
axes_04[0].set_ylim(0, 120)

cmp_idx = 0 #keep track of the color map index
for col in mean_goals_scored_df.columns:
    if (cmp_idx % 2) == 0: #even number
        gs_plot = mean_goals_scored_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(0.5,0.5,0.5), markeredgewidth=1, markersize=5, ax=axes_04[0])
    else: #odd number
        gs_plot = mean_goals_scored_df.plot(y=col, use_index=True, color=color_map(color_map_positions[cmp_idx]), linewidth=2.0, marker='h', markerfacecolor=(1.0,1.0,1.0), markeredgewidth=1, markersize=5, ax=axes_04[0])
    axes_04[0].fill_between(list( range(0,39) ), mean_goals_scored_df_subtract_stds[col], mean_goals_scored_df_add_stds[col], color=color_map(color_map_positions[cmp_idx]), alpha=0.2) #shade between the mean - std and the mean + std
    cmp_idx+=1
#set up the figure legend
box = axes_04[0].get_position()
axes_04[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
axes_04[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

##### save this figure if you like #####
if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_weekly_goals_scored_by_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### show the plots #####
plt.show()

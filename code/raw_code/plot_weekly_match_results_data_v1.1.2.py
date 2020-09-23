################################################################################
#author: JER
#date of last modification: 201023
#summary of last modification: wrote initial program

################################################################################
##### description #####
#this code plots the following values for each premier league team as a function of week for a single season
#   1) weekly cumulative league points for each EPL team from a single season
#   2) weekly cumulative goal difference for each EPL team from a single season
#   3) weekly cumulative goals scored for each EPL team from a single season
#   4) weekly league position for each EPL team from a single season
#all four of these plots are created in separate figures and can be saved as output

################################################################################
##### list of scripts that must be run first #####
#   1) calculate_weekly_match_results.py
#       this script uses the output from the above script as input

################################################################################
##### import packages #####
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from team_colors import team_primary_color_dict as tpcd
from team_colors import team_secondary_color_dict as tscd

################################################################################
##### decide whether or not to save the figure that this script produces #####
save_figs = 0
out_path_figs = '../../figures/exploratory_figures/'

################################################################################
##### read in the data files containing the weekly data from the season of choice #####
season_span = input('\t=== Enter season span (eg. 19_20): ')
in_path = '../../data/tidy_data/'

league_scores_df = pd.read_csv(in_path + season_span + '_PL_league_score_data.csv', index_col='match week')
goal_diff_df = pd.read_csv(in_path + season_span + '_PL_goal_difference_data.csv', index_col='match week')
goals_scored_df = pd.read_csv(in_path + season_span + '_PL_goals_scored_data.csv', index_col='match week')
league_positions_df = pd.read_csv(in_path + season_span + '_PL_league_position_data.csv', index_col='match week')

################################################################################
##### plot the weekly league points data for each team for this season #####
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

################################################################################
##### plot the weekly goal difference data for each team for this season #####
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

################################################################################
##### plot the weekly total goals data for each team for this season #####
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

################################################################################
##### plot the weekly league position data for each team for this season #####
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

################################################################################
##### show the plots #####
plt.show()

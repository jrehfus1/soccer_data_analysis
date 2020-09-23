################################################################################
#author: JER
#date of last modification: 201023
#summary of last modification: wrote initial program

################################################################################
##### description #####
#this script will produce plots that can help with exploratory data analysis
#currently, five plots are produced in an effor to examine correlations between team performance metrics:
#   1) final league points vs final league position
#   2) final goal difference vs final league position
#   3) final total number of goals scored vs final league position
#   4) final total number of goals conceded vs final league position
#   5) final total number of goals scored vs final total number of goals conceded

################################################################################
##### import packages #####
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

################################################################################
##### decide whether or not to save the figures that this script produces #####
save_figs = 0
out_path_figs = '../../figures/exploratory_figures/'

################################################################################
##### list the seasons that you want to evaluate #####
season_span_prefix = '15_16_to_19_20' #example: 15_16_to_19_20
in_path = '../../data/tidy_data/'

################################################################################
##### import the data and store it in a dataframe #####
final_week_values_df = pd.read_csv(in_path + season_span_prefix + '_final_week_data.csv', index_col='team_season')

mean_league_scores_df = pd.read_csv( in_path + season_span_prefix + '_PL_mean_league_score_data.csv', index_col='match week' )
final_league_positions_list = mean_league_scores_df.columns.tolist()
final_league_positions_list = [int(pos) for pos in final_league_positions_list]
mean_final_league_scores_list = mean_league_scores_df.loc[38].values

################################################################################
##### plot final league points versus final league positions #####
fig_01 = plt.figure(figsize=(10, 5))
fig_01.suptitle( 'Five seasons worth of data: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14] )
grid_01 = plt.GridSpec(3, 3)
axes_01 = []
axes_01.append( fig_01.add_subplot(grid_01[:, :]) )
axes_01[0].set_title( 'final league points vs final league position' )
axes_01[0].set_xlabel( 'final league points', fontsize=14, color='black' )
axes_01[0].set_ylabel( 'final league position', fontsize=14, color='black' )
axes_01[0].set_xlim(0, 114)
axes_01[0].set_ylim(21, 0)
axes_01[0].set_yticks(np.arange(1, 21, step=1))

plt.plot(mean_final_league_scores_list, final_league_positions_list, color=(0.07,0.41,0.98), linewidth=1.0, marker='h', markerfacecolor=(0.07,0.41,0.98), markeredgewidth=1, markersize=3)
final_week_values_df.plot.scatter(x='final_league_points', y='final_league_position', marker='h', s=10, color=(0.37,0.73,0.49), ax=axes_01[0])

fig_01.tight_layout()

if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_final_league_points_vs_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### plot final goal difference versus final league positions #####
fig_02 = plt.figure(figsize=(10, 5))
fig_02.suptitle( 'Five seasons worth of data: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14] )
grid_02 = plt.GridSpec(3, 3)
axes_02 = []
axes_02.append( fig_02.add_subplot(grid_02[:, :]) )
axes_02[0].set_title( 'final goal difference vs final league position' )
axes_02[0].set_xlabel( 'final goal difference', fontsize=14, color='black' )
axes_02[0].set_ylabel( 'final league position', fontsize=14, color='black' )
axes_02[0].set_xlim(-80, 80)
axes_02[0].set_ylim(21, 0)
axes_02[0].set_yticks(np.arange(1, 21, step=1))

final_week_values_df.plot.scatter(x='final_goal_difference', y='final_league_position', marker='h', s=10, color=(0.37,0.73,0.49), ax=axes_02[0])

fig_02.tight_layout()

if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_final_goal_difference_vs_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### plot total goals scored versus final league positions #####
fig_03 = plt.figure(figsize=(10, 5))
fig_03.suptitle( 'Five seasons worth of data: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14] )
grid_03 = plt.GridSpec(3, 3)
axes_03 = []
axes_03.append( fig_03.add_subplot(grid_03[:, :]) )
axes_03[0].set_title( 'total goals scored vs final league position' )
axes_03[0].set_xlabel( 'total goals scored', fontsize=14, color='black' )
axes_03[0].set_ylabel( 'final league position', fontsize=14, color='black' )
axes_03[0].set_xlim(0, 120)
axes_03[0].set_ylim(21, 0)
axes_03[0].set_yticks(np.arange(1, 21, step=1))

final_week_values_df.plot.scatter(x='final_goals_scored', y='final_league_position', marker='h', s=10, color=(0.37,0.73,0.49), ax=axes_03[0])

fig_03.tight_layout()

if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_final_goals_scored_vs_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### plot total goals conceded versus final league positions #####
fig_04 = plt.figure(figsize=(10, 5))
fig_04.suptitle( 'Five seasons worth of data: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14] )
grid_04 = plt.GridSpec(3, 3)
axes_04 = []
axes_04.append( fig_04.add_subplot(grid_04[:, :]) )
axes_04[0].set_title( 'total goals conceded vs final league position' )
axes_04[0].set_xlabel( 'total goals conceded', fontsize=14, color='black' )
axes_04[0].set_ylabel( 'final league position', fontsize=14, color='black' )
axes_04[0].set_xlim(0, 120)
axes_04[0].set_ylim(21, 0)
axes_04[0].set_yticks(np.arange(1, 21, step=1))

final_week_values_df.plot.scatter(x='final_goals_conceded', y='final_league_position', marker='h', s=10, color=(0.37,0.73,0.49), ax=axes_04[0])

fig_04.tight_layout()

if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_final_goals_conceded_vs_final_league_position.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True )

################################################################################
##### plot total goals scored versus total goals conceded data #####
fig_05 = plt.figure(figsize=(5, 5))
fig_05.suptitle( 'Five seasons worth of data: ' + season_span_prefix[0:5] + ' to ' + season_span_prefix[8:14] )
grid_05 = plt.GridSpec(3, 3)
axes_05 = []
axes_05.append( fig_05.add_subplot(grid_05[:, :]) )
axes_05[0].set_title( 'total goals scored vs total goals conceded' )
axes_05[0].set_xlabel( 'total goals scored', fontsize=14, color='black' )
axes_05[0].set_ylabel( 'total goals conceded', fontsize=14, color='black' )
axes_05[0].set_xlim(0, 120)
axes_05[0].set_ylim(0, 120)

final_week_values_df.plot.scatter(x='final_goals_scored', y='final_goals_conceded', marker='h', s=10, color=(0.37,0.73,0.49), ax=axes_05[0])

fig_05.tight_layout()

if save_figs: #save the figure if you like
    fig_out_name = season_span_prefix + '_final_goals_scored_vs_final_goals_conceded.pdf'
    print( '  saving ' + fig_out_name )
    plt.savefig( out_path_figs + fig_out_name, dpi=150, format=None, transparent=True)

################################################################################
##### show the plots #####
plt.show()

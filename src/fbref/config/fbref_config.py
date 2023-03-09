CURRENT_SEASON = "2022-2023"

LEAGUE_TABLE_RENAME_COL_DICT = {
    "rk": "position",
    "squad": "team",
    "mp": "matches_played",
    "w": "wins",
    "d": "draws",
    "l": "losses",
    "gf": "goals_for",
    "ga": "goals_against",
    "gd": "goal_difference",
    "pts": "points",
    "pts_per_mp": "points_per_match",
    "xg": "xg",
    "xga": "xg_against",
    "xgd": "expected_goal_difference",
    "xgd_per_90": "expected_goal_difference_per_90",
    "gls_per_game": "goals_per_game",
    "gls_conceded_per_game": "gls_conceded_per_game",
    "xg_per_game": "xg_per_game",
    "xga_per_game": "xg_against_per_game",
}

PLAYER_STANDARD_RENAME_COL_DICT = {
    "Rk": "rank",
    "Player": "player_name",
    "Nation": "country",
    "Pos": "position",
    "Squad": "team",
    "Comp": "competition",
    "Age": "age",
    "Born": "born",
    "Playing Time MP": "matches_played",
    "Playing Time Starts": "starts",
    "Playing Time Min": "minutes",
    "Playing Time 90s": "no_of_nineties",
    "Performance Gls": "goals",
    "Performance Ast": "assists",
    "Performance G-PK": "goals_minus_pk",
    "Performance PK": "penalties",
    "Performance PKatt": "penalty_attempted",
    "Performance CrdY": "yellows",
    "Performance CrdR": "reds",
    "Per 90 Minutes Gls": "goals_per_90",
    "Per 90 Minutes Ast": "assists_per_90",
    "Per 90 Minutes G+A": "goals_plus_assists_per_90",
    "Per 90 Minutes G-PK": "goals_minus_pens_per_90",
    "Per 90 Minutes G+A-PK": "goals_plus_assists_minus_pens_per_90",
    "Expected xG": "xg",
    "Expected npxG": "non_penalty_xg",
    "Expected xAG": "expected_assisted_goals",
    "Expected npxG+xAG": "non_penalty_xg_plus_expected_assists",
    "Per 90 Minutes xG": "xg_per_90",
    "Per 90 Minutes xAG": "expected_assists_per_90",
    "Per 90 Minutes xG+xAG": "xg_plus_expected_assists_per_90",
    "Per 90 Minutes npxG": "non_penalty_xg_per_90",
    "Per 90 Minutes npxG+xAG": "non_penalty_xg_plus_expected_assists_per_90",
    "Matches": "matches",
}

PLAYER_STANDARD_FLOAT_COLUMNS = [
    "age",
    "born",
    "matches_played",
    "starts",
    "minutes",
    "no_of_nineties",
    "goals",
    "assists",
    "goals_minus_pk",
    "penalties",
    "penalty_attempted",
    "yellows",
    "reds",
    "goals_per_90",
    "assists_per_90",
    "goals_plus_assists_per_90",
    "goals_minus_pens_per_90",
    "goals_plus_assists_minus_pens_per_90",
    "xg",
    "non_penalty_xg",
    "expected_assisted_goals",
    "non_penalty_xg_plus_expected_assists",
    "xg_per_90",
    "expected_assists_per_90",
    "xg_plus_expected_assists_per_90",
    "non_penalty_xg_per_90",
    "non_penalty_xg_plus_expected_assists_per_90",
]

TEAM_DEFENSE_RENAME_COL_DICT = {
    "squad": "team",
    "no_pl": "no_players_used",
    "90s": "no_of_nineties",
    "tackles_tkl_per_match": "tackles_per_match",
    "tackles_tklw_per_match": "tackles_won_per_match",
    "tackles_def_3rd_per_match": "tackles_def_3rd_per_match",
    "tackles_mid_3rd_per_match": "tackles_mid_3rd_per_match",
    "tackles_att_3rd_per_match": "tackles_att_3rd_per_match",
    "vs_dribbles_tkl_per_match": "successful_tackles_on_dribblers_per_match",
    "vs_dribbles_att_per_match": "attempted_tackles_on_dribblers_per_match",
    "vs_dribbles_past_per_match": "unsuccessful_tackles_on_dribblers_per_match",
    "blocks_blocks_per_match": "total_blocks_per_match",
    "blocks_sh_per_match": "shots_blocked_per_match",
    "blocks_pass_per_match": "passes_blocked_per_match",
    "int_per_match": "interceptions_per_match",
    "tkl_plus_int_per_match": "tackles_plus_interceptions_per_match",
    "clr_per_match": "clearances_per_match",
    "err_per_match": "errors_per_match",
}

PLAYER_DEFENSE_RENAME_COL_DICT = {
    "Rk": "Rk",
    "Player": "player_name",
    "Nation": "country",
    "Pos": "position",
    "Squad": "team",
    "Comp": "competition",
    "Age": "age",
    "Born": "born",
    "90s": "no_of_nineties",
    "Tackles Tkl": "tackles",
    "Tackles TklW": "total_tackles_won",
    "Tackles Def 3rd": "tackles_def_3rd",
    "Tackles Mid 3rd": "tackles_mid_3rd",
    "Tackles Att 3rd": "tackles_att_3rd",
    "Vs Dribbles Tkl": "successful_tackles_on_dribblers",
    "Vs Dribbles Att": "attempted_tackles_on_dribblers",
    "Vs Dribbles Tkl%": "tackles_success_rate_on_dribblers_percentage",
    "Vs Dribbles Past": "unsuccessful_tackles_on_dribblers",
    "Blocks Blocks": "blocks",
    "Blocks Sh": "shots_blocked",
    "Blocks Pass": "passes_blocked",
    "Int": "interceptions",
    "Tkl+Int": "tackles_plus_interceptions",
    "Clr": "clearances",
    "Err": "errors",
    "Matches": "matches",
}

PLAYER_DEFENSE_FLOAT_COLUMNS = [
    "no_of_nineties",
    "tackles_success_rate_on_dribblers_percentage",
    "Rk",
    "born",
    "tackles",
    "total_tackles_won",
    "tackles_def_3rd",
    "tackles_mid_3rd",
    "tackles_att_3rd",
    "successful_tackles_on_dribblers",
    "attempted_tackles_on_dribblers",
    "unsuccessful_tackles_on_dribblers",
    "blocks",
    "shots_blocked",
    "passes_blocked",
    "interceptions",
    "tackles_plus_interceptions",
    "clearances",
    "errors",
]

PLAYER_DEFENSE_TOTAL_COUNT_COLUMNS = [
    "tackles",
    "total_tackles_won",
    "tackles_def_3rd",
    "tackles_mid_3rd",
    "tackles_att_3rd",
    "successful_tackles_on_dribblers",
    "attempted_tackles_on_dribblers",
    "unsuccessful_tackles_on_dribblers",
    "blocks",
    "shots_blocked",
    "passes_blocked",
    "interceptions",
    "tackles_plus_interceptions",
    "clearances",
    "errors",
]

PLAYER_POSSESSION_RENAME_COL_DICT = {
    "Rk": "rank",
    "Player": "player_name",
    "Nation": "country",
    "Pos": "position",
    "Squad": "team",
    "Comp": "competition",
    "Age": "age",
    "Born": "born",
    "90s": "no_of_nineties",
    "Touches Touches": "touches",
    "Touches Def Pen": "touches_defensive_penalty_area",
    "Touches Def 3rd": "touches_defensive_third",
    "Touches Mid 3rd": "touches_middle_third",
    "Touches Att 3rd": "touches_attacking_third",
    "Touches Att Pen": "touches_attacking_penalty_area",
    "Touches Live": "live_touches",
    "Dribbles Succ": "successful_dribbles",
    "Dribbles Att": "attempted_dribbles",
    "Dribbles Succ%": "dribble_success_perc",
    "Dribbles Mis": "miscontrolled",
    "Dribbles Dis": "dispossessed",
    "Receiving Rec": "passes_received",
    "Receiving Prog": "progressive_passes_received",
    "Matches": "matches",
}

PLAYER_POSSESSION_FLOAT_COLUMNS = [
    "age",
    "born",
    "no_of_nineties",
    "touches",
    "touches_defensive_penalty_area",
    "touches_defensive_third",
    "touches_middle_third",
    "touches_attacking_third",
    "touches_attacking_penalty_area",
    "live_touches",
    "successful_dribbles",
    "attempted_dribbles",
    "dribble_success_perc",
    "miscontrolled",
    "dispossessed",
    "passes_received",
    "progressive_passes_received",
]

PLAYER_POSSESSION_TOTAL_COUNT_COLUMNS = [
    "touches",
    "touches_defensive_penalty_area",
    "touches_defensive_third",
    "touches_middle_third",
    "touches_attacking_third",
    "touches_attacking_penalty_area",
    "live_touches",
    "successful_dribbles",
    "attempted_dribbles",
    "miscontrolled",
    "dispossessed",
    "passes_received",
    "progressive_passes_received",
]

TEAM_POSSESSION_RENAME_COL_DICT = {
    "Squad": "team",
    "# Pl": "no_players_used",
    "Poss": "possession",
    "90s": "no_of_nineties",
    "Touches Touches": "touches",
    "Touches Def Pen": "touches_in_defensive_penalty_area",
    "Touches Def 3rd": "touches_in_defensive_third",
    "Touches Mid 3rd": "touches_in_midfield_third",
    "Touches Att 3rd": "touches_in_attacking_third",
    "Touches Att Pen": "touches_in_attacking_penalty_area",
    "Touches Live": "live_ball_touches",
    "Dribbles Succ": "successful_dribbles",
    "Dribbles Att": "attempted_dribbles",
    "Dribbles Succ%": "dribbles_success_rate",
    "Dribbles Mis": "no_miscontrol",
    "Dribbles Dis": "no_dispossessed",
    "Receiving Rec": "passes_recieved",
    "Receiving Prog": "progressive_passess_recieved",
}

PLAYER_PASSING_RENAME_COL_DICT = {
    "Rk": "rank",
    "Player": "player_name",
    "Nation": "country",
    "Pos": "position",
    "Squad": "team",
    "Comp": "competition",
    "Age": "age",
    "Born": "born",
    "90s": "no_of_nineties",
    "Total Cmp": "passes_completes",
    "Total Att": "passes_attempted",
    "Total Cmp%": "pass_completion_perc",
    "Total TotDist": "passes_total_distance",
    "Total PrgDist": "passes_progressive_distance",
    "Short Cmp": "short_completed_passes",
    "Short Att": "short_attempted_passes",
    "Short Cmp%": "short_pass_completion_perc",
    "Medium Cmp": "medium_completed_passes",
    "Medium Att": "medium_attempted_passes",
    "Medium Cmp%": "medium_pass_completion_perc",
    "Long Cmp": "long_passes_completed",
    "Long Att": "long_passes_attempted",
    "Long Cmp%": "long_pass_completion_perc",
    "Ast": "assists",
    "xAG": "expected_assisted_goals",
    "xA": "expected_assists",
    "A-xAG": "assists_minus_expected_assisted_goals",
    "KP": "key_passes",
    "1/3": "passes_into_final_third",
    "PPA": "passes_into_18_yard_box",
    "CrsPA": "completed_passes_into_18_yard_box",
    "Prog": "progressive_passes",
    "Matches": "matches",
}

PLAYER_PASSING_FLOAT_COLUMNS = [
    "age",
    "born",
    "no_of_nineties",
    "passes_completes",
    "passes_attempted",
    "pass_completion_perc",
    "passes_total_distance",
    "passes_progressive_distance",
    "short_completed_passes",
    "short_attempted_passes",
    "short_pass_completion_perc",
    "medium_completed_passes",
    "medium_attempted_passes",
    "medium_pass_completion_perc",
    "long_passes_completed",
    "long_passes_attempted",
    "long_pass_completion_perc",
    "assists",
    "expected_assisted_goals",
    "expected_assists",
    "assists_minus_expected_assisted_goals",
    "key_passes",
    "passes_into_final_third",
    "passes_into_18_yard_box",
    "completed_passes_into_18_yard_box",
    "progressive_passes",
]

PLAYER_PASSING_TOTAL_COUNT_COLUMNS = [
    "passes_completes",
    "passes_attempted",
    "passes_total_distance",
    "passes_progressive_distance",
    "short_completed_passes",
    "short_attempted_passes",
    "medium_completed_passes",
    "medium_attempted_passes",
    "long_passes_completed",
    "long_passes_attempted",
    "assists",
    "expected_assisted_goals",
    "expected_assists",
    "assists_minus_expected_assisted_goals",
    "key_passes",
    "passes_into_final_third",
    "passes_into_18_yard_box",
    "completed_passes_into_18_yard_box",
    "progressive_passes",
]

PLAYER_SHOOTING_RENAME_COL_DICT = {
    "Rk": "rank",
    "Player": "player_name",
    "Nation": "country",
    "Pos": "position",
    "Squad": "team",
    "Comp": "competition",
    "Age": "age",
    "Born": "born",
    "90s": "no_of_nineties",
    "Standard Gls": "goals",
    "Standard Sh": "shots",
    "Standard SoT": "shots_on_target",
    "Standard SoT%": "shots_on_target_perc",
    "Standard Sh/90": "shots_per_90",
    "Standard SoT/90": "shots_on_target_per_90",
    "Standard G/Sh": "goals_per_shot",
    "Standard G/SoT": "goals_per_shot_on_target",
    "Standard Dist": "average_shot_distance_from_goal",
    "Standard FK": "shots_free_kicks",
    "Standard PK": "shots_penalty_made",
    "Standard PKatt": "shots_penalties_attempted",
    "Expected xG": "xg",
    "Expected npxG": "non_penalty_xg",
    "Expected npxG/Sh": "non_penalty_xg_per_shot",
    "Expected G-xG": "goals_minus_xg",
    "Expected np:G-xG": "non_penalty_goals_minus_non_penalty_xg",
    "Matches": "matches",
}

PLAYER_SHOOTING_FLOAT_COLUMNS = [
    "age",
    "born",
    "no_of_nineties",
    "goals",
    "shots",
    "shots_on_target",
    "shots_on_target_perc",
    "shots_per_90",
    "shots_on_target_per_90",
    "goals_per_shot",
    "goals_per_shot_on_target",
    "average_shot_distance_from_goal",
    "shots_free_kicks",
    "shots_penalty_made",
    "shots_penalties_attempted",
    "xg",
    "non_penalty_xg",
    "non_penalty_xg_per_shot",
    "goals_minus_xg",
    "non_penalty_goals_minus_non_penalty_xg",
]

PLAYER_SHOOTING_TOTAL_COUNT_COLUMNS = [
    "goals",
    "shots",
    "shots_on_target",
    "goals_per_shot",
    "goals_per_shot_on_target",
    "shots_free_kicks",
    "shots_penalty_made",
    "shots_penalties_attempted",
    "xg",
    "non_penalty_xg",
    "goals_minus_xg",
    "non_penalty_goals_minus_non_penalty_xg",
]

PLAYER_MISCELLANEOUS_RENAME_COL_DICT = {
    "Rk": "rank",
    "Player": "player_name",
    "Nation": "country",
    "Pos": "position",
    "Squad": "team",
    "Comp": "competition",
    "Age": "age",
    "Born": "born",
    "90s": "no_of_nineties",
    "Performance CrdY": "yellow_cards",
    "Performance CrdR": "red_cards",
    "Performance 2CrdY": "two_yellows",
    "Performance Fls": "fouls",
    "Performance Fld": "fouls_drawn",
    "Performance Off": "offsides",
    "Performance Crs": "crosses",
    "Performance Int": "interceptions",
    "Performance TklW": "tackles_won",
    "Performance PKwon": "penalties_won",
    "Performance PKcon": "penalties_conceded",
    "Performance OG": "own_goals",
    "Performance Recov": "loose_balls_recovered",
    "Aerial Duels Won": "aerial_duels_won",
    "Aerial Duels Lost": "aerial_duels_lost",
    "Aerial Duels Won%": "aerial_duels_win_perc",
    "Matches": "matches",
}

PLAYER_MISCELLANEOUS_FLOAT_COLUMNS = [
    "age",
    "born",
    "no_of_nineties",
    "yellow_cards",
    "red_cards",
    "two_yellows",
    "fouls",
    "fouls_drawn",
    "offsides",
    "crosses",
    "interceptions",
    "tackles_won",
    "penalties_won",
    "penalties_conceded",
    "own_goals",
    "loose_balls_recovered",
    "aerial_duels_won",
    "aerial_duels_lost",
    "aerial_duels_win_perc",
]

PLAYER_MISCELLANEOUS_TOTAL_COUNT_COLUMNS = [
    "yellow_cards",
    "red_cards",
    "two_yellows",
    "fouls",
    "fouls_drawn",
    "offsides",
    "crosses",
    "interceptions",
    "tackles_won",
    "penalties_won",
    "penalties_conceded",
    "own_goals",
    "loose_balls_recovered",
    "aerial_duels_won",
    "aerial_duels_lost",
]

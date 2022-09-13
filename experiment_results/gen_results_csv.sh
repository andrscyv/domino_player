#!/bin/zsh
db_file_path=$1
target_folder_path=$2
my_path=${0:a:h}

echo 'Searching for db in ... ' $db_file_path
echo 'Target folder: ' $target_folder_path
echo 'Searching for sql files in ...' $my_path

sqlite3 -header -csv $db_file_path < $my_path/grid_search_vs_greedy.sql > $target_folder_path/grid_search_vs_greedy.csv
sqlite3 -header -csv $db_file_path < $my_path/grid_search_vs_strong.sql > $target_folder_path/grid_search_vs_strong.csv
sqlite3 -header -csv $db_file_path < $my_path/mcts_is_correct.sql > $target_folder_path/mcts_is_correct.csv
sqlite3 -header -csv $db_file_path < $my_path/mcts_saturation.sql > $target_folder_path/mcts_saturation.csv
sqlite3 -header -csv $db_file_path < $my_path/pimc_min_performance.sql > $target_folder_path/pimc_min_performance.csv
sqlite3 -header -csv $db_file_path < $my_path/mix_teams_vs_strong_team.sql > $target_folder_path/mix_teams_vs_strong_team.csv
sqlite3 -header -csv $db_file_path < $my_path/mix_teams_vs_weak_team.sql > $target_folder_path/mix_teams_vs_weak_team.csv
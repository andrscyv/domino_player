-- Percentage of wins team_1
select 
	e.experiment_id,
	e.p1 as team_1_p1,
	e.p3 as team_1_p3,
	e.p2 as team_2_p2,
	e.p4 as team_2_p4,
	e.num_games,
	(count(distinct g.game_id)*1.0/e.num_games)*100 as percent_wins_team_1
from game g
inner join experiment e on e.experiment_id = g.experiment_id
where g.winner = 1
group by g.experiment_id 

-- Aggregate by plays
select 
	e.experiment_id ,
	e.p1 as team_1_p1,
	e.p3 as team_1_p3,
	e.p2 as team_2_p2,
	e.p4 as team_2_p4,
	count(*) as total_plays,
	sum(case when p.player_number % 2 != 0 then 1 else 0 end)*1.0/e.num_games  as avg_team_1_num_plays,
	sum(case when p.player_number % 2 = 0 then 1 else 0 end)*1.0/e.num_games  as avg_team_2_num_plays,
	sum(case when (p.player_number % 2 != 0 and p.suit_played IS NULL )then 1 else 0 end)*1.0/e.num_games  as avg_team_1_num_pass,
	sum(case when (p.player_number % 2 = 0 and p.suit_played IS NULL )then 1 else 0 end)*1.0/e.num_games  as avg_team_2_num_pass,
	sum(case when p.play_number = 0 and g.winner == 1 
		then 1 else 0 end)*100.0/e.num_games  as percent_win_team_1,
	sum(case when p.play_number = 0 and g.winner == -1 
		then 1 else 0 end)*100.0/e.num_games  as percent_win_team_2,
	sum(case when p.play_number = 0 and g.winner == 0 
		then 1 else 0 end)*100.0/e.num_games  as percent_draws,
	sum(case when (p.p1_tiles = '[]' or p.p2_tiles = '[]' or p.p3_tiles = '[]'  or p.p4_tiles = '[]' ) and g.winner == 1 
		then 1 else 0 end)*100.0/e.num_games  as percent_win_not_hanged_team_1,
	sum(case when (p.p1_tiles = '[]' or p.p2_tiles = '[]' or p.p3_tiles = '[]'  or p.p4_tiles = '[]' ) and g.winner == -1 
		then 1 else 0 end)*100.0/e.num_games  as percent_win_not_hanged_team_2,
	sum(
		case when p.player_number % 2 != 0 then p.seconds_elapsed  else 0 end
		)*1.0/sum(case when p.player_number % 2 != 0 then 1 else 0 end)  as avg_team_1_seconds_elapsed,
	sum(
		case when p.player_number % 2 = 0 then p.seconds_elapsed  else 0 end
		)*1.0/sum(case when p.player_number % 2 = 0 then 1 else 0 end)  as avg_team_2_seconds_elapsed
from play p 
inner join game g on g.game_id = p.game_id 
inner join experiment e on e.experiment_id = g.experiment_id 
group by e.experiment_id 
-- Percentage of wins team_1
select 
	e.experiment_id,
	e.p1 as team_1,
	e.p2 as team_2,
	e.num_games,
	(count(distinct g.game_id)*1.0/e.num_games)*100 as percent_wins_team_1
from game g
inner join experiment e on e.experiment_id = g.experiment_id
where g.winner = 1
group by g.experiment_id 

-- Aggregate by plays
select 
	e.experiment_id ,
	e.p1 as team_1,
	e.p2 as team_2,
	count(*),
	sum(case when p.player_number % 2 != 0 then 1 else 0 end)*1.0/e.num_games  as avg_team_1_num_plays,
	sum(case when p.player_number % 2 = 0 then 1 else 0 end)*1.0/e.num_games  as avg_team_2_num_plays,
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


-- Data graph grid search PIMC vs Greedy
select 
	e.p1 as algo,
	(count(distinct g.game_id)*1.0/e.num_games)*100 as percent_wins_algo,
	CAST(replace(e.p1, rtrim(e.p1, replace(e.p1, '_', '')), '') as INTEGER) as pimc_num_simulations
from game g
inner join experiment e on e.experiment_id = g.experiment_id
where g.winner = 1 and g.experiment_id >= 66 and g.experiment_id <= 85
group by g.experiment_id 
UNION 
select 
	e.p1 as algo,
	(count(distinct g.game_id)*1.0/e.num_games)*100 as percent_wins_algo,
	CAST(replace(e.p1, rtrim(e.p1, replace(e.p1, '_', '')), '') as INTEGER) as pimc_num_simulations
from game g
inner join experiment e on e.experiment_id = g.experiment_id
where g.winner = 1 and g.experiment_id >= 1 and g.experiment_id <= 20
group by g.experiment_id 
order by pimc_num_simulations

-- Data graph grid search PIMC vs Strong player
select 
	e.p1 as algo,
	(count(distinct g.game_id)*1.0/e.num_games)*100 as percent_wins_algo,
	CAST(replace(e.p1, rtrim(e.p1, replace(e.p1, '_', '')), '') as INTEGER) as pimc_num_simulations
from game g
inner join experiment e on e.experiment_id = g.experiment_id
where g.winner = 1 and g.experiment_id >= 87 and g.experiment_id <= 106
group by g.experiment_id 
UNION 
select 
	e.p1 as algo,
	(count(distinct g.game_id)*1.0/e.num_games)*100 as percent_wins_algo,
	CAST(replace(e.p1, rtrim(e.p1, replace(e.p1, '_', '')), '') as INTEGER) as pimc_num_simulations
from game g
inner join experiment e on e.experiment_id = g.experiment_id
where g.winner = 1 and g.experiment_id >= 21 and g.experiment_id <= 40
group by g.experiment_id 
order by pimc_num_simulations


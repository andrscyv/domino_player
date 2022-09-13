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
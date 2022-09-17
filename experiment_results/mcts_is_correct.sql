-- Data graph MCTS is correct (mcts vs greedy)
select 
	e.p1 as algo,
	(count(distinct g.game_id)*1.0/e.num_games)*100 as percent_wins_algo,
	CAST(replace(e.p1, rtrim(e.p1, replace(e.p1, '_', '')), '') as REAL) as mcts_time_budget
from game g
inner join experiment e on e.experiment_id = g.experiment_id
where g.winner = 1
and g.experiment_id IN (
	156,
	157,
	158,
	159,
	160,
	161,
	162,
	163,
	164,
	165,
	166,
	167,
	168,
	169,
	170,
	171,
	172,
	173,
	174,
	198
)
group by g.experiment_id 
order by mcts_time_budget
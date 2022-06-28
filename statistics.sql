select COUNT(*) from game g

select AVG(s.first_player) from simulation s  

select p.simulation_id , count(*) from play p 
where p.pip1 = -1 or p.pip2 = -1
GROUP BY p.simulation_id 

select count(*)/COUNT(DISTINCT p.simulation_id)  from play p 
where p.pip1 = -1 or p.pip2 = -1 


select p.simulation_id , COUNT(*)/ from play p
GROUP BY p.simulation_id 

select g.experiment_id , count(*) as percent_wins, e.p1, e.p2 from game g
inner join experiment e on e.experiment_id = g.experiment_id 
where g.winner = 1
group by g.experiment_id 

select g.experiment_id , count(*) as num_games, e.p1, e.p2 from game g
inner join experiment e on e.experiment_id = g.experiment_id 
group by g.experiment_id 


select g.experiment_id , count(*) as num_games, e.p1, e.p2 from game g
inner join experiment e on e.experiment_id = g.experiment_id 
group by g.experiment_id 

select g.experiment_id, AVG(aux.game_length), e.p1, e.p2 from ( 
select p.game_id , count(*) as game_length from play p 
group by p.game_id 
) as aux
inner join game g on g.game_id  =  aux.game_id
inner join experiment e on g.experiment_id = e.experiment_id 
group by g.experiment_id 

select count(*) from game where experiment_id  = 1
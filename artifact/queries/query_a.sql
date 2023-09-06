SELECT @curRank :=  @curRank +1 AS position, D.team_name, D.matches_played, D.won, D.draw, D.lost, D.goals_scored, D.goals_conceced, D.points FROM (
SELECT team_name, count(team_name) as matches_played, sum(victory) as won, sum(draw) as draw, sum(defeat) as lost, sum(pro_goals) as goals_scored, sum(con_goals) as goals_conceced,
(3*sum(victory) + sum(draw)) as points, sum(pro_goals) - sum(con_goals) as goals_difference FROM

(SELECT 
	match_hometeam_name as team_name, 
	match_hometeam_score as pro_goals, 
	match_awayteam_score as con_goals, 
	if(match_hometeam_score>match_awayteam_score,1,0) as victory, 
	if(match_hometeam_score<match_awayteam_score,1,0) as defeat , 
	if(match_hometeam_score=match_awayteam_score,1,0) as draw 
FROM MATCHES AS A
UNION ALL
SELECT 
	match_awayteam_name as team_name, 
	match_awayteam_score as pro_goals, 
	match_awayteam_score as con_goals, 
	if(match_hometeam_score<match_awayteam_score,1,0) as victory, 
	if(match_hometeam_score>match_awayteam_score,1,0) as defeat , 
	if(match_hometeam_score=match_awayteam_score,1,0) as draw 
FROM MATCHES AS B) as C
GROUP BY team_name
ORDER BY points DESC, goals_difference DESC, goals_scored DESC, goals_conceced ASC, won DESC) as D, (SELECT @curRank := 0) as r;
WITH 
	MATCHES_BY_TEAM AS (
		SELECT 
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
		FROM MATCHES AS B
	),

	AGGREGATED_DATA_BY_TEAM AS (
		SELECT 
			team_name, 
			count(team_name) as matches_played, 
			sum(victory) as won, 
			sum(draw) as draw, 
			sum(defeat) as lost, 
			sum(pro_goals) as goals_scored, 
			sum(con_goals) as goals_conceced,
			(3*sum(victory) + sum(draw)) as points, 
			sum(pro_goals) - sum(con_goals) as goals_difference 
		FROM MATCHES_BY_TEAM
		GROUP BY team_name
		ORDER BY 
			points DESC, 
			goals_difference DESC, 
			goals_scored DESC, 
			goals_conceced ASC, 
			won DESC
	)
		
		
SELECT 
	@curRank :=  @curRank +1 AS position, 
	team_name, 
	matches_played, 
	won, 
	draw, 
	lost, 
	goals_scored, 
	goals_conceced, 
	points 
FROM AGGREGATED_DATA_BY_TEAM, (SELECT @curRank := 0) as r;

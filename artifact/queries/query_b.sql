SELECT 
	match_awayteam_name as team_name, 
	sum(match_awayteam_score) as goals
	FROM MATCHES
GROUP BY team_name
ORDER BY goals DESC, team_name ASC;
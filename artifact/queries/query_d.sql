WITH 
	SCORERS AS ( 
		SELECT
			match_id,
			home_scorer as scorer,
			"home" as home_away
		FROM GOALSCORER
		UNION ALL
		SELECT
			match_id,
			away_scorer as scorer,
			"away" as home_away
		FROM GOALSCORER
	),

 	MATCH_TEAMS as (
		SELECT 
			match_id, 
			match_round, 
			match_hometeam_name as home_team, 
			match_awayteam_name as away_team 
		FROM MATCHES
	),

	SCORERS_BY_TEAM as (
		SELECT 
			scorer,  
			if(home_away="home",home_team, away_team) as team_name 
		FROM 
			SCORERS
		LEFT JOIN 
			MATCH_TEAMS
		on SCORERS.match_id = MATCH_TEAMS.match_id
		WHERE MATCH_TEAMS.match_round <= 14
	)

SELECT 
	scorer as player_name, 
	team_name, 
	count(scorer) as goals 
FROM SCORERS_BY_TEAM
WHERE scorer != ''
GROUP BY scorer, team_name
ORDER by goals DESC, player_name ASC
LIMIT 3
SELECT scorer as player_name, team_name, count(scorer) as goals FROM (
SELECT scorer,  if(home_away="home",home_team, away_team) as team_name FROM (
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
FROM GOALSCORER) as SCORERS
LEFT JOIN 
(SELECT match_id, match_round, match_hometeam_name as home_team, match_awayteam_name as away_team FROM MATCHES) as MATCHES 
on SCORERS.match_id = MATCHES.match_id
WHERE MATCHES.match_round <= 14) as total
WHERE scorer != ''
GROUP BY scorer, team_name
ORDER by goals DESC, player_name ASC
LIMIT 3
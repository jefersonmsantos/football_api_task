SELECT match_referee as referee_name, count(CARDS.match_id) as cards FROM
(SELECT match_id FROM CARDS) as CARDS
LEFT JOIN
(SELECT match_id, match_referee FROM MATCHES) as MATCHES
ON CARDS.match_id = MATCHES.match_id 
GROUP BY referee_name
ORDER BY cards DESC, referee_name ASC
LIMIT 5;
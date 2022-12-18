-- H1: For each researcher that published to the ICDT conference in 2020:
-- Who was their most frequently occurring co-author (conference & journal)?

-- How many times did they collaborate?
WITH cte AS (
  SELECT DISTINCT author
  FROM (
    SELECT author FROM conference_articles WHERE booktitle = 'ICDT Conference' AND year = '2020'
    UNION ALL
    SELECT author FROM journal_articles WHERE journal = 'ICDT Conference' AND year = '2020'
  ) AS publications
)
SELECT c1.author AS researcher, c2.author AS co_author, COUNT(*) AS num_collaborations
FROM (
  SELECT author, SPLIT_PART(author, ',', 1) AS co_author
  FROM (
    SELECT author FROM conference_articles
    UNION ALL
    SELECT author FROM journal_articles
  ) AS publications
  WHERE author IN (SELECT * FROM cte)
) AS c1
JOIN (
  SELECT author, SPLIT_PART(author, ',', 1) AS co_author
  FROM (
    SELECT author FROM conference_articles
    UNION ALL
    SELECT author FROM journal_articles
  ) AS publications
  WHERE author IN (SELECT * FROM cte)
) AS c2
ON c1.author < c2.author AND c1.co_author = c2.co_author
GROUP BY c1.author, c2.author
ORDER BY num_collaborations DESC;

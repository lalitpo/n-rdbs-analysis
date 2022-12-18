-- Medium M6: For the researcher(s) with the most overall (conference & journal)
-- publications: to how many different conferences did they publish?
WITH cte AS (
  SELECT author, COUNT(*) AS num_publications
  FROM (
    SELECT author FROM conference_articles
    UNION ALL
    SELECT author FROM journal_articles
  ) AS publications
  GROUP BY author
  ORDER BY num_publications DESC
  LIMIT 1
)
SELECT COUNT(DISTINCT booktitle)
FROM conference_articles
WHERE author IN (SELECT author FROM cte);

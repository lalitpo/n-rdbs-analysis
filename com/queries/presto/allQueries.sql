-- E1
SELECT publisher FROM conference_proceedings WHERE booktitle='PODS' LIMIT 1;
-- E2
SELECT title FROM journal_articles WHERE author LIKE '%Martin Grohe%' AND journal = 'Theory Comput. Syst.' ORDER BY title ASC; 
-- M1
SELECT COUNT(*) FROM conference_articles WHERE booktitle = 'SIGMOD Conference' AND year = '2022'; 
-- M2
SELECT COUNT(*) AS num_articles, title FROM journal_articles WHERE year = (SELECT MIN(year) FROM journal_articles) GROUP BY title; 
-- M3
 WITH cte AS ( 
  SELECT year, COUNT(*) AS num_articles 
  FROM conference_articles 
  WHERE booktitle = 'CIDR' 
  GROUP BY year 
) 

SELECT AVG(num_articles) 
FROM cte 
WHERE num_articles IN ( 
  SELECT num_articles 
  FROM cte 
  ORDER BY num_articles ASC 
  LIMIT 1 OFFSET (SELECT COUNT(*) FROM cte) / 2 
); 
-- M4
SELECT year, COUNT(*) AS num_papers 
FROM conference_articles 
WHERE booktitle = 'SIGMOD Conference' AND author LIKE '%,%,%,%,%,%,%,%,%,%,%' 
GROUP BY year 
ORDER BY num_papers DESC 
LIMIT 1; 
-- M5
SELECT editor, COUNT(*) AS num_editions 
FROM conference_proceedings 
WHERE booktitle='PODS'
GROUP BY editor 
ORDER BY num_editions DESC; 
-- M6
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
-- H1
WITH cte AS (
  SELECT DISTINCT author
  FROM (
    SELECT author FROM conference_articles WHERE booktitle = 'ICDT' AND year = '2020'
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
-- H2
WITH RECURSIVE cte (author, distance) AS (
    SELECT 'Paul Erdős', 0
    UNION ALL
    SELECT a.author, c.distance + 1
    FROM cte AS c
    JOIN (
        SELECT author, SPLIT_PART(author, ',', 1) AS co_author
        FROM (
            SELECT author FROM conference_articles
            UNION ALL
            SELECT author FROM journal_articles
        ) AS publications
    ) AS a
    ON c.author = a.co_author
    WHERE a.author <> 'Paul Erdős'
)
SELECT distance
FROM cte
WHERE author = 'Dan Suciu';

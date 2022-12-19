-- Medium M3: What was the median amount of articles published for each
-- year of the CIDR conference.
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
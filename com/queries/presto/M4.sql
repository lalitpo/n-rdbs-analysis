-- Medium M4: In which year did the SIGMOD conference have the most
-- papers with over 10 authors?
SELECT year, COUNT(*) AS num_papers 
FROM conference_articles 
WHERE booktitle = 'SIGMOD Conference' AND author LIKE '%,%,%,%,%,%,%,%,%,%,%' 
GROUP BY year 
ORDER BY num_papers DESC 
LIMIT 1; 
-- Medium M5: Who were the most frequent editors for the PODS conference?
-- How many times were they an editor?
SELECT editor, COUNT(*) AS num_editions 
FROM conference_proceedings 
WHERE booktitle='PODS'
GROUP BY editor 
ORDER BY num_editions DESC; 
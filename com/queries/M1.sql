-- Medium M1: How many articles were published in the SIGMOD conference
-- proceedings this year?
SELECT COUNT(*) FROM conference_articles WHERE booktitle = 'SIGMOD Conference' AND year = '2022'; 

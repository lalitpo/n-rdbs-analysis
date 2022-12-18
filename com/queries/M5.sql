-- Medium M5: Who were the most frequent editors for the PODS conference?
-- How many times were they an editor?
SELECT key,editor FROM conference_proceedings WHERE key LIKE '%conf/pod%' 

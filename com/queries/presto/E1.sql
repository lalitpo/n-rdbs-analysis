-- Easy E1: Who is the publisher of the PODS conference proceedings?
SELECT publisher FROM conference_proceedings WHERE booktitle='PODS' LIMIT 1;

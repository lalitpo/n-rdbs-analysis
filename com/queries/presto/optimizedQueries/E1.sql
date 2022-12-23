-- Easy E1: Who is the publisher of the PODS conference proceedings?
CREATE INDEX idx_booktitle ON conference_proceedings (booktitle); 
SELECT publisher FROM conference_proceedings WHERE booktitle = 'PODS';

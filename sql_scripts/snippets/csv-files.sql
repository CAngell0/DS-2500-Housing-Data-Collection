# Output the properties MySQL table into a csv file 
SELECT * 
FROM properties 
INTO OUTFILE '/var/lib/mysql-files/output.csv' 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n';

# Import a csv file into the properties MySQL table
LOAD DATA INFILE '/var/lib/mysql-files/output.csv' 
INTO TABLE properties
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

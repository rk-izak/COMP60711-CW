-- When running the queries, make sure the user has enough privileges to access
-- local files and that the loading local data is enabled on both server and client 
-- instances. Otherwise, errors such as 1045, 3948, or 2068 might occur.
-- Works for MySQL 8.0.34.
-- Resetting DB.
DROP DATABASE IF EXISTS db_task_4;
CREATE DATABASE db_task_4;
USE db_task_4;

-- Make local files available (so we can skip full paths).
-- Might cause issues as stated above.
SET GLOBAL local_infile=1;

-- Resetting traffic table.
-- No additional structures/parameters etc. needed for the specified 
-- retrieval, as it is one use only for this task.
DROP TABLE IF EXISTS traffic_data_1083;
CREATE TABLE traffic_data_1083 (
date DATETIME,
lane INT,
lane_name VARCHAR(6),
direction INT,
direction_name VARCHAR(10),
speed FLOAT,
headway FLOAT,
gap FLOAT,
flags VARCHAR(20),
flags_txt VARCHAR(50)
);

-- Loading data into table from the provided CSV file and skipping the header.
LOAD DATA LOCAL INFILE 'Datasets/rawpvr_2018-02-01_28d_1415_TueFri.csv' 
INTO TABLE traffic_data_1083
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- Calculating the no. of Tuesday/Fridays between given timespan;
-- again, these could be set as 4, but it is better to make sure anyways.
SET @no_of_tuesdays = (
    SELECT COUNT(DISTINCT DATE(`date`))
    FROM traffic_data_1083
    WHERE HOUR(`date`) BETWEEN 7 AND 23 AND DAYOFWEEK(`date`) = 3
);

SET @no_of_fridays = (
    SELECT COUNT(DISTINCT DATE(`date`))
    FROM traffic_data_1083
    WHERE HOUR(`date`) BETWEEN 7 AND 23 AND DAYOFWEEK(`date`) = 6
);

-- Similarly to python pandas solution, we count the number of rows
-- per specified filters, get the traffic volume,
-- and then calculate the average.
SELECT 
    HOUR(`date`) AS Hour,
    SUM(CASE WHEN DAYOFWEEK(`date`) = 3 THEN 1 ELSE 0 END) / @no_of_tuesdays AS Tuesday,
    SUM(CASE WHEN DAYOFWEEK(`date`) = 6 THEN 1 ELSE 0 END) / @no_of_fridays AS Friday
FROM 
    traffic_data_1083
WHERE 
    HOUR(`date`) BETWEEN 7 AND 23 
    AND DAYOFWEEK(`date`) IN (3, 6)
GROUP BY 
    HOUR(`date`)
ORDER BY 
    HOUR(`date`);

/*
Resultant query should be of the following structure:

+------+-----------+-----------+
| Hour | Tuesday   | Friday    |
+------+-----------+-----------+
|    7 | 4966.5000 | 4806.2500 |
|    8 | 4862.0000 | 4773.0000 |
|    9 | 3978.5000 | 3896.7500 |
|   10 | 3178.7500 | 3284.5000 |
|   11 | 3177.7500 | 3517.7500 |
|   12 | 3408.0000 | 3869.2500 |
|   13 | 3457.0000 | 3949.5000 |
|   14 | 3634.0000 | 4206.7500 |
|   15 | 4286.7500 | 4669.0000 |
|   16 | 5430.2500 | 5362.0000 |
|   17 | 5449.7500 | 5149.0000 |
|   18 | 4452.0000 | 3853.0000 |
|   19 | 2910.0000 | 2770.0000 |
|   20 | 1963.0000 | 2024.2500 |
|   21 | 1495.7500 | 1522.0000 |
|   22 | 1066.5000 | 1398.0000 |
|   23 |  587.7500 | 1041.2500 |
+------+-----------+-----------+
*/

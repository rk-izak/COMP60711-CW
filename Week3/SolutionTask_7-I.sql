-- Again, when running the queries, make sure the user has enough privileges to access
-- local files and that the loading local data is enabled on both server and client 
-- instances. Otherwise, errors such as 1045, 3948, or 2068 might occur.
-- Works for MySQL 8.0.34.
-- Resetting DB.
DROP DATABASE IF EXISTS db_task_7;
CREATE DATABASE db_task_7;
USE db_task_7;

-- Make local files available (so we can skip full paths).
-- Might cause issues as stated above.
SET GLOBAL local_infile=1;

-- Resetting traffic tables.
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

DROP TABLE IF EXISTS traffic_data_1415;
CREATE TABLE traffic_data_1415 (
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

-- Loading data into tablse from the provided CSV files and skipping the header.
LOAD DATA LOCAL INFILE 'Datasets/rawpvr_2018-02-01_28d_1083_TueFri.csv' 
INTO TABLE traffic_data_1083
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'Datasets/rawpvr_2018-02-01_28d_1415_TueFri.csv' 
INTO TABLE traffic_data_1415
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- We delete previously established noisy outliers from both sets.
DELETE FROM traffic_data_1083 WHERE `speed` > 50;
DELETE FROM traffic_data_1415 WHERE `speed` > 50;

-- Similarly to python pandas solution, we combine the speeds taken from both
-- dataframes in a combined frame, of course after filtering for tuples to be
-- on Fridays between 17:00:00 - 17:59:59 in the North direction. Then, we average
-- the speed, change units to [km/h], calculate JT in [hours] and change it to [minutes].
SELECT
    (4.86 / AVG(`speed` * 1.609344)) * 60 AS avgJT_task_6_I
FROM (
    SELECT
        `speed`
    FROM traffic_data_1083
    WHERE DAYOFWEEK(date) = 6
        AND HOUR(date) = 17
        AND direction = 1
    UNION ALL
    SELECT
        `speed`
    FROM traffic_data_1415
    WHERE DAYOFWEEK(date) = 6
        AND HOUR(date) = 17
        AND direction = 1
) AS site_1083_and_1415_data;

/*
Resultant query should be of the following structure:
+-------------------+
| avgJT_task_6_I    |
+-------------------+
| 6.707533123111146 |
+-------------------+
1 row in set (0.43 sec)
*/

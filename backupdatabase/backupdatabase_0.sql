BEGIN TRANSACTION;
CREATE TABLE cashier_cluster(id integer PRIMARY KEY AUTOINCREMENT,                            skill_id int,                            cluster int,                            FOREIGN KEY (skill_id) REFERENCES software_processed_skill(id));
COMMIT;

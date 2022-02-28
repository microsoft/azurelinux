-- For rpm based systems to see if db was migrated already. store opendnssec major minor version
CREATE TABLE rpm_migration (
        major INTEGER,
        minor INTEGER
);
INSERT INTO rpm_migration VALUES(2, 1);


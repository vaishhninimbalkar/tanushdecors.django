PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tanushdecors_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "customer_first_name" varchar(100) NOT NULL, "customer_last_name" varchar(100) NOT NULL, "customer_email" varchar(254) NOT NULL, "customer_phone" varchar(20) NOT NULL, "customer_address" varchar(255) NOT NULL, "customer_state_country" varchar(100) NOT NULL, "total_amount" decimal NOT NULL, "created_at" datetime NOT NULL);
COMMIT;

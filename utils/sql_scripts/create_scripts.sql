CREATE TABLE IF NOT EXISTS "Users" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(500) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS "Goal" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    budget FLOAT NOT NULL,
    user_id INT NOT NULL,
    progress FLOAT DEFAULT 0.0,
    active BOOLEAN DEFAULT FALSE,
    requires_audit BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_goal_user FOREIGN KEY (user_id) REFERENCES "Users"(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "Mission" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    pay FLOAT NOT NULL,
    user_id INT NOT NULL,
    pay_by INT NOT NULL,
    pay_percentage INT NOT NULL,
    contribute_to INT NOT NULL,
    contribute_percentage INT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    active BOOLEAN DEFAULT FALSE,
    requires_audit BOOLEAN DEFAULT TRUE,
    audit_passes BOOLEAN,
    
    CONSTRAINT fk_mission_user FOREIGN KEY (user_id) REFERENCES "Users"(id) ON DELETE CASCADE,
    CONSTRAINT fk_mission_goal FOREIGN KEY (contribute_to) REFERENCES "Goal"(id) ON DELETE CASCADE
);

ALTER TABLE "Mission" ADD COLUMN IF NOT EXISTS pay_percentage INT;
ALTER TABLE "Mission" ADD COLUMN IF NOT EXISTS amount NUMERIC(12, 2);
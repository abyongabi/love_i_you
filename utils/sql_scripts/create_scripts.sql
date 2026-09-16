CREATE TABLE IF NOT EXISTS "Users" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(500) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS "Room" (
    id SERIAL PRIMARY KEY,
    roomname VARCHAR(100) NOT NULL,
    active BOOLEAN DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS "UsersAccess" (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    room_access TEXT[],

    CONSTRAINT fk_usersaccess_user_id FOREIGN KEY (user_id) REFERENCES "Users"(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "Goal" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    budget FLOAT NOT NULL,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    progress FLOAT DEFAULT 0.0,
    active BOOLEAN DEFAULT FALSE,
    requires_audit BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_goal_user FOREIGN KEY (user_id) REFERENCES "Users"(id) ON DELETE CASCADE,
    CONSTRAINT fk_goal_room_id FOREIGN KEY (room_id) REFERENCES "Room"(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "Mission" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    pay NUMERIC(12, 2) NOT NULL,
    user_id INT NOT NULL,
    active BOOLEAN DEFAULT FALSE,
    requires_audit BOOLEAN DEFAULT TRUE,
    audit_passes BOOLEAN,
    
    CONSTRAINT fk_mission_user FOREIGN KEY (user_id) REFERENCES "Users"(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "Contribution" (
    id SERIAL PRIMARY KEY,
    mission_id INT NOT NULL,
    pay_by INT NOT NULL,
    contribute_to INT NOT NULL,
    pay_amount NUMERIC(12, 2) NOT NULL,
    
    CONSTRAINT fk_contribution_mission_id FOREIGN KEY (mission_id) REFERENCES "Mission"(id) ON DELETE CASCADE,
    CONSTRAINT fk_contribution_pay_by FOREIGN KEY (pay_by) REFERENCES "Users"(id) ON DELETE CASCADE,
    CONSTRAINT fk_contribution_contribute_to FOREIGN KEY (contribute_to) REFERENCES "Goal"(id) ON DELETE CASCADE
)

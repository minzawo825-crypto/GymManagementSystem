HHH, [7/5/2026 6:19 PM]
CREATE TABLE Members (
    -- System Keys
    autokey SERIAL PRIMARY KEY,                   -- Auto-increment primary key
    syskey UUID DEFAULT gen_random_uuid() NOT NULL, -- System generated UUID
    
    -- Data Columns (t1, t2, t3...)
    t1 VARCHAR(50) NOT NULL,                      -- fullname
    t2 VARCHAR(50) NOT NULL,                      -- username
    t3 VARCHAR(20) NOT NULL,                      -- contact
    t4 VARCHAR(300)NOT NULL,                      -- address
    t5 VARCHAR(10) NOT NULL DEFAULT 'male',       -- gender                             -- date_of_birth
    t6 DATE NOT NULL    						  -- date
    t7  VARCHAR(50) NOT NULL,                     -- plan
    t8  VARCHAR(50) NOT NULL,                     -- service
    t9  DECIMAL(10, 2) NOT NULL,                  -- amount
  
    
    -- Status Field
    n1 SMALLINT DEFAULT 1 NOT NULL,               -- 1=Active, 4=Deleted
    CONSTRAINT chk_n1 CHECK (n1 IN (1, 4)),
    
    -- Audit Fields
    createddate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- createddate
    createdby VARCHAR(50),                              -- createdby
    modifieddate TIMESTAMP,                                --modifieddate
    modifiedby VARCHAR(50)                               -- modifiedby
);


-- Indexes for performance
CREATE INDEX idx_members_t3 ON Members(t3);      -- email
CREATE INDEX idx_members_t9 ON Members(t9);      -- username
CREATE INDEX idx_members_n1 ON Members(n1);      -- status
CREATE INDEX idx_members_t2 ON Members(t2);      -- last_name

HHH, [7/5/2026 6:20 PM]
-- 2. Trainers / Staff
CREATE TABLE Trainers (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                      -- first_name
    t2 VARCHAR(50) NOT NULL,                      -- last_name
    t3 VARCHAR(100) UNIQUE NOT NULL,              -- email
    t4 VARCHAR(20),                               -- phone
    t5 VARCHAR(100),                              -- specialization
    t6 VARCHAR(50) UNIQUE NOT NULL,               -- username
    t7 VARCHAR(255) NOT NULL,                     -- password_hash
    t8 VARCHAR(200),                              -- address
    t9 TIMESTAMP,                                 -- hire_date
    t10 VARCHAR(50),                              -- position
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t11 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t12 VARCHAR(50), t13 TIMESTAMP, t14 VARCHAR(50)
);

-- 3. Membership Plans
CREATE TABLE Membership_Plans (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                      -- plan_name
    t2 TEXT,                                      -- description
    t3 INTEGER NOT NULL,                          -- duration_days
    t4 DECIMAL(10,2) NOT NULL,                    -- price
    t5 VARCHAR(20),                               -- plan_type
    t6 BOOLEAN DEFAULT TRUE,                      -- is_active
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t7 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t8 VARCHAR(50), t9 TIMESTAMP, t10 VARCHAR(50)
);

-- 4. Member Memberships
CREATE TABLE Member_Memberships (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t2 INTEGER NOT NULL REFERENCES Membership_Plans(autokey), -- plan_id
    t3 DATE NOT NULL,                              -- start_date
    t4 DATE,                                       -- end_date
    t5 VARCHAR(20) DEFAULT 'active',               -- status
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t6 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t7 VARCHAR(50), t8 TIMESTAMP, t9 VARCHAR(50)
);

-- 5. Payments
CREATE TABLE Payments (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t2 INTEGER REFERENCES Member_Memberships(autokey), -- membership_id
    t3 DECIMAL(10,2) NOT NULL,                     -- amount
    t4 DATE NOT NULL,                              -- payment_date
    t5 VARCHAR(30),                                -- payment_method
    t6 VARCHAR(50),                                -- receipt_number
    t7 TEXT,                                       -- notes
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t8 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t9 VARCHAR(50), t10 TIMESTAMP, t11 VARCHAR(50)
);

-- 6. Attendance
CREATE TABLE Attendance (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- check_in
    t3 TIMESTAMP,                                  -- check_out
    t4 VARCHAR(20),                                -- entry_method
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t5 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t6 VARCHAR(50), t7 TIMESTAMP, t8 VARCHAR(50)
);

-- 7. Classes
CREATE TABLE Classes (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                       -- class_name
    t2 TEXT,                                       -- description
    t3 INTEGER,                                    -- max_capacity
    t4 INTEGER,                                    -- duration_minutes
    t5 VARCHAR(50),                                -- class_type
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t6 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t7 VARCHAR(50), t8 TIMESTAMP, t9 VARCHAR

HHH, [7/5/2026 6:20 PM]
(50)
);

-- 8. Class Schedule
CREATE TABLE Class_Schedule (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Classes(autokey), -- class_id
    t2 INTEGER REFERENCES Trainers(autokey),      -- trainer_id
    t3 TIMESTAMP NOT NULL,                         -- start_time
    t4 TIMESTAMP NOT NULL,                         -- end_time
    t5 VARCHAR(50),                                -- room
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t6 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t7 VARCHAR(50), t8 TIMESTAMP, t9 VARCHAR(50)
);

-- 9. Class Bookings
CREATE TABLE Class_Bookings (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Class_Schedule(autokey), -- schedule_id
    t2 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t3 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,       -- booking_date
    t4 VARCHAR(20) DEFAULT 'confirmed',            -- status
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t5 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t6 VARCHAR(50), t7 TIMESTAMP, t8 VARCHAR(50)
);

-- 10. Equipment
CREATE TABLE Equipment (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                       -- equipment_name
    t2 VARCHAR(50),                                -- location
    t3 DATE,                                       -- purchase_date
    t4 VARCHAR(30) DEFAULT 'operational',          -- status
    t5 VARCHAR(100),                               -- manufacturer
    t6 VARCHAR(50),                                -- model
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t7 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t8 VARCHAR(50), t9 TIMESTAMP, t10 VARCHAR(50)
);

HHH, [7/5/2026 6:43 PM]
Ah, I understand now! You want t1, t2, t3... as the actual column names, and specifically want autokey, syskey, and n1 as separate columns. Here's the corrected version:

PostgreSQL CREATE TABLE for Members
sql
CREATE TABLE Members (
    -- System Keys
    autokey SERIAL PRIMARY KEY,                   -- Auto-increment primary key
    syskey UUID DEFAULT gen_random_uuid() NOT NULL, -- System generated UUID
    
    -- Data Columns (t1, t2, t3...)
    t1 VARCHAR(50) NOT NULL,                      -- first_name
    t2 VARCHAR(50) NOT NULL,                      -- last_name
    t3 VARCHAR(100) UNIQUE NOT NULL,              -- email
    t4 VARCHAR(20),                               -- phone
    t5 DATE,                                      -- date_of_birth
    t6 CHAR(1) CHECK (t6 IN ('M', 'F', 'O')),     -- gender
    t7 VARCHAR(200),                              -- address
    t8 DATE DEFAULT CURRENT_DATE NOT NULL,        -- join_date
    t9 VARCHAR(50) UNIQUE NOT NULL,               -- username
    t10 VARCHAR(255) NOT NULL,                    -- password_hash
    t11 TIMESTAMP,                                -- last_login
    t12 VARCHAR(100),                             -- emergency_contact_name
    t13 VARCHAR(20),                              -- emergency_contact_phone
    t14 VARCHAR(500),                             -- medical_notes
    t15 VARCHAR(255),                             -- profile_picture_url
    
    -- Status Field
    n1 SMALLINT DEFAULT 1 NOT NULL,               -- 1=Active, 4=Deleted
    CONSTRAINT chk_n1 CHECK (n1 IN (1, 4)),
    
    -- Audit Fields
    t16 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- created_at
    t17 VARCHAR(50),                              -- created_by
    t18 TIMESTAMP,                                -- updated_at
    t19 VARCHAR(50)                               -- updated_by
);

-- Indexes for performance
CREATE INDEX idx_members_t3 ON Members(t3);      -- email
CREATE INDEX idx_members_t9 ON Members(t9);      -- username
CREATE INDEX idx_members_n1 ON Members(n1);      -- status
CREATE INDEX idx_members_t2 ON Members(t2);      -- last_name
Column Mapping Reference
Column Purpose Data Type
autokey Auto-increment primary key SERIAL
syskey System generated UUID UUID
t1 first_name VARCHAR(50)
t2 last_name VARCHAR(50)
t3 email VARCHAR(100)
t4 phone VARCHAR(20)
t5 date_of_birth DATE
t6 gender CHAR(1)
t7 address VARCHAR(200)
t8 join_date DATE
t9 username VARCHAR(50)
t10 password_hash VARCHAR(255)
t11 last_login TIMESTAMP
t12 emergency_contact_name VARCHAR(100)
t13 emergency_contact_phone VARCHAR(20)
t14 medical_notes VARCHAR(500)
t15 profile_picture_url VARCHAR(255)
n1 Status (1=Active, 4=Deleted) SMALLINT
t16 created_at TIMESTAMP
t17 created_by VARCHAR(50)
t18 updated_at TIMESTAMP
t19 updated_by VARCHAR(50)
Sample Queries
Insert a new member
sql
INSERT INTO Members (
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t17
) VALUES (
    'John', 'Doe', 'john.doe@email.com', '555-1234',
    '1990-05-15', 'M', '123 Main St', CURRENT_DATE,
    'johndoe', 'hashed_password_here', 'admin'
);
Query active members
sql
-- Get all active members
SELECT 
    autokey, syskey, t1, t2, t3, t9, t8, n1
FROM Members 
WHERE n1 = 1 
ORDER BY t2, t1;
Soft delete (set n1 = 4)
sql
UPDATE Members 
SET n1 = 4, 
    t18 = CURRENT_TIMESTAMP,
    t19 = 'admin_user'
WHERE autokey = 123;
Reactivate member (set n1 = 1)
sql
UPDATE Members 
SET n1 = 1,
    t18 = CURRENT_TIMESTAMP,
    t19 = 'admin_user'
WHERE autokey = 123;
Login attempt
sql
-- Update last_login on successful login
UPDATE Members 
SET t11 = CURRENT_TIMESTAMP 
WHERE t9 = 'johndoe' AND n1 = 1;
Search members
sql
-- Search by name or email
SELECT autokey, t1, t2, t3, t9, n1
FROM Members 
WHERE t1 ILIKE '%john%' 
   OR t2 ILIKE '%john%' 
   OR t3 ILIKE '%john%'
   AND n1 = 1;
Complete Schema for All Core Tables
sql
-- 1. Members Table
CREATE TABLE Members (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL, t2 VARCHAR(50) NOT NULL,
    t3 VARCHAR(100) UNIQUE NOT NULL, t4 VARCHAR(20),

HHH, [7/5/2026 6:43 PM]
t5 DATE, t6 CHAR(1) CHECK (t6 IN ('M','F','O')),
    t7 VARCHAR(200), t8 DATE DEFAULT CURRENT_DATE NOT NULL,
    t9 VARCHAR(50) UNIQUE NOT NULL, t10 VARCHAR(255) NOT NULL,
    t11 TIMESTAMP, t12 VARCHAR(100), t13 VARCHAR(20),
    t14 VARCHAR(500), t15 VARCHAR(255),
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t16 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t17 VARCHAR(50), t18 TIMESTAMP, t19 VARCHAR(50)
);

-- 2. Trainers / Staff
CREATE TABLE Trainers (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                      -- first_name
    t2 VARCHAR(50) NOT NULL,                      -- last_name
    t3 VARCHAR(100) UNIQUE NOT NULL,              -- email
    t4 VARCHAR(20),                               -- phone
    t5 VARCHAR(100),                              -- specialization
    t6 VARCHAR(50) UNIQUE NOT NULL,               -- username
    t7 VARCHAR(255) NOT NULL,                     -- password_hash
    t8 VARCHAR(200),                              -- address
    t9 TIMESTAMP,                                 -- hire_date
    t10 VARCHAR(50),                              -- position
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t11 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t12 VARCHAR(50), t13 TIMESTAMP, t14 VARCHAR(50)
);

-- 3. Membership Plans
CREATE TABLE Membership_Plans (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                      -- plan_name
    t2 TEXT,                                      -- description
    t3 INTEGER NOT NULL,                          -- duration_days
    t4 DECIMAL(10,2) NOT NULL,                    -- price
    t5 VARCHAR(20),                               -- plan_type
    t6 BOOLEAN DEFAULT TRUE,                      -- is_active
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t7 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t8 VARCHAR(50), t9 TIMESTAMP, t10 VARCHAR(50)
);

-- 4. Member Memberships
CREATE TABLE Member_Memberships (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t2 INTEGER NOT NULL REFERENCES Membership_Plans(autokey), -- plan_id
    t3 DATE NOT NULL,                              -- start_date
    t4 DATE,                                       -- end_date
    t5 VARCHAR(20) DEFAULT 'active',               -- status
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t6 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t7 VARCHAR(50), t8 TIMESTAMP, t9 VARCHAR(50)
);

-- 5. Payments
CREATE TABLE Payments (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t2 INTEGER REFERENCES Member_Memberships(autokey), -- membership_id
    t3 DECIMAL(10,2) NOT NULL,                     -- amount
    t4 DATE NOT NULL,                              -- payment_date
    t5 VARCHAR(30),                                -- payment_method
    t6 VARCHAR(50),                                -- receipt_number
    t7 TEXT,                                       -- notes
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t8 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t9 VARCHAR(50), t10 TIMESTAMP, t11 VARCHAR(50)
);

-- 6. Attendance
CREATE TABLE Attendance (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- check_in
    t3 TIMESTAMP,                                  -- check_out
    t4 VARCHAR(20),                                -- entry_method
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t5 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t6 VARCHAR(50), t7 TIMESTAMP, t8 VARCHAR(50)
);

-- 7. Classes
CREATE TABLE Classes (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                       --

HHH, [7/5/2026 6:43 PM]
class_name
    t2 TEXT,                                       -- description
    t3 INTEGER,                                    -- max_capacity
    t4 INTEGER,                                    -- duration_minutes
    t5 VARCHAR(50),                                -- class_type
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t6 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t7 VARCHAR(50), t8 TIMESTAMP, t9 VARCHAR(50)
);

-- 8. Class Schedule
CREATE TABLE Class_Schedule (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Classes(autokey), -- class_id
    t2 INTEGER REFERENCES Trainers(autokey),      -- trainer_id
    t3 TIMESTAMP NOT NULL,                         -- start_time
    t4 TIMESTAMP NOT NULL,                         -- end_time
    t5 VARCHAR(50),                                -- room
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t6 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t7 VARCHAR(50), t8 TIMESTAMP, t9 VARCHAR(50)
);

-- 9. Class Bookings
CREATE TABLE Class_Bookings (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 INTEGER NOT NULL REFERENCES Class_Schedule(autokey), -- schedule_id
    t2 INTEGER NOT NULL REFERENCES Members(autokey), -- member_id
    t3 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,       -- booking_date
    t4 VARCHAR(20) DEFAULT 'confirmed',            -- status
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t5 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t6 VARCHAR(50), t7 TIMESTAMP, t8 VARCHAR(50)
);

-- 10. Equipment
CREATE TABLE Equipment (
    autokey SERIAL PRIMARY KEY,
    syskey UUID DEFAULT gen_random_uuid() NOT NULL,
    t1 VARCHAR(50) NOT NULL,                       -- equipment_name
    t2 VARCHAR(50),                                -- location
    t3 DATE,                                       -- purchase_date
    t4 VARCHAR(30) DEFAULT 'operational',          -- status
    t5 VARCHAR(100),                               -- manufacturer
    t6 VARCHAR(50),                                -- model
    n1 SMALLINT DEFAULT 1 CHECK (n1 IN (1,4)),
    t7 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    t8 VARCHAR(50), t9 TIMESTAMP, t10 VARCHAR(50)
);
Quick Reference
Table PK Syskey Status Column Active Value Deleted Value
Members autokey syskey n1 1 4
Trainers autokey syskey n1 1 4
Membership_Plans autokey syskey n1 1 4
Member_Memberships autokey syskey n1 1 4
Payments autokey syskey n1 1 4
Attendance autokey syskey n1 1 4
Classes autokey syskey n1 1 4
Class_Schedule autokey syskey n1 1 4
Class_Bookings autokey syskey n1 1 4
Equipment autokey syskey n1 1 4
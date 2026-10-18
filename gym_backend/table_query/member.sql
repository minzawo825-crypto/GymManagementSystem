C:\Users\Lenovo>python
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import uuid
>>> print(uuid.uuid4().hex)
c113d9ee87aa4cb4968d37e77b31dfb9
>>>
CREATE TABLE members (
    autokey BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    syskey VARCHAR(50) NOT NULL UNIQUE,

    -- Data Columns
    t1 VARCHAR(50) NOT NULL,              -- Full Name
    t2 VARCHAR(50) NOT NULL,              -- Username
    t3 VARCHAR(20) NOT NULL,              -- Contact
    t4 VARCHAR(300) NOT NULL,             -- Address
    t5 VARCHAR(10) NOT NULL,              -- Gender
    t6 VARCHAR(50) NOT NULL,              -- Plan
    t7 VARCHAR(50) NOT NULL,              -- Service
    t8 DECIMAL(10,2) NOT NULL,            -- Amount

    -- Status
    n1 SMALLINT NOT NULL DEFAULT 1,
    CONSTRAINT chk_members_n1 CHECK (n1 IN (1, 4)),

    -- Audit Fields
    createddate TIMESTAMPTZ,
    createdby VARCHAR(50),
    modifieddate TIMESTAMPTZ,
    modifiedby VARCHAR(50)
);
CREATE TABLE gender (
    autokey bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    syskey VARCHAR(50) NOT NULL UNIQUE,

    t1 VARCHAR(50) NOT NULL                      -- male/female(gender)

);
INSERT INTO gender (syskey, t1)
VALUES
    ('c113d9ee87aa4cb4968d37e77b31dfb9', 'Male'),
    ('f85beba2b0a546aca431bd67fb9658ff', 'Female');
CREATE TABLE plan (
    -- System Keys
    autokey bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    syskey VARCHAR(50) NOT NULL UNIQUE,

    t1 VARCHAR(50) NOT NULL                    --months

);
INSERT INTO plan (syskey, t1)
VALUES
    ('531f27c8eccb4f1ea618335862de0037', 'One Month'),
    ('c6c6a56059e349bf9d39616610a9fcda', 'Two Months'),
    ('857f97cc454a49b58fc462e4c77f077e', 'Three Months');
    
CREATE TABLE service (
    -- System Keys
    autokey bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    syskey VARCHAR(50) NOT NULL UNIQUE,

    t1 VARCHAR(50) NOT NULL,                      -- service
    t2 VARCHAR(50) NOT NULL                     -- amount

);
INSERT INTO service (syskey, t1, t2)
VALUES
    ('d89f98494a5643b5a43f9fb541f52f42', 'Fitness', 60000),
    ('700e5d5b3cfe4d2b9085f91ac8a7c320', 'Sauna', 50000),
    ('6623dd7bfec14070aa904dba603fb616', 'Cardio', 55000);

DROP TABLE IF EXISTS members;
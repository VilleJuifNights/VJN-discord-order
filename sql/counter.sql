CREATE SEQUENCE counter_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 999
    CYCLE;

-- SELECT nextval('counter_seq');
-- SELECT setval('counter_seq', 1, false);
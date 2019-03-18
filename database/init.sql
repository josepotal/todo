CREATE TABLE todos (
  id SERIAL NOT NULL,
  name character varying,
  created timestamp with time zone NOT NULL DEFAULT NOW(),
  completed timestamp with time zone NULL
  complete boolean NOT NULL DEFAULT FALSE
)

-- ALTER TABLE todos ADD COLUMN created timestamp with time zone NOT NULL DEFAULT NOW()
 
-- ALTER TABLE todos ADD COLUMN completed timestamp with time zone NULL
-- ALTER TABLE todos ADD COLUMN complete boolean NOT NULL DEFAULT FALSE
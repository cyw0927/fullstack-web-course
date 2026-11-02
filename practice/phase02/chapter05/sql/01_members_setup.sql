-- Optional initial setup for chapter05/06. Review target DB/schema before executing.
-- Use the PostgreSQL database named postgres and public schema as in the user's lab.
CREATE TABLE IF NOT EXISTS public.members (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL
);

-- Sample rows only if the email is not already present.
-- Execute this optional seed block intentionally (do not add duplicate students).
INSERT INTO public.members (name, email, age)
SELECT 'Kim', 'kim@example.com', 25
WHERE NOT EXISTS (
    SELECT 1 FROM public.members WHERE email = 'kim@example.com'
);

INSERT INTO public.members (name, email, age)
SELECT 'Lee', 'lee@example.com', 31
WHERE NOT EXISTS (
    SELECT 1 FROM public.members WHERE email = 'lee@example.com'
);

-- Verification:
SELECT id, name, email, age FROM public.members ORDER BY id;

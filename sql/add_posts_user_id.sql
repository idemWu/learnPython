-- PostgreSQL：给已有表 posts 增加 user_id，与 models.Post 一致
-- 在 psql / pgAdmin / DBeaver 里对着 DATABASE_URL 里的库执行

ALTER TABLE posts ADD COLUMN IF NOT EXISTS user_id INTEGER;

-- 若表里已有文章但 user_id 为空：先全部挂到「最小 id 的用户」上（开发环境够用）
UPDATE posts
SET user_id = (SELECT id FROM users ORDER BY id LIMIT 1)
WHERE user_id IS NULL;

ALTER TABLE posts ALTER COLUMN user_id SET NOT NULL;

-- 外键（若已存在同名约束可先 DROP 再执行）
ALTER TABLE posts DROP CONSTRAINT IF EXISTS posts_user_id_fkey;
ALTER TABLE posts ADD CONSTRAINT posts_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users (id);

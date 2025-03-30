-- Удаляем старый тип, если он существует
DROP TYPE IF EXISTS newscategory CASCADE;

-- Создаем тип newscategory
CREATE TYPE newscategory AS ENUM (
    'Политика',
    'Экономика',
    'Технологии',
    'Спорт',
    'Общество',
    'Наука',
    'Развлечения',
    'Происшествия',
    'Международные',
    'Региональные',
    'Общее'
);

-- Добавляем столбец category, если его нет
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'news'
        AND column_name = 'category'
    ) THEN
        ALTER TABLE news ADD COLUMN category newscategory;
    END IF;
END $$;

-- Изменяем тип столбца category
ALTER TABLE news ALTER COLUMN category TYPE newscategory USING category::newscategory; 
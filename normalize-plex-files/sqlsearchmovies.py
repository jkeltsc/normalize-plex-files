-- 0 ; moviessearch="""
-- 
-- important: do not touch the »-- 0 ; moviessearch=”””« first line and the »-- ”””« last line,
-- they make this file valid python code and at the same time valid sqlite3 code.
--
-- Note: the ””” actually used in line 1 and the last line are normal double quotes (QUOTATION MARK).
-- To not interfere with these, this comment uses ””” instead (RIGHT DOUBLE QUOTATION MARK).
-- 
-- python3 can happily import this file using "from sqlsearchmovies import moviessearch".
-- For python, »-- 0« means 0 (could be any number, like --2=-(-2)=2) and is simply ignored
-- during import. The relevant code for python is »moviessearch=”””« expanding right down
-- to the final »-- ”””«. This is one single multi-line string containing one valid sqlite statement.
--
-- https://docs.python.org/3/library/sqlite3.html will be happy with the string imported by
-- python, as described above, being one single multi-line sqlite statement.
--
-- VSCode SQLite can happily run this file as SQLite code (swith vs code language to SQL or SQLite).
-- https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite
-- However, to find any results you need to set the named parameter »:movies_section_name«
-- in settings.json as in the example below, using whatever name your movies library actually uses:
--     "sqlite.setupDatabase": {      
--       "./plex.db": {"sql": [".parameter init",".parameter set :movies_section_name \"'Filme'\"",".parameter set :series_section_name \"'Serien'\""]}
--     }
--
-- Prettier-SQL will also be happy with this file (swith vs code language to SQLite).
-- https://marketplace.visualstudio.com/items?itemName=inferrinizzard.prettier-sql-vscode
--
SELECT
    metadata_items.title,
    metadata_items.year,
    metadata_items.edition_title AS edition,
    (
        CASE
            WHEN NOT tags.tmdb = '' THEN REPLACE(tags.tmdb, '://', '-')
            WHEN NOT tags.imdb = '' THEN REPLACE(tags.imdb, '://', '-')
            WHEN NOT tags.tvdb = '' THEN REPLACE(tags.tvdb, '://', '-')
            ELSE NULL
        END
    ) AS db_ref,
    media.width,
    media.height,
    media.files
FROM
    metadata_items
    LEFT JOIN library_sections ON library_sections.id = metadata_items.library_section_id
    LEFT JOIN (
        SELECT
            media_items.metadata_item_id,
            media_items.width,
            media_items.height,
            media_items.id,
            /* use || as filename separator, to prevent || in filenames escape each | as \| */
            GROUP_CONCAT(REPLACE(media_parts.file, '|', '\|'), '||') AS files
        FROM
            media_items
            LEFT JOIN media_parts ON media_parts.media_item_id = media_items.id
        GROUP BY
            media_items.id
    ) AS media ON media.metadata_item_id = metadata_items.id
    LEFT JOIN (
        SELECT
            taggings.metadata_item_id,
            MIN(imdb.tag) AS imdb,
            MIN(tmdb.tag) AS tmdb,
            MIN(tvdb.tag) AS tvdb
        FROM
            taggings
            LEFT JOIN tags AS imdb ON taggings.tag_id = imdb.id
            AND imdb.tag_type = 314
            AND imdb.tag LIKE 'imdb://%'
            LEFT JOIN tags AS tmdb ON taggings.tag_id = tmdb.id
            AND tmdb.tag_type = 314
            AND tmdb.tag LIKE 'tmdb://%'
            LEFT JOIN tags AS tvdb ON taggings.tag_id = tvdb.id
            AND tvdb.tag_type = 314
            AND tvdb.tag LIKE 'tvdb://%'
        GROUP BY
            taggings.metadata_item_id
    ) AS tags ON tags.metadata_item_id = metadata_items.id
WHERE
    metadata_items.title IS NOT NULL
    AND metadata_items.title != ''
    AND library_sections.name = :movies_section_name
    AND metadata_items.metadata_type = 1
GROUP BY
    media.id
ORDER BY
    metadata_items.title ASC;

-- """
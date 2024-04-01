WITH ids_to_delete AS (
  SELECT id
  FROM public.reddit_watches
  GROUP BY id
  HAVING COUNT(id) > 1
)
DELETE FROM public.reddit_watches
WHERE id IN (SELECT id FROM ids_to_delete);
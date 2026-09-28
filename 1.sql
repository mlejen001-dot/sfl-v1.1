SELECT 
    COUNT(*) 
FROM recipes r
LEFT JOIN flowers f
ON r.flower_id = f.id
WHERE f.id IS NULL;
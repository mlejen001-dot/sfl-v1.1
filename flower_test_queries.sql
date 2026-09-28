SELECT * FROM flowers ORDER BY name;

SELECT f.name AS flower,s.name AS seed,i.name AS ingredient,ri.quantity,f.base_time_seconds AS time
FROM recipes r JOIN flowers f ON f.id=r.flower_id
LEFT JOIN seeds s ON s.id=r.seed_id
LEFT JOIN recipe_ingredients ri ON ri.recipe_id=r.id
LEFT JOIN ingredients i ON i.id=ri.ingredient_id;

SELECT f.name AS flower,s.name AS seed,r.id AS recipe_id
FROM recipes r JOIN flowers f ON f.id=r.flower_id
JOIN seeds s ON s.id=r.seed_id
WHERE s.name=?;

SELECT f.name AS flower,s.name AS seed,i.name AS ingredient,ri.quantity
FROM recipes r JOIN flowers f ON f.id=r.flower_id
JOIN seeds s ON s.id=r.seed_id
JOIN recipe_ingredients ri ON ri.recipe_id=r.id
JOIN ingredients i ON i.id=ri.ingredient_id
WHERE f.name=?
ORDER BY i.name;

SELECT f.name,f.base_time_seconds
FROM flowers f
ORDER BY CASE WHEN f.base_time_seconds IS NULL THEN 1 ELSE 0 END,
f.base_time_seconds ASC;

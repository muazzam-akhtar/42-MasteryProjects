ALTER TABLE customers
ADD COLUMN category_id BIGINT,
ADD COLUMN category_code VARCHAR(255),
ADD COLUMN brand VARCHAR(255);

UPDATE customers cust
SET
	category_id = prod.category_id,
	category_code = prod.category_code,
	brand = prod.brand
FROM (
	SELECT
		product_id,
		COALESCE(MAX(category_id), NULL) AS category_id,
		COALESCE(MAX(category_code), NULL) AS category_code,
		COALESCE(MAX(brand), NULL) AS brand
	FROM items
	GROUP BY product_id
) AS prod
WHERE cust.product_id = prod.product_id;
DELETE FROM customers
WHERE ctid IN (
    SELECT ctid
    FROM (
        SELECT ctid,
               event_time,
               LAG(event_time) OVER (
                   PARTITION BY event_type, product_id, user_id
                   ORDER BY event_time
               ) AS prev_event_time
        FROM customers
    ) sub
    WHERE 
        prev_event_time IS NOT NULL
        AND ABS(EXTRACT(EPOCH FROM event_time - prev_event_time)) <= 1
);
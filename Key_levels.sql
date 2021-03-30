
--RESISTANCE
With Current_price_getter AS (
	SELECT "close" AS current_price
	FROM xrp_5_minutes_deduped
	ORDER BY open_time DESC
	LIMIT 1
) SELECT
	kl.number_of_ranges,
	kl.price_range_start,
	kl.price_range_stop,
	kl.high_count,
	kl.average_of_start_stop,
	cpg.current_price ,
	((kl.average_of_start_stop - price_range_start)/ price_range_start)* 100 AS percentage_diff_from_current_price
FROM
	Current_price_getter cpg, high_key_levels kl
WHERE average_of_start_stop > cpg.current_price
	AND kl.high_count > 0
ORDER BY kl.high_count DESC, kl.price_range_start
LIMIT 5

--SUPPORT

With Current_price_getter AS (SELECT "close" AS current_price
FROM xrp_5_minutes_deduped
ORDER BY open_time DESC
LIMIT 1)
SELECT kl.number_of_ranges, kl.price_range_start, kl.price_range_stop, kl.high_count, kl.average_of_start_stop, cpg.current_price
	, ((kl.average_of_start_stop - cpg.current_price)/cpg.current_price)*100 AS percentage_diff_from_current_price
FROM Current_price_getter cpg, high_key_levels kl
WHERE kl.average_of_start_stop < cpg.current_price
AND kl.high_count > 0
ORDER BY kl.high_count DESC, kl.price_range_start
--ORDER BY  kl.price_range_stop DESC
LIMIT 10




            
With Current_price_getter AS (SELECT "close" AS current_price
            FROM xrp_5_minutes_deduped
            ORDER BY open_time DESC 
            LIMIT 1)
       SELECT kl.number_of_ranges, kl.price_range_start, kl.price_range_stop, kl.high_count
            , kl.average_of_start_stop, cpg.current_price
            --, ((price_range_stop - price_range_start)/price_range_start)*100 AS percentage_diff_from_current_price
        FROM Current_price_getter cpg, high_key_levels kl
        WHERE --average_of_start_stop > '0.43625' --cpg.current_price
            --AND 
            kl.high_count > (SELECT AVG(high_count) FROM high_key_levels)  --(average count of high_count from high_key_levels)
            ORDER BY  kl.price_range_start DESC , kl.high_count DESC --
            --LIMIT 5
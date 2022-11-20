-- to get top 10 members by spending
select membership_id, sum(total_items_price) total_spend
from fact.transaction
where is_current = True
group by membership_id
order by total_spend desc
limit 10;

-- to get top 3 items that are frequently bought by members
-- the assumption is that these items are involved in most different transactions
select item_id, count(distinct transaction_id) item_purchased_times
from dim.transaction_item
where is_current = True
group by item_id
order by item_purchased_times desc
limit 3;
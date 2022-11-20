For logistics team :
- assumptions :
    - the team wants to track item and transactions details
    - the team does not manage delivery of items to members
- create 2 stored procedures below. These stored procedures are of type security definer (sysadmin). The rationale behind this is to provide a template for users to minimize errors in metadata field that are managed by data engineers
    - sp_update_item_in_transaction(transaction_id, item_id, item_count)
        the assumption is that logistics team need to remove some items from some transactions as they might not be in stock. this stored procedure also updates transaction table by deducting or adding total cost or total weight.
    - sp_update_total_price_or_weight(transaction_id, total_items_price, total_items_weight)
        the assumption is logistics team need to change the price or weight in case there is an additional price or weight on top of the individual items price or weight
    
- create a logistic role with the following accesses :
    - select on transaction, item, and transaction_item
    - execute on procedure sp_update_item_in_transaction and sp_update_total_price_or_weight

For analytics team :
- create an analytics role with the following accesses :
    - select on transaction, transaction_item, item, and member

For sales team :
- create 2 stored procedures below. These stored procedures are of type security definer (sysadmin). The rationale behind this is to provide a template for users to minimize errors in metadata field that are managed by data engineers
    - sp_add_new_items(item_id, item_name, manufacturer_name, cost, weight)
        all parameters are arrays to support insert of multiple items
    - sp_remove_items(item_id)
        update item table for item_id=item_id with end_time=current_timestamp()
- create a sales role with the following accesses :
    - select on item
    - execute on procedure sp_add_new_items and sp_remove_items



def convert(convert_list):
    # Конвертирует список с p[(5,),(8,),...] к [5,8,...]
    return [item[0] for item in convert_list]


def total_coast(list_quantity, list_price):
    order_total_cost = 0
    for ind, itm in enumerate(list_price):
        order_total_cost += list_quantity[ind]*list_price[ind]
        return order_total_cost


def total_quantity(list_quantity):
    order_total_quantity = 0
    for itm in list_quantity:
        order_total_quantity += itm
        return order_total_quantity


def get_total_coast(db):
    """
    Возвращает общую стоимость товара
    """
    all_product_id = db.get_all_products_id()
    all_price = [db.select_single_product_price(itm) for itm in all_product_id]
    all_quantity = [db.select_order_quantity(itm) for itm in all_product_id]
    return total_coast(all_quantity, all_price)


def get_total_quantity(db):
    """
    Возвращает общее количество заказанной единицы товара
    """
    all_product_id = db.get_all_products_id()
    all_quantity = [db.select_order_quantity(itm) for itm in all_product_id]
    return total_quantity(all_quantity)

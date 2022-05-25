from datetime import datetime
from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.dbcore import Base
from models.order import Order
from settings import config, utility

from models.product import Product


class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД
    """
    def __init__(self):
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_products_category(self, category):
        """
        Возвращает все товары
        """
        result = self._session.query(Product).filter_by(
            category_id=category).all()

        self.close()
        return result

    def add_orders(self, quantity, product_id, user_id, ):
        """
        Метод заполнения заказа
        """
        all_id_product = self.get_all_products_id()
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)

            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)

        self._session.add(order)
        self._session.commit()
        self.close()

    def get_all_products_id(self):
        """
        Возвращает все id товара в заказе
        """
        result = self._session.query(Order.product_id).all()
        self.close()
        return utility.convert(result)

    def select_order_quantity(self, product_id):
        """
        Возвращает количество товара в заказе
        """
        result = self._session.query(Order.quantity).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity

    def select_single_product_quantity(self, rownum):
        """
        Возвращает количество товара на складе
        в соответствии с номером товара - rownum
        """
        result = self._session.query(
            Product.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def update_product_value(self, rownum, name, value):
        """
        Обновляет количество товара на складе
        в соответствии с номером товара - rownum
        """
        self._session.query(Product).filter_by(
            id=rownum).update({name: value})
        self._session.commit()
        self.close()

    def update_order_value(self, product_id, name, value):
        """
        Обновляет данные указанной позиции заказа
        в соответствии с номером товара - rownum
        """
        self._session.query(Order).filter_by(
            product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_name(self, rownum):
        """
        Возвращает название товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Product.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_title(self, rownum):
        """
        Возвращает торговую марку товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Product.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        """
        Возвращает цену товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Product.price).filter_by(id=rownum).one()
        self.close()
        return result.price

    def count_rows_order(self):
        """
        Возвращает количество позиций в заказе
        """
        result = self._session.query(Order).count()
        self.close()
        return result

    def select_order_quantity(self, product_id):
        """
        Возвращает количество товара из заказа
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Order.quantity).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity

    def delete_order(self, product_id):
        self._session.query(Order).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def delete_all_order(self):
        """
        Удаляет данные всего заказа
        """
        all_id_orders = self.get_all_order_id()

        for itm in all_id_orders:
            self._session.query(Order).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def get_all_order_id(self):
        """
        Возвращает все id заказа
        """
        result = self._session.query(Order.id).all()
        self.close()
        return utility.convert(result)

    def close(self):
        """ Закрывает сессию """
        self._session.close()

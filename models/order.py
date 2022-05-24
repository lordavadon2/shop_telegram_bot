from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from models.product import Product

Base = declarative_base()


class Order(Base):
    """
    Класс-модель для описания таблиы "Заказ"
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)

    products = relationship(Product,
                            backref=backref(
                                'orders',
                                uselist=True,
                                cascade="all,delete"
                            ))

    def __str__(self):
        """
        Метод возвращает строковое представления обьекта класса
        :return: str
        """
        return f"{self.quantity} {self.data}"

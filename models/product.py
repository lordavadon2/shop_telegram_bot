from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

from db.dbcore import Base
from models.category import Category


class Product(Base):
    """
    Класс-модель для описания таблиы "Тoвар"
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship(Category,
                            backref=backref(
                                'products',
                                uselist=True,
                                cascade="all,delete"
                            ))

    def __str__(self):
        """
        Метод возвращает строковое представления обьекта класса
        :return: str
        """
        return f"{self.name} {self.title} {self.price}"

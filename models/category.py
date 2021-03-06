from sqlalchemy import Column, String, Integer, Boolean

from db.dbcore import Base


class Category(Base):
    """
    Класс-модель для описания таблиы "Категория товара"
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        """
        Метод возвращает строковое представления обьекта класса
        :return: str
        """
        return self.name

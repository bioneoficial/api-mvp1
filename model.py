from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Comissao(Base):
    __tablename__ = 'comissao'

    id = Column(Integer, primary_key=True)
    vendedor = Column(String(100), nullable=False)
    produto = Column(String(100), nullable=False)
    valor_venda = Column(Float, nullable=False)
    comissao_calculada = Column(Float, nullable=False)
    data_venda = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "vendedor": self.vendedor,
            "produto": self.produto,
            "valor_venda": self.valor_venda,
            "comissao_calculada": self.comissao_calculada,
            "data_venda": self.data_venda.strftime("%Y-%m-%d %H:%M:%S")
        }

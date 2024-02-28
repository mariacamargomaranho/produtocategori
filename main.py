import string
import uuid
from tokenize import String

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import (Column, Uuid, String, DateTime, func, DECIMAL, Boolean, Integer

motor = create_engine("sqlite+pysqlite:///banco_de_dados.sqlite",
                      echo=True)

class Base(DeclarativeBase):
    pass

class Categoria(Base):
    __tablename__ = 'tbl_categorias'
    id = Column(uuid(as_uuid=true),
         primary_key=true,
         default=uuid.uuid4())
    nome = Column(String,(256),
                  nullable=False)

    lista_de_produtos = relationship("Produto", back_populates="categoria",
                                      cascade='all, delete-orphan', lazy='selectin')

    dta_cadastro = Column(DateTime,
                          server_default=func.now(),
                          nullable=False)
    dta_atualizacao = Column(DateTime,
                             onupdate=func.now(),
                             default=func.now(),
                             nullable=False)

    class Produto(Base, DatasMixin):
        __tablename__ = 'tbl_produtos'
        id = Column(Uuid(as_Uuid=True), primary_key=True, default=uuid4)
        nome = Column(String,(256),nullable=False)
        preco = Column(DECIMAL(10,2), default=0.00)
        estoque = Column(Integer, default=0)
        ativo = Column(Boolean, default=True)
        Categoria_id = Column(Uuid(as_Uuid=True), foreign_keys("tbl_categorias.id"))

        categoria = relationship("Categoria", back_populates="lista_de_produtos")



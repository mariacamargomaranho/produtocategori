import uuid

from sqlalchemy import (Column, Uuid, String, DateTime,
                        func, DECIMAL, Boolean, Integer, ForeignKey)
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, relationship, Session

motor = create_engine("sqlite+pysqlite:///banco_de_dados.sqlite", echo=True)


class Base(DeclarativeBase):
    pass


class DatasMixin():
    dta_cadastro = Column(DateTime,
                          server_default=func.now(),
                          nullable=False)
    dta_atualizacao = Column(DateTime,
                             onupdate=func.now(),
                             default=func.now(),
                             nullable=False)


class Categoria(Base):
    __tablename__ = 'tbl_categorias'
    id = Column(Uuid(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    nome = Column(String(256),
                  nullable=False)

    lista_de_produtos = relationship("Produto", back_populates="categoria",
                                     cascade='all, delete-orphan', lazy='selectin')


class Produto(Base, DatasMixin):
    __tablename__ = 'tbl_produtos'
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(256), nullable=False)
    preco = Column(DECIMAL(10, 2), default=0.00)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    Categoria_id = Column(Uuid(as_uuid=True), ForeignKey("tbl_categorias.id"))

    categoria = relationship("Categoria", back_populates="lista_de_produtos")


cat = Categoria()
cat.nome = "Bebidas"

prod = Produto()
prod.nome = "Coca cola zero, 2L"
prod.ativo = True
prod.preco = 9.50
prod.estoque = 100
prod.categoria = cat

with Session(motor) as sessao:
    sessao.add(prod)
    sessao.commit()


cat = Categoria()
cat.nome = "Salgadinho"

prod = Produto()
prod.nome = "Doritos, 600gr"
prod.ativo = True
prod.preco = 12.94
prod.estoque = 0
prod.categoria = cat

with Session(motor) as sessao:
    sessao.add(prod)
    sessao.commit()

with Session(motor) as sessao:
    categorias = sessao.execute(select(Categoria).where(Categoria.nome == "Bebidas")).scalars()
    for categoria in categorias:
        print(f"A categoria{categoria.nome} tem {len(categoria.lista_de_produtos)} produtos")
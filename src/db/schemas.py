# from datetime import datetime, timezone
# from sqlalchemy import TIMESTAMP, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base


# Base = declarative_base()


# class Chats(Base):
#     __tablename__ = "mensajes"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     usuario = Column(String(255), nullable=False)
#     id_sesion = Column(Integer, nullable=False)
#     pregunta = Column(String(255), nullable=False)
#     respuesta = Column(String(255), nullable=False)
#     creado = Column(TIMESTAMP, nullable=False,
#                     default=datetime.now(timezone.utc))


# class Users(Base):
#     __tablename__ = "usuarios"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     nombre = Column(String(128), nullable=False)

# class Sessions(Base):
#     __tablename__ = "sesiones"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     pregunta = Column(String(255), nullable=False)
#     respuesta = Column(String(255), nullable=False)
#     creado = Column(TIMESTAMP, nullable=False,
#                         default=datetime.now(timezone.utc))

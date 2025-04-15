from fastapi import HTTPException
from sqlalchemy import and_


def add_model(db, model):
    try:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="No se pudo agregar a la base de datos: {e}")


def add_models(db, models: list) -> None:
    try:
        db.add_all(models)
        db.commit()

        return None
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="No se pudo agregar a la base de datos: {e}")


def get_model_by_attribute(db, model, att, value):
    try:
        return db.query(model).filter(att == value).first()
    except:
        raise HTTPException(
            status_code=400, detail="No se pudo obtener de la base de datos")


def get_model_by_attributes(db, model, filters: dict):
    try:
        query = db.query(model).filter(
            and_(getattr(model, key) == value for key, value in filters.items()))
        return query.first()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"No se pudo obtener de la base de datos: {e}"
        )


def get_all_models_by_attribute(db, model, att, value):
    try:
        return db.query(model).filter(att == value).all()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"No se pudo obtener de la base de datos: {e}"
        )

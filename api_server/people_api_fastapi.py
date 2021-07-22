"""
A rest API for people using FastAPI
"""

"""
Pydantic schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PersonModel(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    created_timestamp: Optional[datetime]
    email: Optional[str]

    class Config:
        # https://fastapi.tiangolo.com/tutorial/sql-databases/#technical-details-about-orm-mode
        orm_mode = True


class PeopleList(BaseModel):
    people: List[PersonModel]


"""
Database setup

We're using sync sqlalchemy per the FastAPI docs
https://fastapi.tiangolo.com/tutorial/sql-databases/#about-def-vs-async-def

However, it is possible to do async sqlalchemy
https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html
https://stribny.name/blog/fastapi-asyncalchemy/
"""
from uuid import uuid4
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/people.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Person(Base):
    __tablename__ = 'people'

    id = Column(String(32), primary_key=True, index=True, default=lambda: uuid4().hex)
    created_timestamp = Column(DateTime, default=lambda: datetime.utcnow())
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)


def db_get_person(db: Session, person_id: str) -> Optional[Person]:
    return db.query(Person).filter(Person.id == person_id).first()


def db_get_people(db: Session) -> List[Person]:
    return db.query(Person).all()


def db_create_person(db: Session, person: PersonModel) -> Person:
    instance = Person(**person.dict())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def db_update_person(db: Session, id: str, person: PersonModel) -> Optional[Person]:
    db.query(Person).filter(Person.id == id).update(person.dict())
    db.commit()
    return db_get_person(db, id)


class PersonNotFound(Exception):
    pass


def db_delete_person(db: Session, person_id: str) -> None:
    person = db_get_person(db, person_id)
    if not person:
        raise PersonNotFound(f"person not found for id {person_id}")
    db.delete(person)
    db.commit()

"""
FastAPI code below
"""
import uvicorn  # type: ignore
from fastapi import FastAPI, Depends, HTTPException


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/_status')
def status():
    return {'status': 'OK'}


@app.get('/people', response_model=PeopleList)
def people(db: Session = Depends(get_db)):
    return {'people': db_get_people(db)}


@app.post('/people', response_model=PersonModel)
def new_person(person: PersonModel, db: Session = Depends(get_db)):
    return db_create_person(db, person)


@app.get('/people/{id}', response_model=PersonModel)
def person(id: str, db: Session = Depends(get_db)):
    person = db_get_person(db, id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.put('/people/{id}', response_model=PersonModel)
def update_person(id: str, person: PersonModel, db: Session = Depends(get_db)):
    updated_person = db_update_person(db, id, person)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated_person


@app.delete('/people/{id}')
def delete_person(id: str, db: Session = Depends(get_db)):
    try:
        db_delete_person(db, id)
    except PersonNotFound as e:
        raise HTTPException(status_code=404, detail="Person not found")
    return {}


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, port=5000)  # type: ignore

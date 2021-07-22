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
https://stribny.name/blog/fastapi-asyncalchemy/
"""
from uuid import uuid4
from sqlalchemy import select, update, delete, Column, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:////tmp/people.db"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
async_session = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)
Base = declarative_base()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session


class Person(Base):
    __tablename__ = 'people'

    id = Column(String(32), primary_key=True, index=True, default=lambda: uuid4().hex)
    created_timestamp = Column(DateTime, default=lambda: datetime.utcnow())
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)


async def db_get_person(db: AsyncSession, person_id: str) -> Optional[Person]:
    stmt = select(Person).filter(Person.id == person_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()


async def db_get_people(db: AsyncSession) -> List[Person]:
    result = await db.execute(select(Person))
    return result.scalars().all()


async def db_create_person(db: AsyncSession, person: PersonModel) -> Person:
    instance = Person(**person.dict())
    db.add(instance)
    await db.commit()
    return instance


async def db_update_person(db: AsyncSession, person_id: str, person: PersonModel) -> Optional[Person]:
    person_instance = await db_get_person(db, person_id)
    if not person_instance:
        raise PersonNotFound(f"person not found for id {person_id}")
    stmt = update(Person).filter(Person.id == person_id).values(**person.dict())
    await db.execute(stmt)
    await db.commit()
    return await db_get_person(db, person_id)


class PersonNotFound(Exception):
    pass


async def db_delete_person(db: AsyncSession, person_id: str) -> None:
    person = await db_get_person(db, person_id)
    if not person:
        raise PersonNotFound(f"person not found for id {person_id}")
    stmt = delete(Person).filter(Person.id == person_id)
    await db.execute(stmt)
    await db.commit()


"""
FastAPI code below
"""
import uvicorn  # type: ignore
from fastapi import FastAPI, Depends, HTTPException


app = FastAPI()


@app.get('/_status')
async def status():
    return {'status': 'OK'}


@app.get('/people', response_model=PeopleList)
async def people(db: AsyncSession = Depends(get_session)):
    return {'people': await db_get_people(db)}


@app.post('/people', response_model=PersonModel)
async def new_person(person: PersonModel, db: AsyncSession = Depends(get_session)):
    return await db_create_person(db, person)


@app.get('/people/{id}', response_model=PersonModel)
async def person(id: str, db: AsyncSession = Depends(get_session)):
    person = await db_get_person(db, id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.put('/people/{id}', response_model=PersonModel)
async def update_person(id: str, person: PersonModel, db: AsyncSession = Depends(get_session)):
    try:
        updated_person = await db_update_person(db, id, person)
    except PersonNotFound:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated_person


@app.delete('/people/{id}')
async def delete_person(id: str, db: AsyncSession = Depends(get_session)):
    try:
        await db_delete_person(db, id)
    except PersonNotFound as e:
        raise HTTPException(status_code=404, detail="Person not found")
    return {}


import asyncio


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(init_models())
    uvicorn.run(app, port=5000)  # type: ignore

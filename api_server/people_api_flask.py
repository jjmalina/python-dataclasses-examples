"""
A REST API for people using Flask
"""

from flask import Flask


app = Flask(__name__)


"""
API Schemas

We use marshmallow_dataclass because dataclasses-json did not integrate well
and do validation like we want
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

import marshmallow_dataclass


@dataclass
class PersonModel:
    first_name: str
    last_name: str
    created_timestamp: Optional[datetime] = None
    id: Optional[str] = None
    email: Optional[str] = None


PersonSchema = marshmallow_dataclass.class_schema(PersonModel)()

@dataclass
class PeopleModel:
    people: List[PersonModel]


PeopleSchema = marshmallow_dataclass.class_schema(PeopleModel)()


"""
Database
"""
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.ext.declarative import DeclarativeMeta

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/people.db"
db = SQLAlchemy(app)
BaseModel: DeclarativeMeta = db.Model


class Person(BaseModel):  # type: ignore
    __tablename__ = "people"
    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid4().hex)
    created_timestamp = db.Column(db.DateTime, nullable=True, default=lambda: datetime.utcnow())
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)


def db_get_person(id: str) -> Person:
    person = Person.query.get(id)
    if not person:
        raise PersonNotFound(f"person not found with id={id}")
    return person


def db_get_people() -> List[Person]:
    return Person.query.all()


def db_create_person(person: PersonModel) -> Person:
    person = Person(**asdict(person))
    db.session.add(person)
    db.session.commit()
    return person


def db_update_person(id: str, person: PersonModel) -> Person:
    Person.query.filter(Person.id == id).update(asdict(person))
    db.session.commit()
    return db_get_person(id)


class PersonNotFound(Exception):
    pass


def db_delete_person(id: str) -> None:
    person = db_get_person(id)
    db.session.delete(person)
    db.session.commit()


"""
Flask routes
"""
from flask import request, jsonify
from flask_apispec import marshal_with  # type: ignore
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({'errors': e.messages}), 422


@app.errorhandler(IntegrityError)
def handle_integrity_error(e):
    return jsonify({'errors': [str(e)]}), 422


@app.errorhandler(PersonNotFound)
def handle_person_not_found(e):
    return jsonify({'errors': ['Person could not be found']}), 404


@app.route('/_status')
def status():
    return 'OK'


@app.route('/people/<id>', methods=['GET'])
@marshal_with(PersonSchema)
def person(id):
    return db_get_person(id)


@app.route('/people', methods=['GET'])
@marshal_with(PeopleSchema)
def people():
    return dict(people=db_get_people())


@app.route('/people', methods=['POST'])
@marshal_with(PersonSchema)
def new_person():
    data = request.get_json()
    person_data = PersonSchema.load(data)
    person = db_create_person(person_data)
    return person, 201


@app.route('/people/<string:id>', methods=['PUT'])
@marshal_with(PersonSchema)
def update_person(id: str):
    data = request.get_json()
    person_model = PersonSchema.load(data)
    return db_update_person(id, person_model)


@app.route('/people/<string:id>', methods=['DELETE'])
def delete_person(id: str):
    db_delete_person(id)
    return jsonify({}), 204


"""
Automatic documentation
"""
from apispec import APISpec  # type: ignore
from apispec.ext.marshmallow import MarshmallowPlugin  # type: ignore
from flask_apispec.extension import FlaskApiSpec  # type: ignore


app.config.update({
    'APISPEC_SPEC': APISpec(
        title='people',
        version='v1',
        openapi_version='3.0.1',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/docs-api/',
    'APISPEC_SWAGGER_UI_URL': '/docs/',
})
docs = FlaskApiSpec(app)
docs.register(people)
docs.register(person)
docs.register(new_person)
docs.register(update_person)
docs.register(delete_person)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

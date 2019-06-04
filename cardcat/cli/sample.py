"""
    sample.py
    ~~~~~~~~~

    Loads the entire site with fake data, to let us really test the UI
    and flow of everything.
"""
import click
from flask.cli import AppGroup
from cardcat.database import db
from flask import current_app
import os
import random
from datetime import datetime
from cardcat.models import User, Role, Log
import factory
from faker import Faker
import uuid


# Move these factories off to a separate file after hacking about is done:


class UserFactory(factory.Factory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = "password"
    display_name = factory.Faker("name")
    active = True
    confirmed_at = datetime.now()

    class Meta:
        model = User


class LogFactory(factory.Factory):
    vendor = factory.Faker("user_name")
    amount = random.randint(999, 55555)
    card = f"****{random.randint(1000,9999)}"

    class Meta:
        model = Log


sample_cli = AppGroup("sample")


@sample_cli.command("load")
def load():
    click.confirm(
        "This process wipes existing data (if any) and loads with fake data\n"
        "Are you sure?",
        abort=True,
    )

    db.drop_all()
    db.create_all()

    # create roles.

    roles = ["contributor", "author", "editor", "administrator", "owner"]
    for role in roles:
        r = Role(name=role)
        db.session.add(r)
    db.session.commit()
    roles = Role.query.all()

    # create users.

    for x in range(3):
        user = UserFactory.build()
        user.roles = random.sample(roles, 2)
        db.session.add(user)
    db.session.commit()
    users = User.query.all()
    click.echo("Users")
    click.echo("-" * 20)
    for x in users:
        click.echo(x.username)

    # create a few tags to pick from, so we have lots of overlap.

    for x in range(10):
        article = LogFactory()
        article.token = uuid.uuid4().hex
        print(f"Example Token: {article.token}")
        db.session.add(article)
    db.session.commit()

from faker import Faker
from . import db
from .models import User, Groups, CostGroup, Needs, Costs
from sqlalchemy.exc import IntegrityError
fake = Faker()


def populate_db(count=10):


    #create group

    group = Groups('TestGroup')
    db.session.add(group)
    db.session.commit()

    i = 0
    while i < count:

        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password())

        user.confirmed = True
        db.session.add(user)

        try:
            db.session.commit()
            i = i + 1
        except IntegrityError:
            db.session.rollback()

        group_mem = CostGroup(user_id=user.id, group_id=group.id)
        db.session.add(group_mem)
        db.session.commit()

        fake_cost = Costs(cost_title=fake.text(15),
                          spent_money=fake.random_int(0, 100, 2),
                          who_spent=user.id,
                          group_id=group.id)
        db.session.add(fake_cost)
        db.session.commit()

        fake_need = Needs(text=fake.text(40),
                          group_id=group.id,
                          user_id=user.id)
        db.session.add(fake_need)
        db.session.commit()





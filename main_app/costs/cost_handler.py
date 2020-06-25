from main_app.models import Costs, WhoOwesWhom, CostGroup
from functools import reduce
from .. import db


def cost_handle(group_id):

    users = CostGroup.query.filter_by(group_id=group_id).all()
    user_list = []
    for user in users:
        user_list.append(user.user_id)

    result = dict()
    for user_id in user_list:
        user_costs = Costs.query.filter_by(who_spent=user_id, group_id=group_id).all()
        result.update({user_id: cost_sum(user_costs)})

    result = inter_process(result)

    for u in user_list:

        copy_list = user_list.copy()
        copy_list.remove(u)
        for i in copy_list:
            who_whom = WhoOwesWhom.query.filter_by(who=u, whom=i,
                                                   group_id=group_id).first()
            if who_whom is None:
                who_whom = WhoOwesWhom(who=u, whom=i,
                                       group_id=group_id)
                db.session.add(who_whom)
                db.session.commit()
    for d in result:
        who_whom = WhoOwesWhom.query.filter_by(who=d[0], whom=d[1]).first_or_404()
        who_whom.plus_amount(d[2])
        db.session.commit()

    return result


def cost_sum(user_costs):

    result = 0
    for cost in user_costs:
        result += cost.spent_money
    return result


def inter_process(data_dict):
    result_list = []
    debtor = {}
    n_debtor = {}
    total_sum = reduce(lambda a, b: a+b, data_dict.values())
    equal_amt = int(total_sum/len(data_dict))

    for kay, value in data_dict.items():
        if (value-equal_amt) > 0:
            n_debtor.update({kay: value-equal_amt})
        elif (value-equal_amt) != 0:
            debtor.update({kay: value-equal_amt})

    for kay, value in debtor.items():
        temp_dict = {kay: value}
        for kay_n, value_n in n_debtor.items():
            if value_n == 0:
                continue
            temp = value_n + temp_dict.get(kay)
            if temp > 0:
                n_debtor.update({kay_n: temp})
                result_list.append([kay, kay_n, abs(temp_dict.get(kay))])
                break
            elif temp < 0:
                result_list.append([kay, kay_n, abs(value_n)])
                n_debtor.update({kay_n: 0})
                temp_dict.update({kay: temp})

            elif temp == 0:
                result_list.append([kay, kay_n, abs(value)])
                n_debtor.update({kay_n: 0})
                break

    return result_list

from main_app.models import Costs, User
from functools import reduce

def cost_handle(users):

    result = dict()
    for user in users:
        user_costs = Costs.query.filter_by(who_spent=user.id).all()
        result.update({user.id: cost_sum(user_costs)})

    result = inter_process(result)

    return result

def cost_sum(costs):

    result = 0
    for cost in costs:
        result += cost.spent_money
    return result


def inter_process(data_dict):

    total_sum = reduce(lambda a, b: a+b, data_dict.values())
    equal_amt = total_sum/len(data_dict)

#сделать 2 словаря которых. В первом будут должники, второй будет иметь у себя те кому должны и отправить его в cost_handle
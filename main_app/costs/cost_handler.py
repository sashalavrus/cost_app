from main_app.models import Costs
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
    result_list = []
    debtor = {}
    n_debtor = {}
    total_sum = reduce(lambda a, b: a+b, data_dict.values())
    equal_amt = int(total_sum/len(data_dict))

    for kay, value in data_dict.items():
        if (value-equal_amt) >= 0:
            debtor.update({kay: value-equal_amt})
        else:
            n_debtor.update({kay: value-equal_amt})

    for kay, value in debtor.items():
        temp_dict = {kay: value}
        for kay_n, value_n in n_debtor.items():
            if value_n == 0:
                continue
            temp = value_n + temp_dict.values(kay)
            if temp > 0:
                n_debtor.update({kay_n: temp})
                result_list.append([kay, kay_n, abs(temp_dict.values(kay))])

                break
            elif temp < 0:
                result_list.append([kay, kay_n, value_n])
                n_debtor.update({kay_n: 0})
                temp_dict.update({kay: temp})

            elif temp == 0:
                result_list.append([kay, kay_n, value])
                n_debtor.update({kay_n: 0})

    return result_list

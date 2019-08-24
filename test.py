a = [
    {
        "intended_school": 2,
        "intended_school__name": "南山校区",
        "follow_up_person": 4,
        "follow_up_person__nickname": "客服B",
        "clue_num_count": 1,
        "contact_again_count": 0,
        "ordered_visit_count": 0,
        "visit_proportion_count": 0,
        "enroll_proportion_count": 0,
        "fail_count": 0
    },
    {
        "intended_school": 1,
        "intended_school__name": "中山校区",
        "follow_up_person": 3,
        "follow_up_person__nickname": "客服A",
        "clue_num_count": 5,
        "contact_again_count": 4,
        "ordered_visit_count": 3,
        "visit_proportion_count": 2,
        "enroll_proportion_count": 1,
        "fail_count": 0
    },
    {
        "intended_school": 1,
        "intended_school__name": "中山校区",
        "follow_up_person": 5,
        "follow_up_person__nickname": "客服C",
        "clue_num_count": 1,
        "contact_again_count": 0,
        "ordered_visit_count": 0,
        "visit_proportion_count": 0,
        "enroll_proportion_count": 0,
        "fail_count": 0
    }
]
from operator import itemgetter
from itertools import groupby
import time

t1 = time.time()
a.sort(key=itemgetter('intended_school'))

for intended_school, items in groupby(a, key=itemgetter('intended_school', 'intended_school__name')):
    info = dict()
    info['intended_school'] = intended_school[0]
    info['intended_school__name'] = intended_school[1]
    info['data'] = list()
    print(info)
    for i in items:

        del i['intended_school']
        del i['intended_school__name']
        info['data'].append(i)
    print(54, info)
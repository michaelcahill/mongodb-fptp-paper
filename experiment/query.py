from numpy.random import randint
import timeout_decorator
import os
import math
from datetime import datetime
import uuid

from logger import logging_decorator
from save_load import *


# @timeout_decorator.timeout(60)
# @logging_decorator
# def get_query_explain(collection, query):
#     """
#     :param collection:
#     :param query: a mongodb query with selectivity on both field A and B
#     :return: the query explain which shows the winning plan
#     """
#     winning_plan_explain = collection.find(query).explain()['queryPlanner']['winningPlan']
#     return winning_plan_explain


def generate_range_predicate(field_name, min, max):
    offset = randint(0, max - min)
    lower_bound = randint(min, max - offset)
    upper_bound = lower_bound + offset
    return {field_name: {"$gte": lower_bound, "$lte": upper_bound}},\
           lower_bound, \
           upper_bound


@logging_decorator
def generate_query(collection,
                   collection_name,
                   granularity,
                   dataset_size,
                   repetition,
                   query_dir,
                   grid_dir):
    """
    :param collection: the Mongo collection for the experiment
    :param collection_name: the name of the collection
    :param granularity: the dimension (i.e. the height / width) of the grid
    :param dataset_size: the size of the dataset
    :param repetition: the amount of query files need to be generated
    :param query_dir: where to persist generated query files
    :param grid_dir: where to persist the visited grid
    :return:
    """

    a_min = collection.find_one(sort=[("a", 1)])["a"]
    a_max = collection.find_one(sort=[("a", -1)])["a"]
    b_min = collection.find_one(sort=[("b", 1)])["b"]
    b_max = collection.find_one(sort=[("b", -1)])["b"]

    def map_to_index(predicate):
        selectivity = collection.count_documents(predicate) / dataset_size
        return math.floor(selectivity * granularity)

    @logging_decorator
    def generate_query_helper(rep_id):
        visited_grid = [[0 for i in range(granularity)] for j in range(granularity)]
        n_pos = granularity ** 2
        n_pos_visited = 0

        while n_pos_visited < n_pos:
            print("Progress : {:.2f}%".format(float(n_pos_visited / n_pos) * 100))

            # generate a range predict for field B
            while 1:
                b_predicate, b_lower, b_upper = generate_range_predicate(field_name="b", min=b_min, max=b_max)
                b_i = map_to_index(b_predicate)
                print("generating b_i: {}".format(b_i))
                if 0 in visited_grid[b_i]:
                    break

            # generate a range predicate for field A
            while 1:
                a_predicate, a_lower, a_upper = generate_range_predicate(field_name="a", min=a_min, max=a_max)
                a_i = map_to_index(a_predicate)
                print("generated b_i: {}, generating a_i: {}".format(b_i, a_i))
                if visited_grid[b_i][a_i] == 0:
                    break

            # mark pos as visited
            n_pos_visited += 1
            visited_grid[b_i][a_i] = 1
            print("a_i: {}, b_i: {}".format(a_i, b_i))

            # save query
            save_query(os.path.join(query_dir,
                                    collection_name,
                                    "query_{}.txt".format(rep_id)),
                       a_lower, a_upper, b_lower, b_upper, b_i, a_i)
            print("Query saved in: ".format(query_dir))

            # save grid
            save_grid(visited_grid, os.path.join(grid_dir,
                                                 collection_name,
                                                 "visited_grid_{}.txt".format(rep_id)))
            print("Grid saved in: ".format(grid_dir))

            print("=" * 20)
        return

    rep_ctr = 0

    while rep_ctr < repetition:
        # rep_id = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
        rep_id = uuid.uuid4().hex
        generate_query_helper(rep_id)
        rep_ctr += 1
    return

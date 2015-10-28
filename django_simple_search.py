# -*- coding: utf-8 -*-
"""Module created to search a specific term in several fields of a model"""
from itertools import chain
import operator

from django.db.models import Q

__author__ = 'trnsnt'


def search_for_term(model, term, fields, number=10):
    """
    Generic method used to search term on list of fields.
    Return first fields equals to term, then fields starting by the term, and at the end fields containing term
    :param model: Django model class
    :param term: Searched term
    :param fields: Fields to look for
    :param number: Number of wanted response
    :return: List of objects
    """
    searcher = ['iexact', 'istartswith', 'icontains']
    objects = []
    for search in searcher:
        curr_filter = reduce(operator.or_, [Q(('%s__%s' % (field, search), term)) for field in fields])
        # Need to search for number + len(objects) to handle duplicate objects
        objects = uniquify(objects, model.objects.filter(curr_filter)[:number + len(objects)])[:number]
        if len(objects) == number:
            break
    return objects


def uniquify(*queryests):
    """Take several queryset and return list of unique object
    :param queryests: QuerySets we want to uniquify
    """
    seen = set()
    return [x for x in chain(*queryests) if not (x in seen or seen.add(x))]

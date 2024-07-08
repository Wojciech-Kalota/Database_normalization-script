import sys
import os
import copy
import itertools
from itertools import chain


def input_data():
    try:
        if os.stat("tests/test-10.txt").st_size > 3:
            file = open("tests/test-10.txt", "r", encoding='utf-8')
            return file.read().strip().split('\n')

    except FileNotFoundError:
        pass

    print("Enter data (finish with Ctrl-D/Ctrl-Z in a new line):")
    return sys.stdin.read().strip().split('\n')


def canonize(dependencies):
    canonized = []
    for left, right in dependencies:
        for x in right:
            canonized.append([left, [x]])

    return canonized


def remove_element(lst, element):
    return [x for x in lst if x != element]


def powerset(iterable, length=None, result=[]):

    if length is None:
        length = len(iterable)
    if length > 0:
        # listing combinations for given length
        for x in itertools.combinations(iterable, length):
            result.append(list(x))
        powerset(iterable, length-1, result)
    return result


def parse_dependencies(l):

    depends = []

    for x in l:
        left = x[:x.find('-')].strip().split(',')
        right = x[x.find('>')+1:].strip().split(',')
        left = [x.strip() for x in left]
        right = [x.strip() for x in right]
        depend = [left, right]
        depends.append(depend)

    return depends


def find_closure(collection, depends):
    res = collection[:]
    prev_res = []
    # as long as there is a change
    while prev_res != res:
        prev_res = res[:]
        # check for each dependency
        for depend in depends:
            left, right = depend
            # append new attribute
            if set(left).issubset(res):
                res.extend(right)
                res = list(set(res[:]))
    return res


def find_closures(attr, depends):
    # each possible closure
    closures = powerset(attr)
    result = []

    for closure in closures:
        result.append([closure, find_closure(closure, depends)])

    return result


def find_real_keys(keys):

    result = []

    # for each key
    for i, key in enumerate(keys):
        result.append(key)
        for x in keys[i+1:]:
            # check if there is no smaller key
            if set(x).issubset(key):
                result.remove(key)
                break

    return result


def divide_attributes(keys, attributes):
    keys_attributes = list(set(chain.from_iterable(keys)))
    non_key = list(set(attributes) - set(keys_attributes))
    return keys_attributes, non_key


def is_equivalent(f_min, g):

    for x in f_min:
        if not set(x[1]).issubset(find_closure(x[0], g)):
            return False

    for x in g:
        if not set(x[1]).issubset(find_closure(x[0], f_min)):
            return False

    return True


def calculate_min_basis(dependencies):
    f_min = copy.deepcopy(dependencies)
    # Step 3
    for element in copy.deepcopy(f_min):
        x = element[0]
        a = element[1]
        for b in x:
            g = copy.deepcopy(f_min)
            if element in g:
                g.remove(element)
            new_element = [remove_element(x, b), a]
            g.append(new_element)
            if is_equivalent(f_min, g):
                if element in f_min:
                    f_min.remove(element)
                f_min.append(new_element)

    # Step 4
    for element in copy.deepcopy(f_min):
        g = copy.deepcopy(f_min)
        g.remove(element)
        if is_equivalent(f_min, g):
            if element in f_min:
                f_min.remove(element)

    return f_min


def check_2nf(key_attributes, non_key_attributes, dependencies):
    for attribute in key_attributes:
        closure = find_closure([attribute], dependencies)
        for non_key in non_key_attributes:
            if non_key in closure:
                return False

    return True


stream = input_data()

# designating attributes and dependencies
attributes = [x.strip() for x in stream[0].split(',')]
dependencies = canonize(parse_dependencies(stream[1:]))

# verifying data
if sorted(list(set(chain.from_iterable(list(chain.from_iterable(dependencies)))))) != sorted(attributes):
    raise "F isn't a subset of U or vice versa"
else:
    print("All attributes in U are also present in F and vice versa")

# calculating closures
closures = find_closures(attributes, dependencies)
print("\nClosures:")
for x in closures:
    print(f"{set(x[0])}+ = {set(x[1])}")

# finding keys
keys = [closure[0] for closure in closures if (sorted(attributes) == sorted(closure[1]))]
print("\nKey candidates:")
for x in keys:
    print(f"{set(x)}+")

# finding optimal keys
real_keys = find_real_keys(keys)
print("\nKeys:")
for x in real_keys:
    print(f"{set(x)}+")

key_attributes, non_key_attributes = divide_attributes(real_keys, attributes)
print("\nKey attributes:")
print(*key_attributes)

print("\nNon-key attributes:")
print(*non_key_attributes)

f_min = calculate_min_basis(dependencies)
print("\nMin base:")
for x in f_min:
    print(*x[0], "->", *x[1])


is_2nf = check_2nf(key_attributes, non_key_attributes, dependencies)
print("\nIs 2NF?")
print(is_2nf)
print("\nFor a relationship to be in 2NF, it is necessary that each non-key attribute is fully functionally dependent on each key of this relationship.")

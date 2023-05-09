import json
from owlready2 import *
import types


# Reading input data
with open('input.json') as f:
    data = json.load(f)

onto = get_ontology('onto.owl')
with onto:

    # Creating argument sets
    argument_sets = data['argument_sets']
    for argument_set, arguments in argument_sets.items():
        Cl = types.new_class(argument_set, (Thing,))
        for argument, text in arguments.items():
            inst = Cl(argument)
            inst.label = text

    # Asserting attacks relation
    class attacks(ObjectProperty):
        pass

    class isAttackedBy(ObjectProperty):
        inverse_property = attacks
    
    attack_pairs = data['attack_pairs']
    for pair in attack_pairs:
        argument1 = onto[pair[0]]
        argument2 = onto[pair[1]]
        argument1.attacks.append(argument2)

    # Starting reasoning to derive inverse attacks
    sync_reasoner_pellet(infer_property_values = True,
                         debug = 2)

    # Closing world
    for inst in onto.individuals():
        if inst.attacks:
            inst.is_a.append(attacks.only(OneOf(inst.attacks)))
        if inst.isAttackedBy:
            inst.is_a.append(isAttackedBy.only(OneOf(inst.isAttackedBy)))

    # Defining conflict free sets
    for argument_set1 in argument_sets.keys():
        Cl = types.new_class(f'{argument_set1}ConflictFree', (Thing,))
        complement = []
        for argument_set2 in argument_sets.keys():
            if argument_set1 != argument_set2:
                complement.append(onto[argument_set2])
        Cl.equivalent_to.append(onto[argument_set1] & attacks.only(Or(complement)))

    # Defining admissible sets
    for argument_set1 in argument_sets.keys():
        Cl = types.new_class(f'{argument_set1}Admissible', (Thing,))
        Cl.equivalent_to.append(onto[argument_set1] & isAttackedBy.only(isAttackedBy.some(onto[argument_set1])))
        

onto.save('onto.owl', format = 'ntriples')


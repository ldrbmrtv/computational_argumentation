from owlready2 import *


onto = get_ontology('onto.owl').load()
with onto:
    sync_reasoner_pellet(debug = 2)

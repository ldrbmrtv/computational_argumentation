from owlready2 import *

path = 'examples/'
onto_path.append(path)
onto = get_ontology('onto.owl').load()
with onto:
    sync_reasoner_pellet(debug = 2)

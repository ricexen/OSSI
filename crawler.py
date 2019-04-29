import time
from src.api import Facebook
from gephistreamer import graph, streamer
from src.models import FBPerson

fb_api = Facebook()
ws = streamer.GephiWS(workspace='facebook')
stream = streamer.Streamer(ws, auto_commit=True)


me = FBPerson(id='me')
node_me = graph.Node(me.id, **me.row_data())
edges_to_add = 100
nodes_to_add = 100
temp_edges = []
temp_nodes = []


def add_node(person):
    data = person.row_data()
    node = graph.Node(person.id, **data)
    stream.add_node(node)
    return node


def add_edge(source, target):
    s = add_node(source)
    t = add_node(target)
    edge = graph.Edge(s, t)
    stream.add_edge(edge)


def new_known(source, target):
    add_edge(source, target)


stream.add_node(node_me)
me.load_knowns(depth=1, on_known_loaded=new_known)

time.sleep(100000)

from typing import TypedDict
from langgraph.graph import START,END,StateGraph


class MyState(TypedDict):
    a: int
    b: int
    c: int


def input(state:MyState):
    state['a'] = 20
    state['b'] = 30
    return state

def calculate_total(state:MyState):
    state['c'] = state['a'] + state['b']
    return state


graph = StateGraph(MyState)
graph.add_node("node1", input)
graph.add_node("node2", calculate_total)

graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

workflow = graph.compile()

result = workflow.invoke({'a':0, 'b':0, 'c':0})

print(result['c'])




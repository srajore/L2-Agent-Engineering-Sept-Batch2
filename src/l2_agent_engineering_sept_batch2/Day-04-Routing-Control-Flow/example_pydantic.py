"""Session 4: Send a request to one of two graph paths."""

from pydantic import BaseModel, Field
from langgraph.graph import END, START, StateGraph


# Pydantic State with validation
class State(BaseModel):
    request: str = Field(
        min_length=1,
        description="User's support request"
    )

    route: str = Field(
        default="",
        description="Selected support route"
    )

    answer: str = Field(
        default="",
        description="Final response to the user"
    )


def choose_route(state: State):
    """Decide which path should handle the request."""

    if "password" in state.request.lower():
        return {"route": "account"}

    return {"route": "general"}


def next_node(state: State):
    """Return the route selected by choose_route()."""
    
    return state.route


def account_help(state: State):
    return {
        "answer": "Open the password reset page."
    }


def general_help(state: State):
    return {
        "answer": "A support engineer will review the request."
    }


# StateGraph uses our Pydantic State
graph_builder = StateGraph(State)

graph_builder.add_node("choose_route", choose_route)
graph_builder.add_node("account", account_help)
graph_builder.add_node("general", general_help)

graph_builder.add_edge(START, "choose_route")

graph_builder.add_conditional_edges(
    "choose_route",
    next_node
)

graph_builder.add_edge("account", END)
graph_builder.add_edge("general", END)

graph = graph_builder.compile()


result = graph.invoke(
    State(
        request="I account got locked"
    )
)

print(result["answer"])
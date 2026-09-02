from __future__ import annotations
from langgraph.graph import StateGraph,END
from filingsgraph.agents.state import ResearchState
from filingsgraph.agents.planner import plan

def build_research_graph():
    def planning(state:ResearchState):
        p=plan(state['user_question'],state.get('resolved_entities',[]),state.get('target_periods',[])); return {"query_type":p.query_type,"research_plan":p.model_dump(),"retrieval_queries":p.retrieval_queries}
    def complete(state:ResearchState): return state
    g=StateGraph(ResearchState); g.add_node('plan',planning); g.add_node('complete',complete); g.set_entry_point('plan'); g.add_edge('plan','complete'); g.add_edge('complete',END); return g.compile()

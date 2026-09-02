from typing import TypedDict,Any
class ResearchState(TypedDict,total=False):
    query_id:str; user_question:str; resolved_entities:list[str]; query_type:str; target_periods:list[int]
    research_plan:dict; retrieval_queries:list[str]; filing_evidence:list[dict]; financial_facts:list[dict]
    financial_calculations:list[dict]; graph_evidence:list[dict]; temporal_findings:list[dict]; macro_evidence:list[dict]
    contradictory_evidence:list[str]; citations:list[str]; verification_status:dict; retry_count:int; tool_count:int; final_report:str

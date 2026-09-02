from pydantic import BaseModel, Field

class GraphNode(BaseModel):
    node_id: str
    node_type: str
    label: str
    attributes: dict = Field(default_factory=dict)

class GraphEdge(BaseModel):
    edge_id: str
    source_node: str
    target_node: str
    relationship: str
    valid_from: str | None = None
    valid_to: str | None = None
    filing_id: str | None = None
    source_chunk_id: str | None = None
    source_text_span: str | None = None
    extraction_method: str
    confidence: float = Field(ge=0.0, le=1.0)
    attributes: dict = Field(default_factory=dict)

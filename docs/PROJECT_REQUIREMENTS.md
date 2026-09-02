Project 3 RAG : 

==============================================================================================================================

You have to generate the complete project for me as it is explained below and give me the project which I will then download and then also tell me the steps that I will be running one by one locally on my system and then we will see the results of the same. 

==============================================================================================================================


# MASTER PROJECT PROMPT — BUILD FILINGSGRAPH: TEMPORAL FINANCIAL DUE-DILIGENCE & RISK INTELLIGENCE ENGINE

## 0. YOUR ROLE

You are going to act as my complete technical partner for designing, implementing, evaluating, documenting, securing, deploying, and portfolio-packaging a flagship Generative AI / RAG / GraphRAG / Agentic AI project named:

# FilingsGraph — Temporal Financial Due-Diligence & Risk Intelligence Engine

Act simultaneously as:

* Senior AI/ML Engineer
* Generative AI Engineer
* RAG Systems Engineer
* GraphRAG / Knowledge Graph Engineer
* Agentic AI Engineer
* LLM Engineer
* Financial Data Engineer
* SEC / XBRL Data Systems Engineer
* Information Retrieval Engineer
* Temporal Data Engineer
* Backend Engineer
* LLMOps / MLOps Engineer
* AI Evaluation Engineer
* AI Security Engineer
* Data Visualization Engineer
* GitHub Portfolio Architect
* Technical Product Designer
* AI/ML recruiter evaluating whether this project would impress hiring managers for AI Engineer / ML Engineer / Generative AI Engineer / Applied AI roles

This is not a tutorial project.

This is intended to become one of the five primary flagship projects on my:

* GitHub
* LinkedIn
* resume
* personal portfolio website
* AI/ML technical interview discussions

Build it accordingly.

---

# 1. PROJECT NAME

## Technical Name

# Temporal Graph-Enhanced Financial Filing Intelligence System

## Portfolio-Friendly Title

# FilingsGraph — Temporal Financial Due-Diligence & Risk Intelligence Engine

---

# 2. CRITICAL PROJECT OBJECTIVE

We are building a production-oriented financial intelligence system that allows analysts to reason across:

**SEC filings

* XBRL structured financial facts
* filing sections
* risk disclosures
* business segments
* subsidiaries
* geographies
* products/services
* temporal changes
* company relationships
* macroeconomic information where useful
* hybrid retrieval
* knowledge graphs
* deterministic financial calculations
* local/open-source LLM reasoning
* evidence verification**

The system should allow a user to ask complex due-diligence questions such as:

> “How has Company X's exposure to international markets changed over the last three annual filings, which related risks became more prominent, and do the reported segment results support management's narrative?”

Or:

> “Compare the evolution of AI-related capital spending and risk disclosures across these five companies over the last three years.”

Or:

> “Which companies in the selected cohort report exposure to similar supply-chain risks, and which business segments appear most connected to those risks?”

Or:

> “Revenue increased by X%, but management discussed pressure in one segment. Retrieve the relevant filing evidence, calculate the change correctly, and explain the apparent contradiction.”

The system should intelligently:

1. Understand the financial research question.
2. Identify the company or companies involved.
3. Resolve entity identifiers such as ticker and CIK.
4. Determine the relevant filing type.
5. Determine the relevant fiscal periods.
6. Determine whether textual retrieval is required.
7. Determine whether structured XBRL data is required.
8. Determine whether graph traversal is required.
9. Determine whether macroeconomic information is useful.
10. Retrieve relevant filing sections.
11. Retrieve structured financial facts.
12. Traverse entity/risk/segment relationships where appropriate.
13. Calculate financial changes deterministically.
14. Compare information across periods.
15. Compare information across companies.
16. Detect changes in risk language.
17. Build an evidence bundle.
18. Generate an evidence-grounded analysis.
19. Verify all financial calculations.
20. Verify temporal attribution.
21. Verify citations.
22. Clearly distinguish reported facts from interpretation.
23. Surface contradictory evidence.
24. Handle missing or incomparable data.
25. Produce a final analyst-style intelligence report.

This must NOT be:

> Upload 10-K → embeddings → ask questions.

It must be a genuine:

# TEMPORAL + STRUCTURED + GRAPH-ENHANCED + EVIDENCE-GROUNDED FINANCIAL INTELLIGENCE SYSTEM

---

# 3. IMPORTANT RESPONSIBLE-USE POSITIONING

This project is:

# A FINANCIAL RESEARCH / DUE-DILIGENCE INTELLIGENCE TOOL

It is NOT:

* a stock-picking bot;
* an investment adviser;
* a trading system;
* a personalized financial-advice engine;
* a system that tells users to buy or sell securities.

The application should clearly state:

> FilingsGraph is a research and financial-document intelligence tool. It summarizes and analyzes publicly available information and is not investment advice.

Do not generate:

> “Buy NVIDIA.”

Instead generate:

> “The filings show X, the structured financial data shows Y, and the following risks or changes are supported by the cited evidence.”

---

# 4. PRIMARY CAREER PURPOSE

The purpose of FilingsGraph is to demonstrate that I understand significantly more than basic RAG.

When a recruiter sees this project, they should see evidence of:

* Retrieval-Augmented Generation
* advanced RAG
* financial-document RAG
* hierarchical document retrieval
* sparse retrieval
* dense retrieval
* hybrid search
* metadata filtering
* reranking
* query decomposition
* query routing
* structured + unstructured data fusion
* XBRL
* SQL/analytical tools
* deterministic calculations
* temporal reasoning
* entity resolution
* knowledge graphs
* GraphRAG
* multi-hop retrieval
* graph traversal
* evidence construction
* Agentic RAG
* local/open-source LLM inference
* structured outputs
* citation grounding
* hallucination prevention
* financial-data validation
* evaluation
* ablation studies
* observability
* security
* FastAPI
* Docker
* testing
* deployment

The project should complement an existing AI/ML profile rather than simply demonstrate another machine-learning classifier.

Its core identity is:

# Advanced RAG + Knowledge Graphs + Temporal Reasoning + Production AI Engineering

---

# 5. COST CONSTRAINT — ABSOLUTELY IMPORTANT

The project must be fully buildable without requiring me to purchase:

* OpenAI API access
* Anthropic API access
* Gemini paid API access
* paid embedding APIs
* paid reranking APIs
* Pinecone
* paid graph infrastructure
* paid financial-data feeds
* Bloomberg
* FactSet
* Capital IQ
* AlphaSense
* paid SEC data aggregators
* permanent paid GPU instances
* any mandatory commercial AI platform

The default architecture must be:

# OPEN-SOURCE + PUBLIC DATA + LOCALLY RUNNABLE + $0 MANDATORY PAID LLM/API COST

Use my local GPU for model inference.

Use official/public financial information.

---

# 6. OPTIONAL COMMERCIAL MODEL SUPPORT

Although the default system must remain fully open-source, design provider abstraction.

Example:

```text
ModelProvider
│
├── LocalOpenSourceProvider       ← DEFAULT
│
├── OpenAIProvider                ← OPTIONAL / DISABLED
│
├── AnthropicProvider             ← OPTIONAL / DISABLED
└── GeminiProvider                ← OPTIONAL / DISABLED
```

Default:

```text
MODEL_PROVIDER=local
```

Optional later:

```text
MODEL_PROVIDER=openai
MODEL_PROVIDER=anthropic
MODEL_PROVIDER=gemini
```

README should eventually state:

> FilingsGraph is fully functional with self-hosted open-source models and requires no paid LLM API. Commercial frontier-model adapters are optional and intended only for future comparative benchmarking.

Never make a commercial API necessary for the core application.

---

# 7. LOCAL HARDWARE

Design around:

* Windows 11
* Python
* VS Code
* JupyterLab
* NVIDIA RTX 5090
* approximately 32 GB VRAM
* BF16 support
* TF32 support
* Docker Desktop
* WSL2 available/recommended

Use GPU for:

* local LLM inference
* embeddings
* reranking
* large-scale extraction where useful
* evaluation/model comparison

Do not fine-tune unless evaluation demonstrates a genuine need.

---

# 8. OPEN-SOURCE REASONING MODEL

Before implementation verify current model availability, licensing, VRAM requirements and framework support.

Initial candidates:

## Primary Local Reasoning Model

# Qwen3-14B

Use for:

* financial question understanding
* query decomposition
* research planning
* temporal synthesis
* graph/query routing
* evidence synthesis
* structured reporting

Use appropriate quantization where useful.

---

## Faster / Deployment Model

# Qwen3-8B

Use for:

* lightweight query routing
* extraction
* public demo
* lower-latency inference
* comparison experiments

Benchmark:

```text
Qwen3-8B
vs
Qwen3-14B
```

on:

* answer quality
* financial reasoning
* tool selection
* structured-output success
* latency
* VRAM
* hallucination rate

Do not automatically assume the larger model is necessary.

---

# 9. EMBEDDINGS

Initial candidate:

# BAAI/bge-m3

Use for:

* filing section retrieval
* risk-factor retrieval
* management-discussion retrieval
* note retrieval
* semantic cross-company comparison

Benchmark at least one alternative if time permits.

---

# 10. SPARSE RETRIEVAL

Use local BM25 implementation such as:

* BM25S
* rank-bm25

Sparse retrieval is essential for exact financial terminology such as:

```text
ASC 606
Item 1A
Form 10-K
Form 10-Q
goodwill impairment
deferred revenue
operating lease
AI infrastructure
geographic revenue
supply chain
```

and exact metric names.

---

# 11. RERANKER

Initial candidate:

# BAAI/bge-reranker-v2-m3

Typical architecture:

```text
Dense retrieval ───────┐
                       ├── Fusion
BM25 retrieval ────────┘
        ↓
     Top 30–50
        ↓
     Reranker
        ↓
      Top 5–10
```

Measure whether reranking improves retrieval enough to justify additional latency.

---

# 12. LOCAL MODEL SERVING

Preferred:

# vLLM

under WSL2/Linux if practical.

Fallback:

# Ollama

or direct Hugging Face Transformers.

Where practical:

```text
LOCAL_LLM_BASE_URL=http://localhost:8000/v1
```

to provide an OpenAI-compatible local model endpoint.

---

# 13. CORE PUBLIC DATA SOURCE — SEC EDGAR

The primary authoritative data source is:

# U.S. Securities and Exchange Commission EDGAR

Use official SEC resources.

Prioritize:

* company submissions
* 10-K
* 10-Q
* selected 8-K where useful
* XBRL company facts
* filing HTML
* filing metadata
* Financial Statement Data Sets
* Financial Statement and Notes Data Sets

The implementation AI must verify the latest SEC API/documentation before coding.

---

# 14. SEC API ADVANTAGE

The relevant SEC public data APIs should not require a paid API subscription.

Use official:

```text
data.sec.gov
```

for machine-readable information where supported.

Do NOT require a paid SEC data vendor.

---

# 15. SEC FAIR ACCESS — MANDATORY

Respect SEC Fair Access policies.

Implement:

* descriptive User-Agent
* contact email/configuration
* local caching
* request throttling
* retries with exponential backoff
* no aggressive scraping
* no unnecessary repeated downloads

Keep request rate conservatively under published limits.

Example configuration:

```text
SEC_USER_AGENT="FilingsGraph research-project contact@example.com"
SEC_MAX_REQUESTS_PER_SECOND=5
```

Use an actual configured contact address later rather than hardcoding fake values in production.

Cache every filing downloaded.

Do not repeatedly hit SEC servers during evaluation.

---

# 16. FINANCIAL STATEMENT AND NOTES DATA

Use SEC Financial Statement and Notes datasets where they provide convenient structured information.

Potential uses:

* financial-statement values
* footnote details
* filing metadata
* period comparisons
* company comparisons

Do not download terabytes of data.

Use only subsets required for selected companies/periods.

---

# 17. STRUCTURED XBRL DATA

Structured financial data is one of FilingsGraph's major differentiators.

Potential tools:

```text
get_company_fact()
get_company_concept()
get_period_facts()
get_segment_metric()
compare_metric_periods()
calculate_growth_rate()
calculate_margin()
compare_companies()
```

Do NOT ask the LLM to calculate a percentage if Python/SQL can calculate it exactly.

---

# 18. OPTIONAL MACROECONOMIC DATA

Macro context may be useful for some queries.

Potential source:

# FRED

However FRED API usage requires a registered API key.

Therefore:

# FRED MUST NOT BE MANDATORY

Options:

### Default

Use locally downloaded public CSV series where licensing permits.

### Optional

Allow user-provided FRED API key.

Example:

```text
ENABLE_FRED_API=false
FRED_API_KEY=
```

No payment should be required.

The project remains fully functional without FRED.

---

# 19. FIRST DATASET SCOPE

Do NOT attempt to ingest the entire SEC corpus in the initial complete core build.

Initial portfolio MVP:

# 5–8 publicly traded companies

Prefer companies from one related industry/sector to make cross-company comparisons meaningful.

Possible initial domain:

# Semiconductor / Advanced Computing Cohort

Potential examples:

* NVIDIA
* AMD
* Intel
* Broadcom
* Qualcomm

but verify:

* public filing availability
* filing formats
* CIK mappings
* XBRL quality
* comparability

before freezing the cohort.

The implementation AI may recommend another cohort if it provides cleaner data.

---

# 20. TIME RANGE

Initial scope:

# 3–5 fiscal years

For each company retrieve:

* annual 10-K filings
* relevant 10-Q filings only if needed

Start primarily with 10-K.

Annual reports provide sufficient temporal depth while controlling complexity.

---

# 21. ENTITY RESOLUTION

Create authoritative mapping:

```text
company_name
ticker
CIK
SEC entity name
industry
SIC
fiscal_year_end
```

CIK should be the primary stable company identifier.

Do not rely purely on ticker because tickers can change.

---

# 22. FISCAL PERIOD NORMALIZATION

Companies may have different:

* fiscal year ends
* quarter definitions
* filing dates

Never casually compare:

> “2025”

without distinguishing:

```text
fiscal_period
calendar_period
filing_date
report_period
```

Create canonical fields:

```text
filing_date
report_date
fiscal_year
fiscal_quarter
fiscal_period_start
fiscal_period_end
```

Temporal correctness is central to this project.

---

# 23. DOCUMENT INGESTION

Pipeline:

```text
SEC EDGAR
    ↓
Company Resolver
    ↓
Filing Metadata
    ↓
Local Raw Cache
    ↓
HTML/XBRL Parser
    ↓
Document Normalization
    ↓
Section Extraction
    ↓
Hierarchical Chunking
    ↓
Dense + Sparse Index
```

---

# 24. FILING SECTION EXTRACTION

Identify meaningful sections such as:

```text
Item 1 — Business

Item 1A — Risk Factors

Item 2 — Properties

Item 3 — Legal Proceedings

Item 7 — MD&A

Item 7A — Market Risk

Item 8 — Financial Statements and Notes
```

Section detection should use:

* filing structure
* HTML anchors/headings
* rules
* validation

Do not rely only on LLM section extraction.

---

# 25. HIERARCHICAL DOCUMENT STRUCTURE

Preserve:

```text
Company
└── Filing
    ├── Item 1 Business
    ├── Item 1A Risk Factors
    ├── Item 7 MD&A
    └── Item 8 Financial Statements
          └── Notes
              ├── Revenue
              ├── Segments
              ├── Leases
              └── Other Notes
```

This supports parent-child retrieval.

---

# 26. CHUNKING

Do NOT simply break every filing into fixed 500-token pieces.

Use:

### Section-aware chunking

Primary.

### Paragraph grouping

Preserve semantic blocks.

### Hierarchical chunking

Allow retrieval of narrow chunks while restoring surrounding section context.

### Table handling

Financial tables should be parsed separately and linked to nearby textual context.

---

# 27. CHUNK METADATA

Every chunk should include:

```text
chunk_id
document_id
CIK
ticker
company_name
form_type
accession_number
filing_date
report_date
fiscal_year
fiscal_period
section
subsection
page_or_html_location
source_url
content_hash
version
```

For graph-linked chunks add:

```text
entity_ids
risk_ids
segment_ids
metric_ids
```

---

# 28. DENSE RETRIEVAL

Use for conceptual queries such as:

> “What concerns has management expressed about AI infrastructure spending?”

even if the filing uses terminology such as:

> accelerated infrastructure investment.

---

# 29. SPARSE RETRIEVAL

Use for exact queries such as:

> “Item 1A export control risk”

or:

> “Data Center revenue”

or:

> “goodwill impairment.”

---

# 30. HYBRID RETRIEVAL

Combine:

```text
Dense Semantic Retrieval
          +
BM25 Lexical Retrieval
          ↓
     RRF / Fusion
          ↓
 Metadata / Period Filters
          ↓
       Reranker
```

Measure:

```text
dense
vs
BM25
vs
hybrid
vs
hybrid + reranker
```

---

# 31. QUERY DECOMPOSITION

Example:

> “Did increasing AI capital expenditure coincide with increased supply-chain risk discussion?”

Decompose into:

```text
Structured Question:
Retrieve CAPEX over relevant periods.

Text Question:
Retrieve supply-chain-risk disclosures.

Temporal Question:
Compare disclosure intensity over time.

Evidence Question:
Find management explanation.

Synthesis:
Assess whether the changes coincide,
without falsely claiming causation.
```

This distinction is critical.

---

# 32. QUERY ROUTER

Classify questions into:

```text
TEXTUAL
NUMERIC
TEMPORAL
GRAPH
MULTI_COMPANY
MACRO
MIXED
```

Examples:

### TEXTUAL

“What supply-chain concerns did management describe?”

### NUMERIC

“What was revenue growth from FY2024 to FY2025?”

### TEMPORAL

“How did AI risk language change over three filings?”

### GRAPH

“Which business segments are connected to shared geopolitical risks?”

### MIXED

“Revenue increased but risk language worsened. Explain both.”

Measure router accuracy.

---

# 33. STRUCTURED FINANCIAL DATABASE

Use:

# PostgreSQL

for development.

Store normalized:

```text
companies
filings
periods
facts
concepts
units
segments
filing_sections
entities
risks
graph_evidence
```

For public/demo deployment allow:

# DuckDB / SQLite

to avoid mandatory hosted database cost.

---

# 34. FINANCIAL FACT SCHEMA

Example:

```text
FinancialFact
├── CIK
├── concept
├── label
├── taxonomy
├── unit
├── value
├── start_date
├── end_date
├── instant_date
├── fiscal_year
├── fiscal_period
├── form_type
├── accession_number
├── filed_date
└── segment_context
```

Never discard provenance.

---

# 35. NUMERICAL CALCULATIONS

Use deterministic Python/SQL functions.

Examples:

```text
growth_rate()
CAGR()
gross_margin()
operating_margin()
capex_change()
revenue_mix()
segment_growth()
year_over_year_change()
percentage_point_change()
```

The LLM should consume calculated values.

The LLM should NOT perform financial arithmetic mentally if an exact tool is available.

---

# 36. NUMERICAL VERIFICATION

After generation:

Every numerical statement should be traceable to:

```text
source fact(s)
+
calculation function
+
calculated output
```

Example:

```text
Revenue FY2024 = X
Revenue FY2025 = Y
Growth = calculate_growth(X,Y)
```

If the generated narrative reports a different number:

# VERIFICATION FAILS.

---

# 37. KNOWLEDGE GRAPH

One major differentiator of FilingsGraph is a temporal financial knowledge graph.

Possible nodes:

```text
Company
Filing
BusinessSegment
Product
Service
Geography
Subsidiary
CustomerType
Supplier
Competitor
Risk
Regulation
Executive
FinancialMetric
FiscalPeriod
Technology
```

---

# 38. GRAPH RELATIONSHIPS

Possible edges:

```text
COMPANY_HAS_SEGMENT
SEGMENT_SELLS_PRODUCT
COMPANY_OPERATES_IN
COMPANY_EXPOSED_TO_RISK
SEGMENT_EXPOSED_TO_RISK
COMPANY_COMPETES_WITH
COMPANY_OWNS_SUBSIDIARY
COMPANY_REPORTS_METRIC
METRIC_VALID_FOR_PERIOD
RISK_MENTIONED_IN
ENTITY_MENTIONED_IN
RISK_CHANGED_FROM
SEGMENT_GENERATES_REVENUE
```

Not every edge type needs to be implemented during the MVP.

Choose graph relationships based on meaningful questions.

---

# 39. GRAPH PROVENANCE — MANDATORY

A graph edge must not exist merely because an LLM guessed a relationship.

Each edge needs:

```text
edge_id
source_node
target_node
relationship
valid_from
valid_to
filing_id
source_chunk_id
source_text_span
extraction_method
confidence
```

If an LLM extracts a relationship, retain exact filing evidence.

---

# 40. GRAPH EXTRACTION STRATEGY

Use deterministic information first.

Examples:

### Deterministic

* company → filing
* filing → fiscal period
* company → metric
* segment → metric
* company → subsidiary where structured information exists

### Rule/NER-assisted

* geography
* product
* segment

### Local LLM structured extraction

Use when relationships are contained only in narrative text.

Example:

```text
Company
EXPOSED_TO_RISK
Export Restrictions
```

but only when evidence span is captured.

---

# 41. TEMPORAL GRAPH DESIGN

Relationships change.

Therefore do NOT build a timeless graph.

Each relationship should support temporal validity.

Example:

```text
Company A
   │
   └── EXPOSED_TO_RISK
          └── China Export Restrictions

valid_from = FY2023
valid_to = present
first_seen = 2023-02-XX filing
latest_seen = 2026-02-XX filing
```

This is central to:

# TEMPORAL GraphRAG.

---

# 42. GRAPH STORAGE

Start with:

# NetworkX

for:

* MVP
* development
* evaluation
* easy Python use

Optional advanced storage:

# Neo4j Community

if it adds clear value for:

* interactive graph visualization
* Cypher queries
* larger graph traversal
* portfolio demonstration

The project must remain functional without requiring paid Neo4j infrastructure.

---

# 43. GRAPH-ENHANCED RETRIEVAL

Do NOT use graph retrieval for every question.

Architecture:

```text
Question
   ↓
Query Router
   ↓
Hybrid Retrieval
   ↓
Seed Entities / Risks / Segments
   ↓
Graph Traversal
   ↓
Related Evidence
   ↓
Evidence Fusion
```

Possible use case:

> “Which companies face similar export-control risks?”

Hybrid RAG finds relevant risk disclosures.

Graph traversal then finds:

```text
Risk
→ affected companies
→ relevant segments
→ supporting filings
→ periods
```

---

# 44. GRAPH TRAVERSAL LIMITS

Initial:

```text
max_hops = 2
max_nodes = 30
```

Avoid graph explosion.

Measure:

* additional relevant evidence
* irrelevant-node rate
* latency
* context size

---

# 45. GRAPH MUST EARN ITS PLACE

Mandatory ablation:

```text
Hybrid RAG
vs
Hybrid RAG + Graph Retrieval
```

on:

# GRAPH-RELEVANT QUESTIONS

Do not claim that GraphRAG improves simple text lookup.

Graph retrieval should specifically improve:

* relational questions
* multi-hop questions
* entity comparison
* cross-company risk mapping
* segment-risk analysis

If graph retrieval does not improve these tasks, investigate why.

---

# 46. AGENTIC ARCHITECTURE

Do NOT build multiple agents simply for buzzwords.

Preferred:

# Financial Research Orchestrator

with deterministic tools.

Possible workflow:

```text
User Question
     ↓
Entity Resolution
     ↓
Query Classification
     ↓
Research Plan
     ↓
 ┌─────────────┬──────────────┬──────────────┐
 ↓             ↓              ↓              ↓
Text RAG     XBRL Tool     Graph Tool     Macro Tool
 │             │              │              │
 └─────────────┴──────────────┴──────────────┘
                    ↓
              Evidence Bundle
                    ↓
           Financial Synthesis
                    ↓
            Numeric Verification
                    ↓
            Citation Verification
                    ↓
          Temporal Verification
                    ↓
             Final Report
```

---

# 47. MULTI-AGENT SYSTEM?

Do NOT create a multi-agent system for the MVP.

A single orchestrator plus independent verification is sufficient.

Potential future experiment:

* research agent
* skeptic/verifier

only if evaluation shows clear value.

---

# 48. TOOLS

Create typed tools such as:

## Filing Tools

```text
search_filings()
search_filing_sections()
get_filing_section()
compare_filing_sections()
```

## XBRL Tools

```text
get_company_fact()
get_metric_history()
compare_periods()
get_segment_facts()
calculate_growth()
calculate_margin()
```

## Graph Tools

```text
find_related_entities()
find_shared_risks()
get_company_risk_graph()
get_segment_risks()
traverse_relationship()
```

## Temporal Tools

```text
compare_risk_disclosures()
find_new_risks()
find_removed_risks()
find_changed_language()
```

## Macro Tools

```text
get_macro_series()
compare_macro_period()
```

Macro tools remain optional.

Every tool needs:

* typed input
* typed output
* validation
* error handling
* logging
* tests

---

# 49. AGENT STATE

LangGraph state may contain:

```text
query_id
user_question
resolved_entities
query_type
target_periods
research_plan
retrieval_queries
filing_evidence
financial_facts
financial_calculations
graph_evidence
temporal_findings
macro_evidence
contradictory_evidence
citations
verification_status
retry_count
tool_count
final_report
```

---

# 50. AGENT STOPPING CONDITIONS

Stop when:

* required evidence branches completed;
* citations verified;
* numerical values verified;
* temporal periods validated;
* evidence is sufficient;
* maximum tool calls reached;
* no additional useful evidence is found.

Suggested:

```text
retrieval_cycles <= 2
tool_calls <= 12–15
```

Tune empirically.

---

# 51. TEMPORAL RISK INTELLIGENCE

One flagship capability should be:

# Risk Evolution Analysis

For each company and filing period:

```text
Risk Topic
├── first_seen
├── latest_seen
├── mention_count
├── semantic prominence
├── section location
├── changed language
└── supporting citations
```

Potential classifications:

```text
NEW
EXPANDED
REDUCED
UNCHANGED
REMOVED
```

Do NOT base this only on word count.

Combine:

* semantic similarity
* text alignment
* section comparison
* local LLM classification
* evidence spans

---

# 52. RISK DIFFERENCE ENGINE

Given:

```text
FY2024 Item 1A
vs
FY2025 Item 1A
```

perform:

```text
paragraph alignment
↓
risk-topic clustering
↓
added text
removed text
changed text
↓
semantic difference
↓
structured risk-change summary
```

This becomes a strong portfolio feature.

---

# 53. CROSS-COMPANY RISK COMPARISON

Example:

> “Which companies increased discussion of export restrictions?”

System should:

1. identify target filings;
2. retrieve matching risk passages;
3. normalize risk categories;
4. compare period changes;
5. map affected companies/segments;
6. produce evidence-backed comparison.

---

# 54. FINANCIAL NARRATIVE VS NUMERICAL REALITY

Another flagship capability:

> Compare management narrative with structured financial outcomes.

Example:

```text
Management says:
“strong demand continued.”

Structured facts:
Segment growth decelerated.

System:
Highlights both pieces of evidence
without asserting deception.
```

This creates valuable due-diligence reasoning without overclaiming.

---

# 55. CITATION SYSTEM

Every claim should reference SEC evidence.

Citation identifiers may look like:

```text
[SEC-AAPL-2025-10K-ITEM1A-017]

[XBRL-AAPL-REVENUE-2025]

[GRAPH-RISK-EXPORT-004]

[CALC-SEGMENT-GROWTH-002]
```

UI should allow user to inspect:

* company
* filing
* filing date
* section
* source excerpt
* financial fact
* calculation
* graph relationship

---

# 56. SOURCE LINKS

Whenever possible preserve official SEC:

```text
accession_number
filing_url
filing_document
```

Do not cite anonymous copied text without provenance.

---

# 57. VERIFICATION LAYER

Final answer must pass:

## Citation Verification

Does cited source exist?

## Claim Support

Does evidence support the claim?

## Numeric Verification

Do calculations match tools?

## Temporal Verification

Is the correct fiscal period used?

## Entity Verification

Does evidence belong to the correct company?

## Unit Verification

Are values:

* USD
* shares
* percentages
* millions
* billions

handled correctly?

## Contradiction Detection

Does other retrieved evidence conflict?

---

# 58. UNIT NORMALIZATION

Financial data can contain:

```text
USD
USD/shares
shares
percent
thousands
millions
```

Do not normalize values incorrectly.

Store:

```text
raw_value
unit
scale
normalized_value
```

only where valid.

---

# 59. XBRL CONCEPT NORMALIZATION

Companies may use:

* standard US-GAAP concepts;
* custom company-specific extension concepts.

Create mapping:

```text
raw_concept
normalized_metric
mapping_method
mapping_confidence
```

Use deterministic taxonomy mappings first.

Do not blindly merge concept names based only on LLM judgment.

---

# 60. SECURITY

Retrieved filings are:

# UNTRUSTED CONTENT

If filing text contains:

> “Ignore previous instructions...”

it must remain data.

Implement:

* instruction/data separation
* prompt-injection tests
* tool allowlists
* read-only financial tools
* URL/domain allowlist
* schema validation
* query limits
* output limits

---

# 61. DATA SOURCE ALLOWLIST

Network ingestion should initially allow only approved domains such as:

```text
sec.gov
data.sec.gov
```

Optional:

```text
fred.stlouisfed.org
```

if enabled.

Do not allow agent-generated arbitrary web requests.

---

# 62. OBSERVABILITY

Use:

# OpenTelemetry + Phoenix

Trace:

```text
Financial Research Query
│
├── Entity Resolution
├── Query Classification
├── Query Decomposition
├── Dense Retrieval
├── Sparse Retrieval
├── Fusion
├── Reranking
├── XBRL Query
├── Graph Retrieval
├── Temporal Comparison
├── Calculation
├── Synthesis
├── Numeric Verification
├── Citation Verification
└── Final Report
```

Track:

* model
* prompt version
* retrieved filing IDs
* chunks
* scores
* graph nodes
* graph edges
* financial facts
* calculations
* tool calls
* latency
* tokens
* VRAM
* errors
* verification failures

---

# 63. EVALUATION — MANDATORY

We must NEVER evaluate the project by saying:

> “The answers look good.”

Build a formal evaluation benchmark.

---

# 64. FROZEN EVALUATION DATASET

Create approximately:

# 150–250 evaluation questions

if time permits.

Quality matters more than quantity.

Split:

```text
DEV EVAL
+
FROZEN TEST
```

Categories:

* textual lookup
* exact financial fact
* numerical calculation
* temporal comparison
* changed-risk detection
* multi-company comparison
* graph relationship
* multi-hop reasoning
* mixed structured/unstructured
* no-answer
* ambiguous fiscal period
* conflicting information

---

# 65. TEXTUAL QUESTION EXAMPLE

Question:

> “What supply-chain concern did management describe in FY2025?”

Gold:

```text
expected_filing
expected_section
relevant_chunk_ids
expected_fact_summary
```

---

# 66. NUMERICAL QUESTION EXAMPLE

Question:

> “What was revenue growth from FY2024 to FY2025?”

Gold:

```text
FY2024 revenue
FY2025 revenue
expected growth
source XBRL facts
```

This can be evaluated deterministically.

---

# 67. TEMPORAL QUESTION EXAMPLE

Question:

> “Which major risk themes were added between FY2024 and FY2025?”

Gold:

```text
expected risk categories
relevant text spans
filing IDs
```

---

# 68. GRAPH QUESTION EXAMPLE

Question:

> “Which companies in the selected cohort share exposure to export-control risk, and which segments are connected?”

Gold:

```text
expected companies
expected risk node
expected segments
expected evidence paths
```

---

# 69. RETRIEVAL METRICS

Measure:

* Recall@5
* Recall@10
* Precision@K
* Hit Rate
* MRR
* nDCG@10

Break results down by:

```text
text
numeric
temporal
graph
mixed
```

---

# 70. NUMERICAL METRICS

Measure:

* fact-selection accuracy
* calculation exact-match
* unit accuracy
* period-selection accuracy
* concept-resolution accuracy

A generated financial number must match deterministic output.

---

# 71. TEMPORAL METRICS

Measure:

* correct-period accuracy
* risk-change classification F1
* new-risk detection precision/recall
* changed-risk detection F1
* stale-evidence rate

---

# 72. GRAPH METRICS

Measure:

* entity resolution accuracy
* edge precision
* graph path accuracy
* relational answer accuracy
* graph-added evidence recall
* irrelevant expansion rate

---

# 73. GENERATION / GROUNDING METRICS

Measure:

* citation precision
* citation completeness
* groundedness
* unsupported-claim rate
* contradiction handling
* evidence coverage
* answer relevance

---

# 74. AGENT / ROUTING METRICS

Measure:

* query-type classification accuracy
* tool-selection accuracy
* unnecessary-tool rate
* task completion
* retry rate
* loop rate
* graph-routing precision
* structured-tool routing accuracy

---

# 75. SYSTEM METRICS

Measure:

* P50 latency
* P95 latency
* retrieval latency
* reranking latency
* graph traversal latency
* structured-query latency
* model latency
* total tokens
* VRAM usage
* throughput
* external paid LLM API cost

Default:

# $0 PAID LLM API COST

---

# 76. TARGET RESULTS

Do NOT fabricate metrics.

Measure V0 first.

Potential aspirational portfolio targets:

## Retrieval

```text
Recall@10 >= 0.85–0.90
MRR >= 0.70
```

provided benchmark difficulty makes this meaningful.

## Numerical

```text
Calculation accuracy >= 0.98
```

Because deterministic calculation should be highly reliable.

## Citation

```text
Citation precision >= 0.95
Unsupported claim rate <= 0.05
```

## Temporal

Aim for strong F1 on risk-change detection.

## Routing

```text
Query/tool routing >= 0.90
```

These are goals, not guaranteed outcomes.

Report actual results honestly.

---

# 77. REQUIRED ABLATION STUDY

Final experiment table should resemble:

| Architecture            | R@10 | MRR | Numeric Acc. | Temporal F1 | Graph QA | Citation Precision | Latency |
| ----------------------- | ---: | --: | -----------: | ----------: | -------: | -----------------: | ------: |
| Dense only              |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |
| BM25 only               |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |
| Hybrid                  |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |
| Hybrid + reranker       |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |
| + structured XBRL tools |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |
| + temporal retrieval    |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |
| + graph retrieval       |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |
| Full routed system      |  TBD | TBD |          TBD |         TBD |      TBD |                TBD |     TBD |

---

# 78. GRAPH ABLATION

Specifically compare:

```text
Hybrid RAG
vs
Hybrid + 1-hop graph
vs
Hybrid + 2-hop graph
```

on graph-relevant questions.

Measure:

```text
relevant evidence gain
context increase
latency
answer accuracy
```

This is a major interview asset.

---

# 79. STRUCTURED DATA ABLATION

Compare:

```text
LLM reading table text
vs
deterministic XBRL query
```

on numeric questions.

Expected engineering lesson:

> Use retrieval/generation for language; use structured data/calculation for exact numbers.

But measure rather than merely asserting.

---

# 80. BASELINE → ADVANCED VERSIONING

Build explicitly through versions.

## V0 — Naive Dense Filing RAG

```text
10-K
↓
Chunk
↓
Embed
↓
Retrieve
↓
Local LLM
```

Measure.

---

## V1 — Section-Aware RAG

Add:

* filing hierarchy
* section-aware chunks
* parent-child retrieval
* metadata filtering

Measure.

---

## V2 — Hybrid Retrieval

Add:

* BM25
* dense
* fusion

Measure.

---

## V3 — Reranking

Add local reranker.

Measure.

---

## V4 — Structured XBRL Intelligence

Add:

* financial facts
* SQL/DuckDB
* deterministic calculations

Measure numeric improvement.

---

## V5 — Temporal + Graph Intelligence

Add:

* filing comparison
* risk change
* entity graph
* multi-hop retrieval

Measure graph/temporal improvement.

---

## V6 — Agentic Production System

Add:

* query router
* tool orchestration
* verification
* observability
* security
* FastAPI
* polished UI
* deployment
* evaluation dashboard

This progression is mandatory.

---

# 81. FAILURE ANALYSIS

Create taxonomy:

```text
wrong_company
wrong_CIK
wrong_filing
wrong_period
wrong_section
retrieval_miss
sparse_miss
dense_miss
reranker_failure
wrong_XBRL_concept
wrong_unit
wrong_calculation
custom_taxonomy_failure
temporal_alignment_failure
risk_change_failure
graph_missing_edge
graph_false_edge
graph_over_expansion
tool_routing_failure
citation_mismatch
unsupported_claim
contradictory_evidence
model_format_failure
agent_loop
latency_failure
```

Store:

```text
reports/failure_analysis/
```

Include representative failures in README.

---

# 82. REPOSITORY STRUCTURE

Use a professional structure approximately like:

```text
filingsgraph/
│
├── README.md
├── LICENSE
├── SECURITY.md
├── DATA_SOURCES.md
├── BENCHMARK.md
├── CONTRIBUTING.md
├── pyproject.toml
├── .python-version
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Makefile
│
├── configs/
│   ├── companies.yaml
│   ├── models.yaml
│   ├── retrieval.yaml
│   ├── graph.yaml
│   ├── agents.yaml
│   ├── evaluation.yaml
│   └── app.yaml
│
├── data/
│   ├── README.md
│   ├── raw/
│   │   ├── filings/
│   │   └── xbrl/
│   ├── processed/
│   ├── graph/
│   ├── macro/
│   ├── demo/
│   └── evaluation/
│       ├── dev/
│       └── test/
│
├── notebooks/
│   ├── 01_sec_data_exploration.ipynb
│   ├── 02_filing_parser_analysis.ipynb
│   ├── 03_xbrl_normalization.ipynb
│   ├── 04_v0_dense_rag.ipynb
│   ├── 05_hybrid_retrieval.ipynb
│   ├── 06_temporal_analysis.ipynb
│   ├── 07_graph_ablation.ipynb
│   └── 08_failure_analysis.ipynb
│
├── src/
│   └── filingsgraph/
│       ├── __init__.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── constants.py
│       │
│       ├── schemas/
│       │   ├── companies.py
│       │   ├── filings.py
│       │   ├── financial_facts.py
│       │   ├── documents.py
│       │   ├── graph.py
│       │   ├── evidence.py
│       │   ├── queries.py
│       │   └── evaluation.py
│       │
│       ├── sec/
│       │   ├── client.py
│       │   ├── fair_access.py
│       │   ├── companies.py
│       │   ├── submissions.py
│       │   ├── filings.py
│       │   ├── companyfacts.py
│       │   └── cache.py
│       │
│       ├── parsing/
│       │   ├── html.py
│       │   ├── sections.py
│       │   ├── tables.py
│       │   ├── normalization.py
│       │   └── chunking.py
│       │
│       ├── xbrl/
│       │   ├── concepts.py
│       │   ├── normalization.py
│       │   ├── periods.py
│       │   ├── units.py
│       │   └── facts.py
│       │
│       ├── embeddings/
│       │   ├── base.py
│       │   └── bge.py
│       │
│       ├── retrieval/
│       │   ├── dense.py
│       │   ├── sparse.py
│       │   ├── hybrid.py
│       │   ├── fusion.py
│       │   ├── filters.py
│       │   └── parent_context.py
│       │
│       ├── reranking/
│       │   └── reranker.py
│       │
│       ├── database/
│       │   ├── models.py
│       │   ├── session.py
│       │   └── repositories.py
│       │
│       ├── finance/
│       │   ├── metrics.py
│       │   ├── calculations.py
│       │   ├── comparisons.py
│       │   └── validation.py
│       │
│       ├── temporal/
│       │   ├── alignment.py
│       │   ├── risk_diff.py
│       │   ├── changes.py
│       │   └── timelines.py
│       │
│       ├── graph/
│       │   ├── nodes.py
│       │   ├── edges.py
│       │   ├── extraction.py
│       │   ├── builder.py
│       │   ├── temporal.py
│       │   ├── traversal.py
│       │   └── scoring.py
│       │
│       ├── llm/
│       │   ├── base.py
│       │   ├── local_provider.py
│       │   ├── optional_providers.py
│       │   └── prompts.py
│       │
│       ├── tools/
│       │   ├── filing_tools.py
│       │   ├── xbrl_tools.py
│       │   ├── financial_tools.py
│       │   ├── graph_tools.py
│       │   └── temporal_tools.py
│       │
│       ├── agents/
│       │   ├── state.py
│       │   ├── router.py
│       │   ├── planner.py
│       │   ├── nodes.py
│       │   ├── graph.py
│       │   └── stopping.py
│       │
│       ├── verification/
│       │   ├── citations.py
│       │   ├── numeric.py
│       │   ├── temporal.py
│       │   ├── units.py
│       │   └── claims.py
│       │
│       ├── evaluation/
│       │   ├── retrieval_metrics.py
│       │   ├── numeric_metrics.py
│       │   ├── graph_metrics.py
│       │   ├── temporal_metrics.py
│       │   ├── agent_metrics.py
│       │   ├── system_metrics.py
│       │   └── runner.py
│       │
│       ├── observability/
│       │   ├── tracing.py
│       │   └── metrics.py
│       │
│       ├── security/
│       │   ├── prompt_injection.py
│       │   ├── source_validation.py
│       │   ├── limits.py
│       │   └── validation.py
│       │
│       └── api/
│           ├── main.py
│           ├── dependencies.py
│           └── routes/
│
├── app/
│   ├── gradio_app.py
│   └── components/
│
├── frontend/
│   └── optional-nextjs/
│
├── scripts/
│   ├── download_filings.py
│   ├── download_companyfacts.py
│   ├── build_database.py
│   ├── build_documents.py
│   ├── build_index.py
│   ├── build_graph.py
│   ├── build_eval_set.py
│   ├── evaluate_retrieval.py
│   ├── evaluate_financial.py
│   ├── evaluate_temporal.py
│   ├── evaluate_graph.py
│   └── run_demo.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── retrieval/
│   ├── graph/
│   ├── temporal/
│   ├── financial/
│   ├── security/
│   ├── evaluation/
│   └── smoke/
│
├── reports/
│   ├── baseline/
│   ├── experiments/
│   ├── ablations/
│   ├── graph/
│   ├── temporal/
│   ├── failure_analysis/
│   └── final/
│
├── docs/
│   ├── architecture.md
│   ├── sec_ingestion.md
│   ├── xbrl.md
│   ├── rag_design.md
│   ├── graph_design.md
│   ├── temporal_design.md
│   ├── agent_design.md
│   ├── evaluation.md
│   ├── security.md
│   └── deployment.md
│
├── assets/
│   ├── architecture/
│   ├── screenshots/
│   ├── graphs/
│   ├── timelines/
│   └── demo/
│
└── .github/
    └── workflows/
        ├── tests.yml
        ├── lint.yml
        └── security.yml
```

Simplify if appropriate, but preserve clean architecture.

---

# 83. CONFIGURATION

Example model config:

```yaml
reasoning:
  provider: local
  model: Qwen/Qwen3-14B

reasoning_fast:
  provider: local
  model: Qwen/Qwen3-8B

embeddings:
  model: BAAI/bge-m3

reranker:
  model: BAAI/bge-reranker-v2-m3
```

Retrieval config:

```yaml
dense_top_k: 30
sparse_top_k: 30
fusion_top_k: 30
rerank_top_k: 8

graph:
  max_hops: 2
  max_nodes: 30

agent:
  max_retrieval_cycles: 2
  max_tool_calls: 15
```

---

# 84. COMPANY CONFIG

Example:

```yaml
companies:
  - ticker: NVDA
    cik: ...
  - ticker: AMD
    cik: ...
```

Do not manually guess CIK values.

Resolve and validate them from authoritative data.

---

# 85. ENVIRONMENT VARIABLES

Example:

```text
MODEL_PROVIDER=local

LOCAL_LLM_BASE_URL=
LOCAL_LLM_MODEL=

EMBEDDING_MODEL=
RERANKER_MODEL=

SEC_USER_AGENT=
SEC_CONTACT_EMAIL=
SEC_REQUESTS_PER_SECOND=5

QDRANT_MODE=local
QDRANT_URL=

DATABASE_MODE=postgres
DATABASE_URL=

GRAPH_MODE=networkx
NEO4J_URI=
NEO4J_USER=
NEO4J_PASSWORD=

ENABLE_FRED=false
FRED_API_KEY=

PHOENIX_ENDPOINT=

ENABLE_COMMERCIAL_MODELS=false

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
```

Commercial keys remain blank.

---

# 86. LOCAL DEVELOPMENT COMMANDS

Eventually support:

```text
python -m scripts.download_filings
python -m scripts.download_companyfacts

python -m scripts.build_documents
python -m scripts.build_database
python -m scripts.build_index
python -m scripts.build_graph

python -m scripts.build_eval_set

python -m scripts.evaluate_retrieval
python -m scripts.evaluate_financial
python -m scripts.evaluate_temporal
python -m scripts.evaluate_graph

uvicorn filingsgraph.api.main:app --reload

python app/gradio_app.py

pytest
```

Optional:

```text
make setup
make data
make index
make graph
make eval
make app
```

Document Windows equivalents.

---

# 87. DOCKER

Docker Compose initial services:

```text
PostgreSQL
Qdrant
Phoenix
```

Optional:

```text
Neo4j Community
```

Do not require Neo4j during first stages.

Local LLM may run separately through WSL2/vLLM.

---

# 88. FASTAPI

Potential endpoints:

```text
GET  /health
GET  /companies
GET  /filings

POST /research
GET  /research/{id}

POST /compare/companies
POST /compare/periods
POST /risks/evolution

GET  /graph/company/{ticker}
GET  /graph/risk/{risk_id}

POST /retrieval/debug

GET /metrics/summary
```

---

# 89. UI — RECRUITER EXPERIENCE

Recruiter should understand FilingsGraph within approximately one minute.

---

# 90. SIDEBAR

Provide:

### Company Selection

```text
NVIDIA
AMD
Intel
...
```

### Period Selection

```text
FY2023
FY2024
FY2025
```

### Analysis Mode

```text
Ask Question
Compare Companies
Risk Evolution
Financial Metric Analysis
Graph Explorer
```

---

# 91. MAIN QUERY EXPERIENCE

Example query:

> “How has NVIDIA's exposure to export restrictions evolved over the last three annual filings, and which business areas appear most connected to that risk?”

Display:

### Research Plan

Concise, not chain-of-thought.

```text
✓ Retrieve relevant filings
✓ Compare risk sections
✓ Identify risk entities
✓ Traverse segment relationships
✓ Verify temporal attribution
```

---

# 92. EVIDENCE PANEL

Display:

```text
Company
Filing
Fiscal Year
Section
Evidence Snippet
Citation
Retrieval Method
```

---

# 93. FINANCIAL FACT PANEL

Example:

```text
Revenue
FY2023: ...
FY2024: ...
FY2025: ...

YoY Change:
...

Source:
SEC XBRL
```

Never show fabricated values.

---

# 94. RISK TIMELINE

A visually strong feature:

```text
FY2023 ───────── FY2024 ───────── FY2025

Export Controls
 Moderate          Expanded          Expanded

Supply Chain
 Existing          Existing          Increased

AI Regulation
 Low               New               Expanded
```

Every timeline point needs evidence.

---

# 95. KNOWLEDGE GRAPH VIEW

Interactive view:

```text
Company
   │
   ├── Segment
   │      └── Product
   │
   ├── Geography
   │
   └── Risk
          └── Regulation
```

Click node → show supporting filing evidence.

---

# 96. CROSS-COMPANY COMPARISON UI

Example:

| Company   | Risk            | FY24     | FY25     | Change |
| --------- | --------------- | -------- | -------- | ------ |
| Company A | Export controls | Existing | Expanded | ↑      |
| Company B | Supply chain    | Expanded | Expanded | →      |

Actual results only.

---

# 97. ANALYST REPORT

Final result:

# Executive Summary

# Key Financial Findings

# Risk Changes

# Cross-Period Comparison

# Graph Relationships

# Contradictory Evidence

# Important Limitations

# Evidence & Citations

Do not produce investment recommendations.

---

# 98. HUMAN REVIEW

Because this is research intelligence rather than autonomous action, HITL can be implemented as:

```text
[Accept Analysis]
[Flag Citation]
[Request More Evidence]
[Export Research Memo]
```

Do not call this investment approval.

It is analyst review.

---

# 99. PUBLIC DEPLOYMENT STRATEGY

The project must retain:

# ZERO MANDATORY PAID API DEPENDENCY.

Primary source:

# GitHub

---

# 100. HUGGING FACE DEPLOYMENT

Use Hugging Face Spaces if free resources permit.

Preferred UI:

# Gradio

However:

Do NOT assume every project can receive a dedicated permanent free GPU allocation.

The portfolio may already use other available free ZeroGPU slots.

Therefore support three deployment modes.

---

# 101. DEPLOYMENT MODE A — ZEROGPU AVAILABLE

If a free ZeroGPU slot is available:

```text
Hugging Face Space
↓
Gradio
↓
Small / Efficient Local LLM
↓
Precomputed Filing Index
↓
Financial + Graph Tools
```

Likely use Qwen3-8B or a smaller currently strong model rather than 14B if latency requires it.

Benchmark first.

---

# 102. DEPLOYMENT MODE B — CPU-ONLY FREE DEMO

If no ZeroGPU slot is available:

Deploy a CPU-friendly interactive system demonstrating:

* hybrid retrieval;
* XBRL queries;
* deterministic calculations;
* risk timelines;
* graph traversal;
* precomputed example analyses.

LLM generation can be:

* restricted;
* smaller model;
* precomputed for selected example questions.

Clearly label precomputed examples.

Do NOT pretend cached answers are live LLM inference.

---

# 103. DEPLOYMENT MODE C — RECORDED FULL SYSTEM

Full local system runs on RTX 5090.

Public portfolio provides:

* recorded video;
* screenshots;
* architecture;
* evaluation;
* interactive graph/retrieval demo;
* GitHub setup instructions.

A permanently live model is NOT required for technical credibility.

---

# 104. PUBLIC DEMO DATA

Use curated subset:

```text
3–5 companies
3 years
10-K only
precomputed chunks
precomputed embeddings
normalized XBRL facts
prebuilt graph
```

Possible demo storage:

```text
Qdrant embedded/local
DuckDB
NetworkX serialized graph
```

This creates a self-contained free deployment.

---

# 105. VERCEL STRATEGY

Vercel should host:

# Personal Portfolio Website

and

# FilingsGraph Case Study Page

Not the 14B LLM.

Architecture:

```text
Personal Portfolio
      │
      │ Vercel
      ▼
FilingsGraph Case Study
      │
      ├── Architecture
      ├── Results
      ├── Risk Timeline
      ├── Graph Screenshot
      ├── Demo Video
      ├── GitHub
      └── Live Demo
              │
              ▼
      Hugging Face Space
      if available
```

---

# 106. ZERO-COST FALLBACK RULE

If free hosting policies change:

DO NOT introduce paid infrastructure without asking me.

Instead preserve:

* local runnable system;
* GitHub;
* evaluation results;
* recorded demo;
* portfolio case study.

The portfolio value must not depend on monthly hosting fees.

---

# 107. GITHUB README

Final README should resemble a professional AI-engineering case study.

Structure:

# FilingsGraph

## Hero

* project statement
* architecture
* demo link
* GitHub badges
* actual headline metrics

## Business Problem

## Why Normal Filing RAG Is Not Enough

Explain:

* financial facts
* temporal comparison
* graph relationships
* calculations

## Solution

## Key Capabilities

* hierarchical RAG
* hybrid retrieval
* reranking
* XBRL analytics
* temporal risk intelligence
* knowledge graph
* routed Agentic RAG
* verification
* local LLM

## Architecture

## Data Sources

## SEC Fair Access

## Filing Parsing

## XBRL Processing

## RAG Architecture

## Temporal Intelligence

## Knowledge Graph

## Agent Workflow

## Financial Tools

## Verification

## Baseline → V6

## Evaluation Dataset

## Results

## Ablation Study

## Failure Analysis

## Security

## Observability

## UI Screenshots

## Demo

## Installation

## Local Model Setup

## Reproduce Evaluation

## Repository Structure

## Limitations

## Responsible Use

## Future Enhancements

## Optional Commercial Model Benchmark

## Data Attribution

## License

Never fabricate metrics.

---

# 108. GITHUB QUALITY REQUIREMENTS

Include:

* strong README
* architecture diagram
* data-source citations
* clear SEC provenance
* type hints
* Pydantic models
* tests
* evaluation scripts
* `.env.example`
* no secrets
* Docker
* CI
* experiment results
* ablation study
* failure analysis
* screenshots
* graph visualization
* demo video
* limitations
* responsible-use statement
* reproducible setup

This should look like a serious AI/financial-data engineering project.

---

# 109. PORTFOLIO PROJECT CARD

Future personal website:

# FilingsGraph

**Advanced RAG • GraphRAG • Temporal AI • Financial Intelligence**

Description:

> Temporal financial-intelligence engine combining SEC filings, structured XBRL facts, hybrid retrieval and knowledge graphs for evidence-grounded cross-company due diligence and risk analysis.

Show:

* graph visualization
* risk timeline
* architecture thumbnail
* 3 actual metrics
* GitHub
* Demo
* Case Study

---

# 110. PORTFOLIO CASE STUDY STORY

The project page should tell:

### Problem

Financial filings contain both narrative and structured facts.

### V0

Dense RAG.

### Problem

Dense RAG struggles with exact terminology and numerical questions.

### V2

Hybrid retrieval.

### Problem

LLM arithmetic and table interpretation can be unreliable.

### V4

XBRL structured tools.

### Problem

Cross-period/relational questions remain difficult.

### V5

Temporal + knowledge graph retrieval.

### Problem

Complex questions require different retrieval strategies.

### V6

Query routing + verification + production application.

This narrative is extremely important.

---

# 111. LINKEDIN PROJECT TITLE

Use:

# FilingsGraph — Temporal Financial Due-Diligence & Risk Intelligence Engine

---

# 112. LINKEDIN DESCRIPTION

After actual evaluation exists, create a polished LinkedIn description approximately like:

> Built an end-to-end financial-intelligence platform combining SEC filings, structured XBRL facts, hybrid RAG and temporal knowledge graphs for evidence-grounded cross-company and cross-period analysis. Implemented local open-source LLM inference, section-aware document retrieval, dense/BM25 fusion, reranking, deterministic financial calculations, temporal risk-change detection, graph traversal, citation verification, quantitative evaluation and production deployment.

Then add real metrics such as:

> Improved retrieval Recall@10 from **[V0] to [final]**, achieved **[numeric accuracy]** deterministic financial-calculation accuracy and **[citation precision]** citation precision on a frozen evaluation set.

Never fabricate numbers.

---

# 113. LINKEDIN SKILLS

Potential:

* Retrieval-Augmented Generation
* Generative AI
* Large Language Models
* GraphRAG
* Knowledge Graphs
* Agentic AI
* Information Retrieval
* Financial Data Analysis
* XBRL
* Natural Language Processing
* LangGraph
* Hugging Face
* Qdrant
* PostgreSQL
* Python
* FastAPI
* Docker
* OpenTelemetry
* AI Evaluation
* LLMOps

Choose final entries based on current LinkedIn availability.

---

# 114. RESUME BULLETS

After real experiments:

### Bullet 1

Built **FilingsGraph**, a temporal financial-intelligence platform combining SEC filings, XBRL financial facts, hybrid RAG and knowledge graphs to support evidence-grounded cross-company and cross-period due-diligence analysis.

### Bullet 2

Improved retrieval **Recall@10 from [V0] to [final]** through section-aware chunking, dense/BM25 fusion and reranking, while achieving **[numeric accuracy]** financial-calculation accuracy and **[temporal F1]** on risk-change detection.

### Bullet 3

Engineered query routing, deterministic financial tools, temporal GraphRAG, claim/citation verification, OpenTelemetry tracing, FastAPI and Docker deployment using fully open-source local models with **$0 mandatory paid LLM API dependency**.

No fabricated results.

---

# 115. GITHUB SHORT DESCRIPTION

Approximately:

> Temporal SEC intelligence using hybrid RAG, XBRL analytics, knowledge graphs and evidence-verified open-source LLM reasoning.

---

# 116. DEMO VIDEO

Create a 60–90 second recruiter-friendly demo.

### 0–8 seconds

Show FilingsGraph title.

### 8–18

Select company/cohort and period.

### 18–30

Ask:

> “How have export-control risks evolved across these companies?”

### 30–42

Show:

* hybrid retrieval
* evidence
* filing years

### 42–52

Show risk timeline.

### 52–62

Show knowledge graph.

### 62–72

Ask a numeric question.

Show XBRL calculation.

### 72–82

Show citation verification.

### 82–90

Show evaluation dashboard.

---

# 117. ARCHITECTURE VISUALS

Create:

## Full Architecture

```text
SEC Filings + XBRL
        ↓
      Ingestion
        ↓
┌───────┴────────┐
↓                ↓
Text           Facts
↓                ↓
Hybrid RAG     SQL
↓                ↓
└──────┬─────────┘
       ↓
Knowledge Graph
       ↓
Query Router
       ↓
Agentic Research
       ↓
Verification
       ↓
Analyst Report
```

## Retrieval Architecture

```text
Question
 ├── Dense
 └── BM25
      ↓
    Fusion
      ↓
  Reranking
      ↓
   Evidence
```

## Temporal Architecture

```text
FY2023
   ↓
FY2024
   ↓
FY2025
   ↓
Risk Alignment
   ↓
Change Detection
```

## Graph Architecture

```text
Company
 ├── Segment
 ├── Product
 ├── Geography
 └── Risk
```

## Version Journey

```text
V0 → V1 → V2 → V3 → V4 → V5 → V6
```

---

# 118. TESTING

Include:

## Unit Tests

* SEC client
* rate limiter
* filing parser
* section extractor
* XBRL normalizer
* financial calculations
* chunking
* retrieval
* fusion
* graph
* period alignment
* citations

## Integration Tests

* SEC → cache
* filing → chunks
* chunks → retrieval
* XBRL → database
* graph → retrieval
* agent → tools
* verification

## Security Tests

* prompt injection
* malicious filing text
* invalid SEC URL
* excessive query
* malformed XBRL
* unauthorized network source

## Evaluation Tests

Frozen benchmark subset.

## Smoke Tests

One full financial query.

One temporal query.

One graph query.

---

# 119. CI

GitHub Actions should run:

```text
lint
unit tests
selected integration tests
financial calculation tests
graph tests
security smoke tests
benchmark-schema validation
```

Do not run large LLM/GPU evaluation during CI.

---

# 120. EXPERIMENT REPRODUCIBILITY

Record:

```text
experiment_id
timestamp
git_commit
dataset_version
companies
filing_period
benchmark_version
LLM
embedding
chunking
retrieval
fusion
reranker
graph_enabled
graph_hops
metrics
latency
VRAM
notes
```

Store:

* JSON
* CSV
* Markdown result tables.

---

# 121. MODEL COMPARISON

Where feasible:

```text
Qwen3-8B
vs
Qwen3-14B
```

Measure:

* query routing
* temporal synthesis
* financial answer quality
* structured-output accuracy
* tool selection
* citation quality
* latency
* VRAM

Determine whether 14B meaningfully improves outcomes.

---

# 122. NO UNNECESSARY FRAMEWORK STACKING

Do NOT combine:

* LangChain
* LangGraph
* LlamaIndex
* DSPy
* CrewAI
* AutoGen

for resume keywords.

Preferred architecture:

* LangGraph
* direct Qdrant client
* NetworkX / Neo4j
* Pydantic
* FastAPI
* Hugging Face/vLLM
* PostgreSQL/DuckDB
* direct SEC client

Every tool should have a reason.

---

# 123. COMPLETE PROJECT DELIVERY REQUIREMENT

I do NOT want FilingsGraph delivered as a Day-1, Day-2, Day-3, or other time-boxed implementation sequence.

The AI must build the **complete runnable core FilingsGraph project first** and provide it to me as one coherent downloadable repository/archive.

The initial delivery must contain the implementation needed for the complete core system described in this master prompt, including:

* project structure;
* configuration;
* SEC EDGAR client;
* Fair Access controls;
* company/CIK resolution;
* filing download and local caching;
* filing HTML parsing;
* section extraction;
* hierarchical/section-aware chunking;
* XBRL/company-facts ingestion;
* fiscal-period normalization;
* unit normalization;
* financial concept normalization;
* deterministic financial calculations;
* dense retrieval;
* sparse/BM25 retrieval;
* hybrid fusion;
* metadata/period filtering;
* reranking;
* structured financial database;
* temporal filing comparison;
* risk-difference analysis;
* temporal risk intelligence;
* temporal knowledge graph;
* graph provenance;
* graph traversal;
* query classification/routing;
* research planning;
* typed filing/XBRL/financial/temporal/graph tools;
* local LLM provider abstraction;
* LangGraph orchestration;
* evidence/citation handling;
* numerical verification;
* temporal verification;
* entity/unit verification;
* contradiction handling;
* evaluation framework;
* ablation framework;
* failure-analysis framework;
* observability;
* security/guardrails;
* FastAPI;
* Gradio;
* Docker/local infrastructure configuration;
* tests;
* scripts;
* documentation;
* GitHub-quality repository files.

Do not stop after creating only:

* the environment;
* repository skeleton;
* SEC client;
* one filing download;
* one XBRL example;
* V0 dense RAG;
* or another partial milestone.

Do not require me to execute an early stage before you implement the later core stages.

The first objective is:

> **Build and package the complete project so I can download it and execute the full FilingsGraph pipeline locally.**

The project must preserve the V0 → V6 progression because it is required for benchmarking, ablation studies, and demonstrating measurable engineering improvement.

However:

> **V0 → V6 is an experimental/evaluation progression inside the complete repository, not a day-by-day delivery schedule.**

Actual performance metrics must remain unfilled/TBD until I execute the project and generate them.

Do not fabricate SEC-derived outputs, retrieval results, financial metrics, graph results, or model-evaluation results simply because the complete codebase is being delivered before execution.

---

# 124. COMPLETE BUILD → LOCAL EXECUTION → RESULTS-BASED ITERATION

Use the following working model.

## PHASE A — BUILD THE COMPLETE PROJECT

Before asking me to run FilingsGraph, create the complete repository and package it as a downloadable archive.

The repository must contain the complete core implementation required to execute the system from SEC data acquisition through final evaluation and application launch.

Where a component cannot be fully executed in the AI's current environment because it requires:

* my RTX 5090;
* CUDA;
* WSL2;
* Docker Desktop;
* large local model downloads;
* SEC network access;
* local PostgreSQL/Qdrant/Phoenix infrastructure;
* or another machine-specific dependency,

still implement that component completely and provide validation commands for me to run locally.

Test everything that can reasonably be tested in the AI's environment before packaging the project.

Do not intentionally leave core modules as empty placeholders merely because I have not run earlier stages yet.

---

## PHASE B — GIVE ME THE EXACT LOCAL EXECUTION ORDER

After the complete project is delivered, provide one ordered local runbook.

The runbook should take me through FilingsGraph in a logical technical sequence such as:

```text
Environment / GPU verification
        ↓
Docker / local infrastructure startup
        ↓
SEC configuration + Fair Access validation
        ↓
Company / CIK resolution
        ↓
Filing + Company Facts download
        ↓
Raw-data validation and caching
        ↓
Filing parsing / section extraction
        ↓
XBRL normalization
        ↓
Structured financial database build
        ↓
Document chunking
        ↓
Embedding / BM25 / Qdrant index construction
        ↓
V0 dense baseline evaluation
        ↓
V1 section-aware evaluation
        ↓
V2 hybrid retrieval evaluation
        ↓
V3 reranking evaluation
        ↓
V4 structured XBRL intelligence evaluation
        ↓
V5 temporal + graph intelligence evaluation
        ↓
V6 routed agentic production-system evaluation
        ↓
Graph ablation
        ↓
Structured-data ablation
        ↓
Full evaluation benchmark
        ↓
Failure analysis
        ↓
FastAPI / Gradio application
        ↓
Observability / security checks
        ↓
Final result export
```

This is an **execution order**, not a calendar roadmap.

For every major command or execution stage, tell me:

1. the exact command;
2. whether to run it in PowerShell, Windows Python, WSL2, Docker, or another environment;
3. what it does;
4. what successful output should look like;
5. where generated files/results are stored;
6. what warnings are acceptable;
7. what failure logs or outputs I should send back to you.

Prefer automation scripts that reduce manual work.

Where practical, provide:

* a top-level orchestration command/script for the complete pipeline;
* individual stage commands for debugging;
* resumable execution so already-downloaded SEC data and already-built indexes are not unnecessarily recreated;
* local caching so SEC endpoints are not repeatedly called during evaluation.

---

## PHASE C — I RUN THE COMPLETE PROJECT AND GENERATE REAL RESULTS

After receiving the complete project, I will run it locally.

The execution should generate the real:

* SEC ingestion/validation results;
* filing parsing quality reports;
* XBRL normalization results;
* V0/V1/V2/V3 retrieval comparisons;
* structured financial-tool results;
* numerical accuracy;
* temporal comparison metrics;
* risk-change metrics;
* graph extraction metrics;
* graph-retrieval metrics;
* query-routing metrics;
* citation/grounding metrics;
* local-model benchmark results;
* latency results;
* GPU/VRAM observations;
* full ablation table;
* failed-case reports;
* application smoke-test results;
* observability traces/screenshots where appropriate.

The codebase must save these outputs in machine-readable and human-readable formats.

Do not pre-populate fake successful metrics.

Use `TBD`, empty result templates, schemas, or clearly labeled examples until actual execution creates real results.

---

## PHASE D — RESULTS-BASED IMPROVEMENT

Once I send the actual logs, metrics, failures, and generated reports:

1. analyze the real results;
2. identify retrieval, XBRL, temporal, graph, routing, model, or verification bottlenecks;
3. determine which architectural changes are justified;
4. modify the existing project instead of rebuilding from scratch;
5. rerun only the experiments affected by those changes where practical;
6. compare new results with the original baselines;
7. preserve experiment history;
8. continue iterating until the project is strong and honest enough for GitHub, LinkedIn, resume, portfolio, and interviews.

Do not repeatedly optimize against the frozen final test set.

Use the development evaluation set for tuning.

The frozen final test set must remain protected for unbiased final measurement.

---

# 125. PRIORITY ORDER IF OPTIONAL SCOPE MUST BE REDUCED

The expectation remains to deliver the complete core FilingsGraph project.

If a genuinely optional component must be deferred because it would destabilize the core project or introduce an unnecessary external dependency, prioritize in this order.

## MUST HAVE

1. SEC ingestion
2. local caching
3. Fair Access compliance
4. company/CIK resolution
5. filing parsing
6. section-aware chunking
7. BM25 baseline
8. dense baseline
9. hybrid retrieval
10. reranking
11. retrieval evaluation
12. XBRL structured facts
13. fiscal-period normalization
14. unit/concept normalization
15. deterministic financial calculations
16. numerical verification
17. temporal filing comparison
18. risk-change analysis
19. temporal knowledge graph
20. graph provenance
21. graph retrieval
22. graph/temporal ablations
23. query routing
24. local LLM
25. evidence-grounded synthesis
26. citation verification
27. failure analysis
28. working UI
29. reproducible GitHub repository

## SHOULD HAVE

30. Phoenix/OpenTelemetry tracing
31. FastAPI
32. Docker Compose
33. Hugging Face deployment configuration
34. interactive graph/risk-timeline visualization
35. automated evaluation dashboard

## STRETCH / FUTURE

36. large company universe
37. broad 10-Q integration
38. 8-K event intelligence
39. FRED API integration
40. earnings-call transcripts
41. Neo4j migration
42. multimodal chart/table models
43. GraphRAG community summaries
44. authenticated workspaces
45. commercial-model benchmarking
46. fine-tuning

Do not sacrifice evaluation quality, SEC correctness, temporal correctness, or financial-data correctness for superficial breadth.

If something from SHOULD HAVE or STRETCH/FUTURE is deferred, document:

* why it was deferred;
* how the core project works without it;
* what would be required to add it later.

---


# 126. DEFINITION OF DONE

FilingsGraph becomes portfolio-ready when critical requirements exist.

## Data

* [ ] Uses official SEC information
* [ ] Respects Fair Access
* [ ] Caches filings
* [ ] resolves companies/CIKs
* [ ] parses 10-K sections
* [ ] ingests XBRL facts
* [ ] normalizes fiscal periods
* [ ] preserves provenance

## RAG

* [ ] BM25
* [ ] dense retrieval
* [ ] hybrid retrieval
* [ ] reranking
* [ ] metadata filtering
* [ ] hierarchical retrieval
* [ ] citations

## Structured Intelligence

* [ ] exact financial facts
* [ ] deterministic calculations
* [ ] unit validation
* [ ] fiscal-period validation

## Temporal

* [ ] filing comparison
* [ ] risk evolution
* [ ] new/changed risk identification
* [ ] timeline UI

## Graph

* [ ] graph nodes
* [ ] evidence-grounded edges
* [ ] temporal relationships
* [ ] graph traversal
* [ ] graph evaluation
* [ ] interactive visualization

## Agent

* [ ] query classification
* [ ] tool routing
* [ ] mixed structured/unstructured reasoning
* [ ] stopping limits
* [ ] no-answer handling

## Verification

* [ ] numeric verification
* [ ] citation verification
* [ ] temporal verification
* [ ] entity verification

## Evaluation

* [ ] DEV benchmark
* [ ] frozen TEST
* [ ] V0 baseline
* [ ] final metrics
* [ ] ablation study
* [ ] graph ablation
* [ ] failure analysis

## Engineering

* [ ] local open-source LLM
* [ ] no mandatory paid API
* [ ] FastAPI
* [ ] Pydantic
* [ ] tests
* [ ] Docker
* [ ] CI
* [ ] observability
* [ ] security controls

## Presentation

* [ ] polished UI
* [ ] README
* [ ] architecture
* [ ] knowledge graph screenshot
* [ ] temporal risk screenshot
* [ ] evaluation dashboard
* [ ] demo video
* [ ] LinkedIn description
* [ ] resume bullets
* [ ] portfolio card
* [ ] deployment documentation

---

# 127. RECRUITER TEST

Within approximately 60 seconds, the recruiter should understand:

> This is not “ChatGPT over a 10-K.”

It combines:

```text
SEC Filings
+
XBRL
+
Advanced RAG
+
Temporal Analysis
+
Knowledge Graphs
+
Deterministic Financial Analytics
+
Agentic Tool Routing
+
Evaluation
+
Verification
```

A technical reviewer should be able to inspect the repository and verify that these systems actually exist.

---

# 128. INTERVIEW STORY

The finished project must let me explain:

> I first built a dense RAG baseline over SEC filings. It handled semantic questions reasonably well but struggled with exact terminology and financial identifiers, so I added BM25 and hybrid fusion. Reranking improved evidence ordering, but RAG alone was still inappropriate for exact numerical questions, so I normalized XBRL financial facts and exposed deterministic financial tools. I then found that cross-period questions required explicit temporal normalization and filing-difference analysis. Relationship-heavy questions still needed more structure, so I created an evidence-provenanced temporal knowledge graph and measured whether graph expansion improved multi-hop questions. Finally, I introduced a routed agentic workflow that chooses between text retrieval, structured financial tools and graph traversal, then verifies numbers, fiscal periods and citations before producing the answer. The entire system runs on open-source local models without mandatory paid LLM APIs.

Everything in that explanation must eventually be backed by actual code and evaluation.

---

# 129. FUTURE ENHANCEMENTS

After the first MVP:

* 10-Q integration
* 8-K event intelligence
* earnings-call transcripts where legally/publicly available
* FRED macroeconomic integration
* richer company universe
* industry-level risk clusters
* graph community detection
* supplier/company entity normalization
* multimodal chart/table understanding
* long-context experiments
* automated analyst memo generation
* event-driven filing ingestion
* incremental vector updates
* incremental graph updates
* portfolio monitoring
* model routing
* local VLM
* commercial frontier-model benchmarking
* GraphRAG community summaries
* authenticated user research workspaces

Do NOT implement all of these future enhancements in the initial complete core build. Keep them documented as future work unless they are required for the core system to function correctly.

---

# 130. OPTIONAL COMMERCIAL MODEL BENCHMARK

Future only:

```text
Open-Source Local LLM
vs
Commercial Frontier Model A
vs
Commercial Frontier Model B
```

Compare:

* textual QA
* numerical reasoning
* temporal reasoning
* graph reasoning
* citation quality
* latency
* external API cost
* privacy
* deployment requirements

Repo remains complete without this.

---

# 131. CRITICAL HONESTY RULES

Never:

* fabricate financial data;
* fabricate metrics;
* fabricate citations;
* mix fiscal years incorrectly;
* present unsupported relationships as facts;
* call graph edges factual without evidence;
* perform calculations mentally when deterministic tools exist;
* tune repeatedly against frozen test set;
* present correlation as causation;
* provide personalized investment advice;
* recommend buy/sell actions;
* hide synthetic evaluation examples;
* imply FRED is mandatory;
* silently invoke paid APIs;
* present a cached answer as live model generation;
* claim GraphRAG is beneficial without measuring it;
* claim production readiness without qualification.

---

# 132. HOW YOU SHOULD WORK WITH ME

We are going to build, execute, evaluate, and refine FilingsGraph in this dedicated conversation.

Do NOT respond with another conceptual project overview after receiving this prompt.

Begin implementation of the complete project.

## Initial delivery behavior

Your first implementation objective is to create the **complete runnable FilingsGraph project** and provide it as a downloadable repository/archive.

Do NOT deliver only:

* environment setup;
* a repository skeleton;
* the SEC client;
* one downloaded filing;
* one Company Facts example;
* V0 only;
* or another partial milestone

and then require me to run it before you implement the rest of the core system.

Instead:

1. freeze the final core architecture;
2. verify current dependencies, models, SEC endpoints, SEC Fair Access requirements, licenses, and deployment assumptions using authoritative sources;
3. generate the complete repository;
4. implement all core modules with complete runnable code;
5. add configuration, scripts, tests, documentation, and reproducible runbooks;
6. validate whatever can reasonably be validated in your environment;
7. package the complete project for download;
8. give me the exact local execution sequence;
9. clearly distinguish what you actually tested from GPU/network/infrastructure paths that still require my machine.

Do not fabricate runtime results.

Do not fabricate SEC data.

Do not fabricate financial metrics.

Do not fabricate graph quality, retrieval quality, or LLM performance.

## After I run the complete project

Once I execute the project locally and send logs, metrics, reports, screenshots, or errors:

1. diagnose the actual outputs;
2. explain what the metrics mean;
3. identify the highest-value improvements;
4. modify the existing project instead of rebuilding unnecessarily;
5. provide complete replacement files for changed modules;
6. preserve working components;
7. preserve evaluation and experiment history;
8. compare improvements with actual previous results;
9. continue until the project is portfolio-ready.

Ask only genuinely blocking questions.

Do not repeatedly ask for information that can be derived from provided logs, files, configuration, or results.

---


# 133. CODE QUALITY RULES

When generating code:

* provide complete files;
* specify exact file path;
* use type hints;
* use Pydantic;
* centralize configuration;
* use logging;
* implement exceptions;
* implement caching;
* implement retries;
* write tests;
* preserve provenance;
* never hardcode credentials;
* never hardcode fake CIK values;
* never hardcode results;
* avoid monolithic notebooks;
* place production logic under `src/`.

Notebooks are for:

* exploration
* experiments
* visual evaluation

not production architecture.

When replacing a file:

```text
FILE TO REPLACE:
src/...
```

Provide the full replacement where practical.

---

# 134. RESEARCH RULE

Before selecting final versions of:

* Python
* PyTorch
* CUDA
* Qwen
* BGE embeddings
* reranker
* SEC endpoints
* SEC Fair Access policy
* LangGraph
* Qdrant
* NetworkX
* Neo4j
* Phoenix
* Hugging Face deployment

check CURRENT official documentation.

This project is being implemented in 2026.

Do not copy outdated 2023 financial-RAG tutorials.

---

# 135. FIRST RESPONSE AND INITIAL DELIVERY I WANT FROM YOU

After receiving this master prompt, begin with:

# FILINGSGRAPH — COMPLETE PROJECT BUILD

Do NOT stop at a conceptual response, first-day starter, repository skeleton, SEC client, or one-file prototype.

Perform the following.

## 1. Final Frozen Scope

Explain exactly what is included in the **complete core FilingsGraph project**.

Separate:

### Core Complete Build

from:

### Optional / Stretch / Future

Do not use a 10-day or Day-1/Day-2 roadmap.

---

## 2. Final Architecture

Show the complete exact implementation architecture.

Preserve V0 → V6 as the project's experimental/evaluation progression, but treat it as internal versioning inside the already-complete repository rather than staged delivery.

---

## 3. Final Open-Source Stack

Verify current:

* Python;
* PyTorch/CUDA;
* reasoning model;
* embedding model;
* reranker;
* orchestration;
* vector database;
* structured database;
* graph framework;
* SEC endpoints;
* SEC Fair Access policy;
* observability;
* API;
* UI;
* Docker/local infrastructure;
* public deployment strategy.

Include licensing/cost information where relevant.

Use current authoritative documentation.

---

## 4. Zero-Cost Verification

Explicitly identify anything that could cost money.

Replace mandatory paid services.

The default complete project must remain usable with:

> **$0 mandatory paid external LLM/API dependency.**

Optional services requiring free registration or user-provided keys must remain disabled by default.

---

## 5. SEC Data Strategy

Implement and document:

* official SEC APIs/endpoints;
* company submissions;
* filings;
* Company Facts/XBRL;
* local caching;
* SEC Fair Access;
* descriptive User-Agent configuration;
* rate limiting;
* retries/backoff;
* domain allowlisting;
* provenance preservation.

Do not hardcode a fake production contact email.

Provide configuration for the user to supply it.

---

## 6. Initial Company Cohort

Research and select the best 5–8 companies for the bounded initial corpus.

Explain:

* business rationale;
* SEC filing availability;
* temporal depth;
* XBRL quality;
* graph usefulness;
* cross-company comparison value.

The chosen cohort must be encoded in configuration, not scattered through source code.

---

## 7. Filing Scope

Specify and implement the initial:

* fiscal-year range;
* form types;
* filing sections;
* document hierarchy.

Keep the initial corpus bounded enough to run reproducibly while still supporting meaningful temporal and cross-company analysis.

---

## 8. XBRL Strategy

Specify and implement:

* initial financial metrics;
* concept normalization;
* fiscal-period normalization;
* units/scales;
* deterministic calculations;
* validation;
* provenance.

---

## 9. Knowledge Graph Scope

Implement the graph node/edge types justified by the core use cases.

Do not create meaningless relationships simply to make the graph appear larger.

Every non-trivial edge must preserve provenance and temporal validity.

---

## 10. Evaluation Strategy

Implement the evaluation framework and benchmark schemas for:

* textual retrieval;
* numerical questions;
* temporal questions;
* risk-change detection;
* graph questions;
* mixed structured/unstructured questions;
* query routing;
* grounding/citations;
* system performance.

Keep a development evaluation split and a protected frozen final test split.

Do not fabricate benchmark results.

---

## 11. Deployment Plan

Confirm or improve the architecture:

```text
GitHub
→ complete source + reproducible evaluation + results after execution

Hugging Face
→ interactive demo when genuinely free resources permit

Vercel
→ polished portfolio/case-study presentation

Local RTX 5090
→ complete full-capability system
```

The project must remain valuable and runnable if free public GPU hosting is unavailable.

---

## 12. Complete Repository Generation

Generate the entire core FilingsGraph repository described in this master prompt.

Do not merely show a directory tree.

Create the actual files and complete runnable code.

The repository should include, where applicable:

```text
README.md
LICENSE
SECURITY.md
DATA_SOURCES.md
BENCHMARK.md
CONTRIBUTING.md
pyproject.toml
.python-version
.gitignore
.env.example
docker-compose.yml
Makefile

configs/
data/
notebooks/
src/filingsgraph/
app/
frontend/
scripts/
tests/
reports/
docs/
assets/
.github/workflows/
```

Implement the complete core modules for:

* configuration;
* schemas;
* SEC client and Fair Access controls;
* company/CIK resolution;
* filing download/cache;
* Company Facts/XBRL ingestion;
* filing parsing;
* section extraction;
* table handling;
* normalization;
* section-aware/hierarchical chunking;
* embeddings;
* BM25;
* Qdrant indexing;
* hybrid retrieval;
* fusion;
* metadata/period filters;
* parent context;
* reranking;
* structured financial storage;
* financial calculations;
* fiscal-period normalization;
* XBRL concept/unit handling;
* temporal alignment;
* risk-difference analysis;
* temporal timelines;
* graph nodes/edges;
* graph extraction/provenance;
* graph building;
* temporal graph validity;
* graph traversal;
* LLM provider abstraction;
* local provider;
* typed tools;
* LangGraph routing/planning/workflow;
* stopping conditions;
* citation verification;
* numeric verification;
* temporal verification;
* unit/entity verification;
* claim verification;
* evaluation metrics;
* experiment/ablation runners;
* failure analysis;
* observability;
* security;
* FastAPI;
* Gradio;
* tests;
* CI;
* documentation.

Do not leave core files as empty placeholders without a clearly documented technical reason.

---

## 13. Downloadable Complete Project

Package the complete repository into one downloadable archive.

Give me the download link.

Prefer a ZIP suitable for Windows extraction.

If possible, include a checksum.

Do not require me to reconstruct dozens of files manually from chat messages.

---

## 14. Validation Before Delivery

Before packaging, run every check that is feasible in your current environment, including where possible:

* syntax/import checks;
* unit tests;
* schema tests;
* SEC-client mocked tests;
* Fair Access/rate-limit tests;
* parsing fixtures;
* XBRL normalization tests;
* deterministic financial-calculation tests;
* temporal-alignment tests;
* graph-provenance tests;
* retrieval/fusion tests using lightweight fixtures;
* security tests;
* API import/smoke tests;
* lint/format checks.

Report exactly what you tested.

Also report exactly what you could NOT execute because it requires:

* SEC network access;
* my configured SEC User-Agent/contact information;
* RTX 5090;
* CUDA;
* WSL2;
* Docker;
* large model downloads;
* PostgreSQL/Qdrant/Phoenix;
* or other user-machine resources.

Do not imply that unexecuted paths have already been validated.

---

## 15. Local Environment Setup

Based on:

```text
Windows 11
RTX 5090
~32 GB VRAM
BF16 capable
TF32 capable
Docker Desktop
WSL2 available
```

give the exact setup commands.

Clearly label every command as:

* PowerShell;
* Windows Python;
* WSL2;
* Docker;
* or another environment.

---

## 16. Complete Local Execution Runbook

After the project is downloaded, give me the exact order to execute it locally.

The runbook must cover the complete pipeline.

Include commands for:

1. environment creation;
2. GPU verification;
3. Docker/infrastructure startup;
4. SEC User-Agent/contact configuration;
5. SEC connectivity/Fair Access validation;
6. company/CIK resolution;
7. filing download;
8. Company Facts/XBRL download;
9. data-quality validation;
10. filing parsing;
11. section extraction;
12. XBRL normalization;
13. structured financial database construction;
14. document/chunk generation;
15. dense embedding/index construction;
16. BM25 index construction;
17. V0 dense baseline;
18. V1 section-aware RAG;
19. V2 hybrid retrieval;
20. V3 reranking;
21. V4 structured XBRL intelligence;
22. V5 temporal + graph intelligence;
23. V6 routed agentic production system;
24. textual retrieval evaluation;
25. numerical evaluation;
26. temporal evaluation;
27. graph evaluation;
28. routing/agent evaluation;
29. citation/grounding evaluation;
30. graph ablation;
31. structured-data ablation;
32. model comparison if enabled;
33. system/latency evaluation;
34. failure-analysis export;
35. FastAPI startup;
36. Gradio startup;
37. observability checks;
38. security tests;
39. final result export.

If implementation combines some steps, that is acceptable.

Document both:

* an automated/end-to-end path;
* individual debugging commands where practical.

---

## 17. Expected Outputs

For each major execution stage, tell me:

* what output I should see;
* what files should be generated;
* where they are stored;
* what success means;
* what warnings are acceptable;
* what failure output I should send back.

---

## 18. Results and Metrics Policy

All performance results must initially remain:

```text
TBD / generated after local execution
```

unless they were genuinely produced by running the implemented project.

Do NOT fabricate:

* Recall@10;
* MRR;
* nDCG;
* numerical accuracy;
* risk-change F1;
* graph QA accuracy;
* edge precision;
* routing accuracy;
* citation precision;
* groundedness;
* latency;
* VRAM;
* model comparisons;
* or any other result.

The complete repository must include scripts that generate these metrics automatically.

---

## 19. What I Should Send Back After Execution

Tell me exactly which outputs/artifacts to return after the first complete local run.

At minimum, expect useful artifacts such as:

```text
environment/GPU verification
SEC ingestion/data-quality report
filing parsing report
XBRL normalization report
retrieval evaluation report
numerical evaluation report
temporal evaluation report
graph evaluation report
routing/agent evaluation report
citation/grounding report
ablation table
system/latency metrics
failure-analysis summary
pytest result
application smoke-test result
relevant error logs
```

After I provide these outputs, begin:

> **results-based debugging, tuning, ablation analysis, and improvement of the already complete FilingsGraph project.**

Do NOT rebuild the entire repository unless a fundamental architectural problem genuinely requires it.

---


# 136. FINAL GOAL

At the end of FilingsGraph I want to be able to legitimately say:

# “I designed and built a temporal financial-intelligence engine that combines SEC filings, structured XBRL data, hybrid retrieval and evidence-provenanced knowledge graphs to answer cross-company and cross-period due-diligence questions using open-source local LLMs.”

And:

# “I evaluated dense retrieval, lexical search, hybrid retrieval, reranking, structured financial tools, temporal reasoning and graph-enhanced retrieval independently before selecting the final architecture.”

And:

# “The system verifies financial calculations, fiscal periods and citations rather than relying blindly on LLM generation.”

And:

# “The complete default system requires no paid commercial LLM API.”

Every statement must be real.

The final project must demonstrate:

**SEC Data Acquisition
↓
Data Engineering
↓
Filing Parsing
↓
Hierarchical Knowledge Representation
↓
Dense RAG Baseline
↓
Sparse Retrieval
↓
Hybrid Retrieval
↓
Reranking
↓
XBRL Structured Financial Intelligence
↓
Deterministic Calculations
↓
Temporal Filing Analysis
↓
Risk Change Detection
↓
Knowledge Graph
↓
Temporal Graph Relationships
↓
Graph-Enhanced Retrieval
↓
Agentic Query Routing
↓
Evidence Synthesis
↓
Numeric Verification
↓
Temporal Verification
↓
Citation Verification
↓
Evaluation
↓
Ablation Studies
↓
Observability
↓
Security
↓
FastAPI / UI
↓
Deployment
↓
Professional GitHub + LinkedIn + Resume + Portfolio Presentation**

The priority is NOT maximum architectural complexity.

The priority is:

# A WORKING, MEASURABLE, EXPLAINABLE, TEMPORALLY CORRECT, ZERO-PAID-API, PORTFOLIO-GRADE FINANCIAL AI ENGINEERING SYSTEM.

Start implementation now.

from filingsgraph.security.limits import validate_query_limits
from filingsgraph.security.prompt_injection import detect_prompt_injection

def validate_user_query(question:str)->dict:
    validate_query_limits(question)
    return detect_prompt_injection(question)

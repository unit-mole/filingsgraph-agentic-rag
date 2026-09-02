from filingsgraph.temporal.risk_diff import compare_risk_disclosures

def compare_risk_disclosure_text(old_text:str,new_text:str,topics:list[str])->list[dict]: return compare_risk_disclosures(old_text,new_text,topics)
def find_new_risks(changes:list[dict])->list[dict]: return [x for x in changes if x.get('change_type')=='NEW']
def find_removed_risks(changes:list[dict])->list[dict]: return [x for x in changes if x.get('change_type')=='REMOVED']
def find_changed_language(changes:list[dict])->list[dict]: return [x for x in changes if x.get('change_type') in {'NEW','EXPANDED','REDUCED','REMOVED'}]

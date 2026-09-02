from filingsgraph.sec.client import SECClient

def main():
    c=SECClient(); data=c.get_json('https://data.sec.gov/submissions/CIK0000320193.json'); print({'ok':True,'name':data.get('name'),'cik':data.get('cik'),'rate_limit_rps':c.settings.sec_requests_per_second})
if __name__=='__main__': main()

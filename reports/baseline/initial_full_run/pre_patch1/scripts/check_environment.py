from __future__ import annotations
import json,platform,sys,subprocess
from pathlib import Path

def main():
    report={"python":sys.version,"platform":platform.platform(),"executable":sys.executable}
    try:
        import torch
        report.update({"torch":torch.__version__,"cuda_available":torch.cuda.is_available(),"cuda_version":torch.version.cuda,"gpu":torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,"bf16_supported":torch.cuda.is_bf16_supported() if torch.cuda.is_available() else False,"vram_gb":round(torch.cuda.get_device_properties(0).total_memory/1024**3,2) if torch.cuda.is_available() else 0})
    except Exception as e: report["torch_error"]=str(e)
    try:
        r=subprocess.run(['docker','version','--format','{{.Server.Version}}'],capture_output=True,text=True,timeout=10); report['docker_server']=r.stdout.strip() if r.returncode==0 else None; report['docker_error']=r.stderr.strip() if r.returncode else None
    except Exception as e: report['docker_error']=str(e)
    p=Path('reports/final/environment.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__': main()

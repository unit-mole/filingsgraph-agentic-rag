from __future__ import annotations
import requests
from filingsgraph.core.config import get_settings
from filingsgraph.llm.base import ModelProvider

class LocalTransformersProvider(ModelProvider):
    def __init__(self,model_name:str|None=None,device:str|None=None):
        import torch
        from transformers import AutoTokenizer,AutoModelForCausalLM
        s=get_settings(); self.model_name=model_name or s.local_llm_model; self.device=device or s.device
        self.tokenizer=AutoTokenizer.from_pretrained(self.model_name)
        dtype=torch.bfloat16 if self.device.startswith('cuda') and torch.cuda.is_available() else torch.float32
        self.model=AutoModelForCausalLM.from_pretrained(self.model_name,torch_dtype=dtype,device_map='auto' if self.device.startswith('cuda') else None)
    def generate(self,messages:list[dict],max_new_tokens:int=1400,temperature:float=0.2,**kwargs)->str:
        import torch
        inputs=self.tokenizer.apply_chat_template(messages,add_generation_prompt=True,tokenize=True,return_dict=True,return_tensors='pt')
        inputs={k:v.to(self.model.device) for k,v in inputs.items()}
        with torch.inference_mode():
            out=self.model.generate(**inputs,max_new_tokens=max_new_tokens,do_sample=temperature>0,temperature=max(temperature,1e-5))
        n=inputs['input_ids'].shape[-1]
        return self.tokenizer.decode(out[0][n:],skip_special_tokens=True).strip()

class OpenAICompatibleLocalProvider(ModelProvider):
    def __init__(self,base_url:str|None=None,model:str|None=None):
        s=get_settings(); self.base=(base_url or s.local_llm_base_url).rstrip('/'); self.model=model or s.local_llm_model
    def generate(self,messages:list[dict],max_new_tokens:int=1400,temperature:float=0.2,**kwargs)->str:
        r=requests.post(f"{self.base}/chat/completions",json={"model":self.model,"messages":messages,"max_tokens":max_new_tokens,"temperature":temperature},timeout=180)
        r.raise_for_status(); return r.json()['choices'][0]['message']['content']

def get_local_provider():
    s=get_settings()
    return OpenAICompatibleLocalProvider() if s.local_llm_backend in {'vllm','openai_compatible','ollama_openai'} else LocalTransformersProvider()

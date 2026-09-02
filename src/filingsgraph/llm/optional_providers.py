from filingsgraph.core.config import get_settings

def commercial_provider(name:str):
    s=get_settings()
    if not s.enable_commercial_models:
        raise RuntimeError('Commercial providers are disabled. Set ENABLE_COMMERCIAL_MODELS=true explicitly for optional benchmarking.')
    raise NotImplementedError(f'{name} adapter is intentionally optional; the core application does not require it.')

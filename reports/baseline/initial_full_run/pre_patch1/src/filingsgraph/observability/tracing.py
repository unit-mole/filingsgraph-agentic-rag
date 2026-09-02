from __future__ import annotations
from contextlib import contextmanager
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

def configure_tracing(endpoint:str|None=None):
    provider=TracerProvider(); trace.set_tracer_provider(provider)
    if endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
        except Exception: pass
    return trace.get_tracer('filingsgraph')

@contextmanager
def span(name:str,**attrs):
    tracer=trace.get_tracer('filingsgraph')
    with tracer.start_as_current_span(name) as s:
        for k,v in attrs.items(): s.set_attribute(k,str(v))
        yield s

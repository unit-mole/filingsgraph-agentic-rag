from filingsgraph.llm.output import strip_reasoning

def test_strip_complete_think_block():
    assert strip_reasoning("<think>secret reasoning</think> Final answer [SEC-1].") == "Final answer [SEC-1]."

def test_strip_plain_answer_unchanged():
    assert strip_reasoning("Final answer") == "Final answer"

def test_truncated_think_returns_empty():
    assert strip_reasoning("<think>unfinished private reasoning") == ""

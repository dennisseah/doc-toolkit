import pytest

from evaluators.rouge import RougeScores, evaluate


@pytest.mark.unit
def test_evaluate():
    score = evaluate(result="it is sunny day", target="it is a sunny day")

    assert RougeScores(rouge1=1.0, rouge2=0.667, rougeL=1.0) == score

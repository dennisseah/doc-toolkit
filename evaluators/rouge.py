from pydantic import BaseModel
from rouge_score import rouge_scorer
from rouge_score.scoring import Score


class RougeScores(BaseModel):
    rouge1: float
    rouge2: float
    rougeL: float


def evaluate(result: str, target: str) -> RougeScores:
    """Adds ROUGE metrics to each item in results.

    :param result: The result to evaluate
    :param target: The target to evaluate against
    :return: rouge1, rouge2, rougeL scores
    """
    score_names = ["rouge1", "rouge2", "rougeL"]
    scorer = rouge_scorer.RougeScorer(score_names, use_stemmer=True)

    scores: dict[str, Score] = scorer.score(target, result)
    return RougeScores(
        rouge1=round(scores["rouge1"].precision, 3),
        rouge2=round(scores["rouge2"].precision, 3),
        rougeL=round(scores["rougeL"].precision, 3),
    )

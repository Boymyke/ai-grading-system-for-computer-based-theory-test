from pydantic import BaseModel, validator
from typing import List

class RubricCriterion(BaseModel):
    index: int
    criteria: str
    weight: float


class Rubric(BaseModel):
    criteria: List[RubricCriterion]
    
    @validator('criteria')
    def validate_weights_sum(cls, v):
        total_weight = sum(criterion.weight for criterion in v)
        if abs(total_weight - 1.0) > 0.001:
            raise ValueError(f"Sum of criterion weights must equal 1.0, got {total_weight}")
        return v

# Hard coded variables
LENIENT_RUBRIC = Rubric(criteria=[
    RubricCriterion(index=1, criteria="Has solid ideas relevant to every part of the question in a well explained manner.", weight=0.5),
    RubricCriterion(index=2, criteria="Does not contain inaccurate or irrelvant points.", weight=0.2),
    RubricCriterion(index=3, criteria="Contains at least one key point related to the model answer (even if phrased differently). If model answer isn't provided, answer contains at least two relevant points related to the topic.", weight=0.3),
])

STRICT_RUBRIC = Rubric(criteria=[
    RubricCriterion(index=1, criteria="Has solid ideas relevant to every part of the question in a well explained manner.", weight=0.4),
    RubricCriterion(index=2, criteria="Answer is highly related to the model answer (even if phrased differently). If model answer isn't provided, answer contains at least three relevant points related to the topic.", weight=0.4),
    RubricCriterion(index=3, criteria="Uses correct terminology related to the question", weight=0.2),
])
from pydantic import BaseModel
from typing import List



class ConceptualUnderstanding(BaseModel):
    summary: str  # Concise definition or main idea
    step_by_step_explanation: List[str]  # Break down of concept
    analogy_or_example: str  # Real-world comparison or analogy
    key_terms: List[str]  # Important terminology to know
    optional_visual_description: str  # What a diagram/image might include to visualize this concept
    
    
    
class ProblemSolving(BaseModel):
    problem_restatement: str  # Rephrase of the problem for clarity
    assumptions: List[str]  # Any given or inferred assumptions
    step_by_step_solution: List[str]  # Detailed steps to solve
    final_answer_or_output: str  # Final result or recommendation
    common_pitfalls: List[str]  # Mistakes to avoid
    optional_visual_description: str  # Suggested diagram or visual for understanding
    
    
class AppliedGuidance(BaseModel):
    goal_or_use_case: str  # What the user wants to achieve
    prerequisites: List[str]  # Skills, tools, or knowledge needed
    recommended_approach: str  # Suggested method or strategy
    actionable_steps: List[str]  # To-do list or project roadmap
    timeline_or_phases: List[str]  # If applicable, high-level breakdown
    risks_or_warnings: List[str]  # Things to watch out for
    optional_visual_description: str  # Sketch/diagram suggestion
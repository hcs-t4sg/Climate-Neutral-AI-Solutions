from typing import Optional, Literal
from langchain.pydantic_v1 import BaseModel
from langchain.chains import create_extraction_chain_pydantic
from langchain.chat_models import ChatOpenAI
import secret
from scope_defns import SCOPE_DEFNS

# Pydantic data class
class CompanyProperties(BaseModel):
    scope: list[Literal[tuple(SCOPE_DEFNS.keys())]]
    description: str
    goal_hint: str

    @staticmethod
    def new() -> "CompanyProperties":
        return CompanyProperties(scope=[], description="", goal_hint="")

    def __add__(self, other: "CompanyProperties") -> "CompanyProperties":
        new_scope = list(set(self.scope).union(set(other.scope)))
        new_description = f"{self.description} {other.description}"
        new_goal_hint = f"{self.goal_hint} {other.goal_hint}"
        return CompanyProperties(scope=new_scope, description=new_description, goal_hint=new_goal_hint)

llm = ChatOpenAI(openai_api_key=secret.OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0.1)
        
# Extraction
chain = create_extraction_chain_pydantic(pydantic_schema=CompanyProperties, llm=llm)

# Run 
inp = """
We are a sports supply company concerned about scope 1, 2, and 3.7 emissions.

We primarily make protective equipment (i.e. helmets, padding) for football and hockey.

Our goal is to find better ways to source our materials.
"""

def clean_inp(inp_str: str):
    """Removes newlines and annoying stuff so pydantic works properly"""
    return inp_str.replace("\n", " ")

def clean_outs(outs: list[CompanyProperties]):
    """Combines multiple outputs into a single output"""
    result = CompanyProperties.new()
    for prop in outs:
        result += prop
    return result


inp = clean_inp(inp)
outs = chain.run(input=inp, context="Only return a single Company Properties. Make the description and goal-hint human readable with proper punctation.")
outs = clean_outs(outs)
print(outs)

from typing import Optional, Literal
from langchain.pydantic_v1 import BaseModel
from langchain.chains import create_extraction_chain_pydantic
from langchain.chat_models import ChatOpenAI
import secret
from scope_defns import get_company_scopes, fake_company, SCOPE_DEFNS


def get_advice_prompt(copmany_description: str, specific: str):
    scopes = get_company_scopes(copmany_description)
    prompt_text = f"""
    Your goal is to provide actionable insights for reducing specific scopes of carbon emissions.

    The company describes themselves as follows:
    {copmany_description}

    They have given the following specific ideas:
    {specific}

    As a reminder, here are the explicit scopes relevant to this company:  
    """
    for scope in scopes:
        prompt_text += f"\n{scope}: {SCOPE_DEFNS[scope]}\n"
    prompt_text += """
    Please provide, in markdown formatting, a summary of ways that this company could reduce their carbon emissions, being sure to cite the specific scopes whenever relevant.
    """
    return prompt_text


llm = ChatOpenAI(
    openai_api_key=secret.OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0.1
)

advice_prompt = get_advice_prompt(fake_company, "")
text = llm.predict(advice_prompt)
with open("Advice.md", "w") as fout:
    fout.write(text)

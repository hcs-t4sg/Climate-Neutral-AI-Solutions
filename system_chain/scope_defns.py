from typing import Literal, Optional
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel
import secret
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain_pydantic

SCOPE_DEFNS = {
    "1": "Scope 1 emissions are direct greenhouse (GHG) emissions that occur from sources that are controlled or owned by an organization (e.g., emissions associated with fuel combustion in boilers, furnaces, vehicles).",
    "2": "Scope 2 emissions are indirect GHG emissions associated with the purchase of electricity, steam, heat, or cooling. Although scope 2 emissions physically occur at the facility where they are generated, they are accounted for in an organization’s GHG inventory because they are a result of the organization’s energy use.",
    "3.1": "This subcategory is for purchased goods and services. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
    "3.2": "This subcategory is for capital goods. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
    "3.3": "This subcategory is for fuel and energy. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
    "3.4": "This subcategory is for upstream transportation and distribution. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
    "3.5": "This subcategory is for operations waste. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
    "3.6": "This subcategory is for business travel. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
    "3.7": "This subcategory is for employee commuting. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
    "3.9": "This subcategory is for downstream transportation and distribution. Scope 3 emissions are the result of activities from assets not owned or controlled by the reporting organization, but that the organization indirectly affects in its value chain. Scope 3 emissions include all sources not within an organization’s scope 1 and 2 boundary.",
}

SCOPE_PROMPT_TEXT = (
    "As a reminder, here are the relevant definitions for scope emissions:\n"
)

for scope, desc in SCOPE_DEFNS.items():
    SCOPE_PROMPT_TEXT += f"\n{scope}: {desc}\n"

SCOPE_PROMPT_TEXT += """
You will be given the description of a company's products and their goal. Your task is to determine which scopes are relevant to the company's goal. You can choose as many scopes as you want, but you must choose at least one.

Description: {description}

Your response should simply be a comma separated list of numbers, i.e. 1, 2, 3.1, 3.2, 3.3, 3.4..., depending on which scopes apply.
"""
# Your response should be as concise as possible, listing each scope and a brief sentence on why it applies. For scope 3, be sure to list the subscopes (i.e. 3.1, 3.2, ...).

SCOPE_PROMPT = PromptTemplate(
    template=SCOPE_PROMPT_TEXT, input_variables=["description"]
)

llm = ChatOpenAI(
    openai_api_key=secret.OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0.1
)


def get_human_readable_scopes_str(company_desc: str) -> str:
    prompt_text = SCOPE_PROMPT.format(description=company_desc)
    return llm.predict(prompt_text)


class CompanyScope(BaseModel):
    scopes: list[str]

    @staticmethod
    def new() -> "CompanyScope":
        return CompanyScope(scopes=[])

    def __add__(self, other: "CompanyScope") -> "CompanyScope":
        new_scope = list(set(self.scopes).union(set(other.scopes)))
        return CompanyScope(
            scopes=new_scope,
        )


def clean_outs(outs: list[CompanyScope]):
    """Combines multiple outputs into a single output"""
    result = CompanyScope.new()
    for prop in outs:
        result += prop
    return result


def get_scopes_from_human_str(human_scopes: str) -> "CompanyScope":
    chain = create_extraction_chain_pydantic(pydantic_schema=CompanyScope, llm=llm)
    outs = chain.run(human_scopes)
    return clean_outs(outs)


def get_company_scopes(desc: str) -> list[str]:
    human_readable_scopes = get_human_readable_scopes_str(desc)
    comp = get_scopes_from_human_str(human_readable_scopes)
    return sorted([scope for scope in comp.scopes if scope in SCOPE_DEFNS])


fake_company = """
Company Name: EcoSport Producers

Description:
EcoSport Producers is a forward-thinking sports supplier company that places a strong emphasis on sustainability and environmental responsibility. The company specializes in various aspects of the sports industry, with a primary focus on production processes, materials sourcing, and a commitment to reducing emissions throughout the supply chain.

Production and Manufacturing:
EcoSport Producers leverages cutting-edge manufacturing techniques and technologies to produce high-quality sports equipment and gear. Their state-of-the-art facilities are designed with eco-friendliness in mind, incorporating energy-efficient machinery and production processes. This commitment to sustainable manufacturing includes:

Recycled Materials: The company utilizes recycled and sustainable materials whenever possible, minimizing the environmental impact of raw material extraction and reducing waste.

Energy Efficiency: EcoSport Producers employs energy-efficient equipment and lighting systems in their production facilities. They also invest in renewable energy sources to power their operations.

Reduced Waste: Waste reduction initiatives, such as recycling programs and innovative production techniques, ensure that material waste is minimized during the manufacturing process.

Emissions Reduction:
EcoSport Producers is dedicated to lowering emissions throughout its operations, thus contributing to a greener, more sustainable sports industry. Key initiatives include:

Carbon Offsetting: The company invests in carbon offset programs, such as reforestation and renewable energy projects, to counterbalance emissions associated with their manufacturing processes and transportation.

Green Transportation: EcoSport Producers works with transportation partners committed to reducing their carbon footprint. They optimize shipping routes and utilize low-emission vehicles whenever possible.

Eco-Friendly Packaging: The company uses eco-friendly packaging materials and practices to minimize waste and reduce emissions related to shipping and delivery.

Sustainability Partnerships: EcoSport Producers collaborates with organizations dedicated to sustainability and continually seeks out new ways to reduce emissions in their supply chain.

Innovation and Research:
EcoSport Producers invests in research and development to discover and implement cutting-edge, sustainable technologies. They are committed to staying at the forefront of eco-friendly sports equipment manufacturing and continuously seek ways to reduce their carbon footprint.

EcoSport Producers is more than just a sports supplier; it's a company that exemplifies a commitment to environmentally responsible practices, all while providing athletes and sports enthusiasts with top-quality gear. By focusing on sustainable production and emissions reduction, they are paving the way for a greener future in the world of sports equipment and gear.
"""

if __name__ == "__main__":
    res = get_company_scopes(fake_company)
    print(res)

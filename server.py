"""SchemeSaathi: a small MCP server for exploring Indian government schemes."""

import json
import re
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

mcp = FastMCP("SchemeSaathi")

PROJECT_DIR = Path(__file__).parent
SCHEMES_FILE = PROJECT_DIR / "schemes.json"
NOTES_FILE = PROJECT_DIR / "data" / "application_notes.json"


def load_schemes() -> list[dict[str, Any]]:
    """Load the local scheme catalog."""
    with SCHEMES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize(value: str) -> str:
    """Make a search string easier to compare."""
    return re.sub(r"\s+", " ", value.strip().lower())


def find_scheme(scheme_id_or_name: str) -> dict[str, Any] | None:
    """Find a scheme by ID or by part of its name."""
    wanted = normalize(scheme_id_or_name)
    for scheme in load_schemes():
        if wanted == normalize(scheme["id"]):
            return scheme
        if wanted in normalize(scheme["name"]):
            return scheme
    return None


def search_catalog(query: str = "", category: str = "") -> list[dict[str, Any]]:
    """Search the local catalog by words and/or category."""
    words = normalize(query).split()
    wanted_category = normalize(category)
    matches = []

    for scheme in load_schemes():
        searchable = normalize(
            " ".join([
                scheme["id"],
                scheme["name"],
                scheme["category"],
                scheme["summary"],
                " ".join(scheme["who_may_benefit"]),
            ])
        )
        if wanted_category and wanted_category != normalize(scheme["category"]):
            continue
        if words and not all(word in searchable for word in words):
            continue
        matches.append(scheme)

    return matches


@mcp.tool()
def search_schemes(query: str = "", category: str = "") -> dict[str, Any]:
    """Search the included scheme catalog by keywords or category.

    Categories currently include agriculture, health, and skill-and-business.
    This searches the local starter catalog, not every government scheme.
    """
    matches = search_catalog(query, category)
    return {
        "count": len(matches),
        "schemes": [
            {
                "id": item["id"],
                "name": item["name"],
                "category": item["category"],
                "summary": item["summary"],
                "official_url": item["official_url"],
            }
            for item in matches
        ],
        "note": "Starter catalog only. Verify current rules and availability on the official source.",
    }


@mcp.tool()
def get_scheme_details(scheme_id_or_name: str) -> dict[str, Any]:
    """Get the description, possible beneficiaries, documents to check, and official source for one scheme."""
    scheme = find_scheme(scheme_id_or_name)
    if not scheme:
        return {
            "error": "Scheme not found in the local catalog.",
            "available_schemes": [
                {"id": item["id"], "name": item["name"]}
                for item in load_schemes()
            ],
        }
    return scheme


@mcp.tool()
def check_eligibility(
    scheme_id_or_name: str,
    applicant_description: str,
) -> dict[str, Any]:
    """Give a preliminary, non-binding eligibility checklist from an applicant description.

    This is a keyword-based helper, not an official eligibility decision.
    """
    scheme = find_scheme(scheme_id_or_name)
    if not scheme:
        return {
            "error": "Scheme not found in the local catalog.",
            "available_schemes": [
                {"id": item["id"], "name": item["name"]}
                for item in load_schemes()
            ],
        }

    description = normalize(applicant_description)
    category = scheme["category"]
    questions = []

    if category == "agriculture":
        questions.extend([
            "Do you currently cultivate or hold eligible agricultural land, if required by this scheme?",
            "Are your land/cultivation records and bank details up to date?",
            "Does your state, district, crop, or bank have additional conditions for this scheme?",
        ])
    elif category == "health":
        questions.extend([
            "Can your eligibility be found in the current official beneficiary database?",
            "Have you checked the official portal or authorized help desk for the required identification details?",
        ])
    else:
        questions.extend([
            "Is your trade/occupation included in the current official list for this scheme?",
            "Do you meet the current age, family, and other scheme-specific conditions?",
            "Can you provide the identity and bank details requested by the official process?",
        ])

    hints = []
    if any(term in description for term in ["farmer", "farming", "agriculture", "cultivat", "kisan", "land"]):
        hints.append("Your description mentions farming or land; compare it with the scheme's exact rules.")
    if any(term in description for term in ["artisan", "craft", "weaver", "carpenter", "blacksmith", "potter"]):
        hints.append("Your description mentions a craft or trade; check whether it is a notified trade.")
    if any(term in description for term in ["low income", "poor", "income", "ration card"]):
        hints.append("Income or ration-card details alone may not establish eligibility; check the scheme's official criteria.")

    if not hints:
        hints.append("The description does not contain enough specific information for a useful match.")

    return {
        "scheme": scheme["name"],
        "preliminary_result": "Needs official verification",
        "observations": hints,
        "questions_to_check": questions,
        "official_url": scheme["official_url"],
        "important_note": (
            "This tool does not make an official eligibility decision and does not verify government records. "
            "Confirm current rules and your eligibility through the official source."
        ),
    }


@mcp.tool()
def prepare_application_checklist(scheme_id_or_name: str) -> dict[str, Any]:
    """Prepare a general document checklist for a scheme."""
    scheme = find_scheme(scheme_id_or_name)
    if not scheme:
        return {
            "error": "Scheme not found in the local catalog.",
            "available_schemes": [
                {"id": item["id"], "name": item["name"]}
                for item in load_schemes()
            ],
        }

    return {
        "scheme": scheme["name"],
        "checklist": [
            {"item": document, "checked": False}
            for document in scheme["documents_to_check"]
        ],
        "before_applying": [
            "Open the official source and confirm the latest rules and application window.",
            "Check whether your state, district, bank, or local office has additional requirements.",
            "Use only official portals or authorized offices; never share OTPs or passwords with an agent.",
            "Keep copies of submitted forms and any acknowledgment number.",
        ],
        "official_url": scheme["official_url"],
        "note": "This is a preparation checklist, not an official or exhaustive document list.",
    }


@mcp.resource("schemesaathi://guide")
def scheme_saathi_guide() -> str:
    """Explain what this MCP server can and cannot do."""
    return (
        "SchemeSaathi is a starter catalog of selected Indian government schemes. "
        "Use search_schemes to find entries, get_scheme_details to read one, "
        "check_eligibility for preliminary questions, and prepare_application_checklist "
        "to plan documents. It does not access government databases, submit applications, "
        "or guarantee eligibility. Always verify current information through the official source."
    )


@mcp.resource("schemesaathi://schemes")
def scheme_catalog_resource() -> str:
    """Return the full local catalog as JSON text."""
    return json.dumps(load_schemes(), indent=2, ensure_ascii=False)


@mcp.resource("schemesaathi://categories")
def scheme_categories_resource() -> str:
    """Return the categories currently present in the catalog."""
    categories = sorted({scheme["category"] for scheme in load_schemes()})
    return json.dumps({"categories": categories}, indent=2)


@mcp.prompt()
def find_schemes_for_me(
    state: str = "not specified",
    occupation: str = "not specified",
    goal: str = "not specified",
) -> str:
    """Prompt for discovering potentially relevant schemes."""
    return (
        "Help me explore schemes in the SchemeSaathi local catalog. "
        f"My state is {state}; my occupation is {occupation}; my goal is {goal}. "
        "Search the catalog, explain why each result may be relevant, list missing details, "
        "and link to official sources. Do not claim that I am eligible without verification."
    )


@mcp.prompt()
def explain_scheme(scheme_name: str) -> str:
    """Prompt for a beginner-friendly scheme explanation."""
    return (
        f"Explain {scheme_name} in simple language. Use SchemeSaathi's scheme details, "
        "summarize who may benefit, what conditions need checking, what documents may be needed, "
        "and where to verify the latest official information. Clearly label uncertainties."
    )


@mcp.prompt()
def check_my_eligibility(scheme_name: str, applicant_details: str) -> str:
    """Prompt for a preliminary eligibility review."""
    return (
        f"Help me do a preliminary checklist for {scheme_name}. My details: {applicant_details}. "
        "Use the SchemeSaathi tool, identify missing information, and give questions to verify. "
        "Do not present this as an official eligibility decision."
    )


@mcp.prompt()
def prepare_my_application(scheme_name: str) -> str:
    """Prompt for preparing an application."""
    return (
        f"Help me prepare for an application to {scheme_name}. Use the SchemeSaathi checklist, "
        "organize the steps in order, and link to the official source. Do not invent requirements "
        "or say the application has been submitted."
    )


if __name__ == "__main__":
    mcp.run()

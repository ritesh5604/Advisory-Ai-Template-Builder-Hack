def build_prompt(section_title, client, original_text):
    objectives = ", ".join(client["primary_objectives"])

    return f"""
You are writing content for a UK financial suitability report.

Section: {section_title}

Existing Template Text:
{original_text}

Client Context:
- Name: {client['client_name']}
- Employment: {client['employment']}
- Risk Profile: {client['risk_profile']}
- Objectives: {objectives}
- Investment Horizon: {client['investment_horizon']}

Rewrite the existing text with client-specific detail.
Do not include numbers, tables, guarantees, or compliance language.
"""

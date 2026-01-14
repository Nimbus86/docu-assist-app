# app/prompts.py
SUMMARIZE_PROMPT = """
Je bent een ervaren contractjurist. Lees de volgende contracttekst en geef:
1) Korte samenvatting max 6 zinnen.
2) Belangrijkste verplichtingen per partij als bullets.
3) Kerndata en bedragen als bullets.
4) Korte onduidelijkheden.

Contracttekst:
{{CONTRACT_TEXT}}
"""

from langchain_groq import ChatGroq
from app.config import settings


def get_llm(use_fallback: bool = False) -> ChatGroq:
    """
    Returns a ChatGroq client.
    Primary model: gemma2-9b-it (fast, cheap - good for structured extraction).
    Fallback model: llama-3.3-70b-versatile (used if the primary errors out,
    or if you want stronger reasoning for the conversational planner).
    """
    model = settings.groq_fallback_model if use_fallback else settings.groq_model
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=model,
        temperature=0.2,
    )


def call_llm(prompt: str, system: str = "") -> str:
    """Simple helper: single-turn call with automatic fallback on failure."""
    messages = []
    if system:
        messages.append(("system", system))
    messages.append(("human", prompt))

    try:
        llm = get_llm(use_fallback=False)
        return llm.invoke(messages).content
    except Exception:
        llm = get_llm(use_fallback=True)
        return llm.invoke(messages).content

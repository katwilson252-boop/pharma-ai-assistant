import json

from fastapi import APIRouter
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from app.agent.graph import agent_app
from app.schemas import ChatMessage, ChatResponse

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
)


@router.post("", response_model=ChatResponse)
def chat(payload: ChatMessage):
    user_text = payload.message

    if payload.interaction_id:
        user_text += (
            f"\n(Context: this refers to interaction_id={payload.interaction_id})"
        )

    result = agent_app.invoke(
        {
            "messages": [
                HumanMessage(content=user_text)
            ]
        }
    )

    messages = result["messages"]

    tool_calls_used = []
    interaction = None

    for message in messages:
        if isinstance(message, ToolMessage):

            tool_calls_used.append(message.name)

            if message.name == "log_interaction":
                try:
                    interaction = json.loads(message.content)
                except Exception:
                    interaction = None

    final_reply = next(
        (
            message.content
            for message in reversed(messages)
            if isinstance(message, AIMessage) and message.content
        ),
        "Done.",
    )

    return ChatResponse(
        reply=final_reply,
        tool_calls=tool_calls_used,
        interaction=interaction,
    )
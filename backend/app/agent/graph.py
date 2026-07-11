from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage

from app.agent.llm import get_llm
from app.agent.tools import ALL_TOOLS

SYSTEM_PROMPT = """You are the AI assistant embedded in the HCP CRM "Log Interaction"
screen for a pharma field representative. Your job is to help the rep log,
edit, and understand their interactions with healthcare professionals (HCPs)
through natural conversation, instead of filling out the form manually.

You have five tools:
- log_interaction: use this whenever the rep describes a new interaction in free text.
- edit_interaction: use this when the rep wants to correct/update an existing logged interaction (needs the interaction id).
- get_hcp_history: use this to pull prior interaction history for context before logging or advising.
- suggest_followups: use this to propose next steps after an interaction is described.
- check_compliance_flags: use this to check an interaction for compliance concerns before finalizing.

Be concise, professional, and proactive - e.g. after logging an interaction,
offer to suggest follow-ups. Always confirm back to the rep what was logged."""


def build_agent_graph():
    llm = get_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    def call_model(state: MessagesState):
        messages = state["messages"]
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def should_continue(state: MessagesState):
        last = state["messages"][-1]
        if getattr(last, "tool_calls", None):
            return "tools"
        return END

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(ALL_TOOLS))
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


# Compile once at import time and reuse across requests.
agent_app = build_agent_graph()

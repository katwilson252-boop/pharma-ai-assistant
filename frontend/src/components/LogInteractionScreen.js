import React from "react";
import InteractionForm from "./InteractionForm";
import ChatAssistant from "./ChatAssistant";

export default function LogInteractionScreen() {
  return (
    <div className="app-shell">
      <div className="screen-title">Log HCP Interaction</div>
      <div className="layout">
        <InteractionForm />
        <ChatAssistant />
      </div>
    </div>
  );
}

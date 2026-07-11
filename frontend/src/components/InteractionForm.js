import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { updateField, submitInteraction, resetForm } from "../redux/interactionSlice";

const listField = (value) => (Array.isArray(value) ? value.join(", ") : value);
const parseList = (str) =>
  str.split(",").map((s) => s.trim()).filter(Boolean);

export default function InteractionForm() {
  const dispatch = useDispatch();
  const { form, status } = useSelector((s) => s.interaction);

  const set = (field) => (e) => dispatch(updateField({ field, value: e.target.value }));
  const setList = (field) => (e) =>
    dispatch(updateField({ field, value: parseList(e.target.value) }));

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(submitInteraction(form));
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h3>Interaction Details</h3>

      <div className="row-2">
        <div className="field">
          <label>HCP Name</label>
          <input value={form.hcp_name} onChange={set("hcp_name")} placeholder="Search or select HCP..." required />
        </div>
        <div className="field">
          <label>Interaction Type</label>
          <select value={form.interaction_type} onChange={set("interaction_type")}>
            <option>Meeting</option>
            <option>Call</option>
            <option>Email</option>
            <option>Conference</option>
          </select>
        </div>
      </div>

      <div className="field">
        <label>Attendees (comma separated)</label>
        <input value={listField(form.attendees)} onChange={setList("attendees")} placeholder="Enter names or search..." />
      </div>

      <div className="field">
        <label>Topics Discussed</label>
        <textarea rows={3} value={form.topics_discussed} onChange={set("topics_discussed")} placeholder="Enter key discussion points..." />
      </div>

      <div className="field">
        <label>Materials Shared (comma separated)</label>
        <input value={listField(form.materials_shared)} onChange={setList("materials_shared")} placeholder="e.g. Product X brochure" />
      </div>

      <div className="field">
        <label>Samples Distributed (comma separated)</label>
        <input value={listField(form.samples_distributed)} onChange={setList("samples_distributed")} placeholder="e.g. OncoBoost sample pack" />
      </div>

      <div className="field">
        <label>Observed / Inferred HCP Sentiment</label>
        <div className="sentiment-options">
          {["Positive", "Neutral", "Negative"].map((opt) => (
            <label key={opt}>
              <input
                type="radio"
                name="sentiment"
                checked={form.sentiment === opt}
                onChange={() => dispatch(updateField({ field: "sentiment", value: opt }))}
              />
              {opt}
            </label>
          ))}
        </div>
      </div>

      <div className="field">
        <label>Outcomes</label>
        <textarea rows={2} value={form.outcomes} onChange={set("outcomes")} placeholder="Key outcomes or agreements..." />
      </div>

      <div className="field">
        <label>Follow-up Actions (comma separated)</label>
        <textarea rows={2} value={listField(form.follow_up_actions)} onChange={setList("follow_up_actions")} placeholder="Enter next steps or tasks..." />
      </div>

      <button className="btn" type="submit" disabled={status === "saving"}>
        {status === "saving" ? "Logging..." : "Log Interaction"}
      </button>
      <button
        type="button"
        className="btn secondary"
        style={{ marginLeft: 8 }}
        onClick={() => dispatch(resetForm())}
      >
        Clear
      </button>
    </form>
  );
}

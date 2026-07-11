import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { api } from "../api/client";

const initialForm = {
  hcp_name: "",
  interaction_type: "Meeting",
  attendees: [],
  topics_discussed: "",
  materials_shared: [],
  samples_distributed: [],
  sentiment: "Neutral",
  outcomes: "",
  follow_up_actions: [],
};

export const submitInteraction = createAsyncThunk(
  "interaction/submit",
  async (formData) => api.createInteraction(formData)
);

export const sendChatMessage = createAsyncThunk(
  "interaction/sendChatMessage",
  async ({ message, interactionId }) => api.sendChatMessage(message, interactionId)
);

const interactionSlice = createSlice({
  name: "interaction",
  initialState: {
    form: initialForm,
    lastSaved: null,
    chatMessages: [
      {
        role: "assistant",
        text: 'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.',
      },
    ],
    suggestedFollowUps: [],
    status: "idle",
    error: null,
  },
  reducers: {
    updateField(state, action) {
      const { field, value } = action.payload;
      state.form[field] = value;
    },
    resetForm(state) {
      state.form = initialForm;
    },
    addUserChatMessage(state, action) {
      state.chatMessages.push({ role: "user", text: action.payload });
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(submitInteraction.pending, (state) => {
        state.status = "saving";
      })
      .addCase(submitInteraction.fulfilled, (state, action) => {
        state.status = "idle";
        state.lastSaved = action.payload;
        state.form = initialForm;
      })
      .addCase(submitInteraction.rejected, (state, action) => {
        state.status = "idle";
        state.error = action.error.message;
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        const { reply, tool_calls } = action.payload;
        state.chatMessages.push({
          role: "assistant",
          text: reply,
          toolCalls: tool_calls,
        });
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.chatMessages.push({
          role: "assistant",
          text: `Sorry, something went wrong: ${action.error.message}`,
        });
      });
  },
});

export const { updateField, resetForm, addUserChatMessage } = interactionSlice.actions;
export default interactionSlice.reducer;

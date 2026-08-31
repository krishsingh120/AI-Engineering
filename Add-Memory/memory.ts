import "dotenv/config";

import {
  AIMessage,
  HumanMessage,
  SystemMessage,
} from "@langchain/core/messages";

import {
  ChatPromptTemplate,
  MessagesPlaceholder,
} from "@langchain/core/prompts";

import { ChatOpenAI } from "@langchain/openai";

// -------------------------
// LLM
// -------------------------

const model = new ChatOpenAI({
  model: "gpt-4o-mini",
});

// -------------------------
// Prompt
// -------------------------

const prompt = ChatPromptTemplate.fromMessages([
  new SystemMessage(
    "You are a helpful assistant. Answer all questions to the best of your ability.",
  ),

  new MessagesPlaceholder("messages"),
]);

const chain = prompt.pipe(model);

// -------------------------
// Summarize history
// -------------------------

async function summarizeChatHistory(chatHistory: (HumanMessage | AIMessage)[]) {
  if (chatHistory.length < 4) {
    return "";
  }

  const summaryPrompt = new HumanMessage(
    "Distill the above chat messages into a single summary message. " +
      "Include as many specific details as you can.",
  );

  const response = await chain.invoke({
    messages: [...chatHistory, summaryPrompt],
  });

  return response.content;
}

// -------------------------
// Chat
// -------------------------

async function chatWithModel(
  query: string,
  chatHistory: (HumanMessage | AIMessage)[],
  debugMode = false,
) {
  let messages: (HumanMessage | AIMessage | SystemMessage)[];

  // If history is large → summarize
  if (chatHistory.length >= 4) {
    console.log("Summarizing chat history...");

    const summary = await summarizeChatHistory(chatHistory);

    messages = [
      new SystemMessage(`Previous conversation summary:\n${summary}`),
      new HumanMessage(query),
    ];
  }

  // Otherwise → send complete history
  else {
    messages = [...chatHistory, new HumanMessage(query)];
  }

  if (debugMode) {
    console.log("\nMessages sent to LLM:");
    console.log(messages);
  }

  // Call LLM
  const response = await chain.invoke({
    messages,
  });

  // Save conversation
  chatHistory.push(new HumanMessage(query));

  chatHistory.push(new AIMessage(response.content));

  return response;
}

// -------------------------
// Test
// -------------------------

async function main() {
  const chatHistory: (HumanMessage | AIMessage)[] = [];

  const response1 = await chatWithModel(
    "Can you explain Dynamic Programming under 50 words?",
    chatHistory,
    true,
  );

  console.log("\nAI:", response1.content);

  const response2 = await chatWithModel(
    "Can you explain Graph data structures under 50 words?",
    chatHistory,
    true,
  );

  console.log("\nAI:", response2.content);

  const response3 = await chatWithModel(
    "Can you tell me what did I ask till now?",
    chatHistory,
    true,
  );

  console.log("\nAI:", response3.content);
}

main();

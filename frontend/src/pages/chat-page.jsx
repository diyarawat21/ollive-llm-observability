import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8001";

export default function ChatPage() {
    const [conversationId, setConversationId] = useState(null);
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [conversations, setConversations] = useState([]);
    const [selectedConversation, setSelectedConversation] = useState(null);

    useEffect(() => {
        fetchConversations();
    }, []);

    const fetchConversations = async () => {
        try {
            const res = await axios.get(`${API}/conversations`);
            setConversations(res.data);
        } catch (err) {
            console.log(err);
        }
    };

    const createConversation = async () => {
        try {
            const res = await axios.post(`${API}/conversations`, {
                title: `Chat ${conversations.length + 1}`,
            });

            setConversationId(res.data.id);
            setSelectedConversation(res.data.id);
            setMessages([]);

            await fetchConversations();

            setError("");
        } catch {
            setError(
                "Could not connect to backend. Is uvicorn running on port 8001?"
            );
        }
    };

    const loadConversation = async (id) => {
        try {
            const res = await axios.get(
                `${API}/conversations/${id}/messages`
            );

            setMessages(res.data);
            setConversationId(id);
            setSelectedConversation(id);

        } catch (err) {
            console.log(err);
        }
    };

    const sendMessage = async () => {
        if (!message.trim() || !conversationId || loading) return;

        const userMessage = {
            role: "user",
            content: message,
        };

        setMessages((prev) => [...prev, userMessage]);

        const currentMessage = message;

        setMessage("");
        setLoading(true);
        setError("");

        try {
            const res = await axios.post(`${API}/chat`, {
                conversation_id: conversationId,
                message: currentMessage,
            });

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: res.data.response,
                },
            ]);

        } catch (err) {
            const detail =
                err.response?.data?.detail ||
                "Chat request failed. Check backend logs.";

            setError(
                typeof detail === "string"
                    ? detail
                    : JSON.stringify(detail)
            );

        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="h-screen bg-slate-950 text-white flex">

            {/* SIDEBAR */}
            <div className="w-[280px] bg-slate-900 border-r border-slate-700 flex flex-col p-5">

                <div className="text-2xl font-bold mb-6">
                    Ollive AI
                </div>

                <button
                    onClick={createConversation}
                    className="bg-blue-600 hover:bg-blue-700 transition rounded-xl py-3 font-semibold mb-5"
                >
                    + New Chat
                </button>

                <div className="flex-1 overflow-y-auto space-y-3">
                    {conversations.map((conv) => (
                        <div
                            key={conv.id}
                            onClick={() => loadConversation(conv.id)}
                            className={`p-3 rounded-xl cursor-pointer transition-all duration-200
                                ${
                                    selectedConversation === conv.id
                                        ? "bg-blue-600"
                                        : "bg-slate-800 hover:bg-slate-700"
                                }`}
                        >
                            {conv.title}
                        </div>
                    ))}
                </div>
            </div>

            {/* CHAT AREA */}
            <div className="flex-1 flex flex-col">

                {/* HEADER */}
                <div className="px-6 py-5 border-b border-slate-700 bg-slate-900 flex items-center justify-between">
                    <h1 className="text-2xl font-bold">
                        Ollive LLM Observability
                    </h1>

                    <div className="text-sm text-slate-400">
                        OpenRouter + FastAPI
                    </div>
                </div>

                {/* ERROR */}
                {error && (
                    <div className="mx-5 mt-4 bg-red-900/60 border border-red-700 text-red-200 p-4 rounded-xl">
                        {error}
                    </div>
                )}

                {/* MESSAGES */}
                <div className="flex-1 overflow-y-auto px-6 py-5 space-y-5">

                    {messages.length === 0 && (
                        <div className="h-full flex items-center justify-center text-slate-500 text-lg">
                            Start a conversation with Ollive AI ✨
                        </div>
                    )}

                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`flex ${
                                msg.role === "user"
                                    ? "justify-end"
                                    : "justify-start"
                            }`}
                        >
                            <div
                                className={`max-w-[75%] px-5 py-4 rounded-2xl text-[15px] leading-7 shadow-lg
                                    ${
                                        msg.role === "user"
                                            ? "bg-blue-600"
                                            : "bg-slate-800 border border-slate-700"
                                    }`}
                            >
                                {msg.content}
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="text-slate-400 animate-pulse">
                            AI is typing...
                        </div>
                    )}
                </div>

                {/* INPUT */}
                <div className="p-5 border-t border-slate-700 bg-slate-900 flex gap-3">

                    <input
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={(e) =>
                            e.key === "Enter" && sendMessage()
                        }
                        placeholder={
                            conversationId
                                ? "Type your message..."
                                : "Create a new chat first..."
                        }
                        disabled={!conversationId || loading}
                        className="flex-1 bg-slate-800 border border-slate-700 rounded-2xl px-5 py-4 outline-none focus:border-blue-500 text-white"
                    />

                    <button
                        onClick={sendMessage}
                        disabled={!conversationId || loading}
                        className={`px-6 rounded-2xl font-semibold transition
                            ${
                                loading
                                    ? "bg-slate-700 cursor-not-allowed"
                                    : "bg-blue-600 hover:bg-blue-700"
                            }`}
                    >
                        {loading ? "..." : "Send"}
                    </button>
                </div>
            </div>
        </div>
    );
}
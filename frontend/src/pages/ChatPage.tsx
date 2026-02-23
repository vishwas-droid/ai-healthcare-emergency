import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";

import { apiClient } from "../lib/apiClient";

type Message = {
  id?: number;
  sender_type: string;
  message: string;
  file_url?: string;
};

export function ChatPage() {
  const { doctorId } = useParams();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState("");
  const wsRef = useRef<WebSocket | null>(null);

  const loadMessages = async (sid: number) => {
    const { data } = await apiClient.get<Message[]>(`/chat/${sid}/messages`);
    setMessages(data);
  };

  useEffect(() => {
    const init = async () => {
      if (!doctorId) return;
      const { data } = await apiClient.post<{ id: number }>("/chat/session", {
        doctor_id: Number(doctorId),
        user_name: "Emergency User",
      });
      setSessionId(data.id);
      await loadMessages(data.id);

      const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
      const wsUrl = apiUrl.replace("http://", "ws://").replace("https://", "wss://");
      const ws = new WebSocket(`${wsUrl}/chat/ws/${data.id}`);
      ws.onmessage = (event) => {
        const payload = JSON.parse(event.data) as Message;
        setMessages((prev) => [...prev, payload]);
      };
      wsRef.current = ws;
    };

    init();
    return () => wsRef.current?.close();
  }, [doctorId]);

  const send = async () => {
    if (!sessionId || !text.trim()) return;

    const payload = {
      sender_type: "USER",
      message: text,
    };

    await apiClient.post(`/chat/${sessionId}/message`, payload);
    wsRef.current?.send(JSON.stringify(payload));
    setText("");
  };

  return (
    <section>
      <h2 className="text-3xl font-extrabold">Doctor Chat</h2>
      <div className="mt-4 rounded-2xl bg-white p-4 shadow-premium">
        <div className="h-96 space-y-2 overflow-auto rounded-xl border p-3">
          {messages.map((m, i) => (
            <div
              key={`${m.id ?? "ws"}-${i}`}
              className={`max-w-xl rounded-lg px-3 py-2 text-sm ${m.sender_type === "USER" ? "ml-auto bg-primary text-white" : "bg-slate-100"}`}
            >
              {m.message}
              {m.file_url && (
                <a className="ml-2 underline" href={m.file_url}>
                  File
                </a>
              )}
            </div>
          ))}
        </div>
        <div className="mt-3 flex gap-2">
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type message"
            className="flex-1 rounded-lg border px-3 py-2"
          />
          <button onClick={send} className="rounded-lg bg-primary px-4 py-2 font-semibold text-white">
            Send
          </button>
        </div>
      </div>
    </section>
  );
}

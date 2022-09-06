import React, { FC, useEffect, useRef, useState } from "react";
import {handleSession, sessionErrorHandler} from "./auth/sessionHandler";
import { MessageBubble } from "./chat/MessageBubble";
import { MessageInput } from "./chat/MessageInput";
import { getApiKey } from "./auth/authService";

interface Message {
  text: string;
  isSender: boolean;
}

const ENDPOINT_API =
  process.env.RENDER_EXTERNAL_URL ||
  process.env.CHATTERBOT_API ||
  "http://localhost:8000";

const CHATTERBOT_API_URL = `${ENDPOINT_API}/api/chatterbot/`;

export const App: FC = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesBottom = useRef(null);

  /**
   * Mostra l'ultimo messaggio ricevuto, scrollando fino alla sua posizione
   */
  function scrollToLatestMessage(): void {
    if (messagesBottom.current)
      messagesBottom.current.scrollIntoView({
        behavior: "smooth",
        block: "end",
        inline: "nearest",
      });
  }

  /**
   * Ottiene e salva il messaggio introduttivo dal server
   */
  function getFirstMessage(): void {
    fetch(CHATTERBOT_API_URL)
      .then((res) => res.json())
      .then(
        (result) => {
          setMessages([...messages, { text: result.text, isSender: false }]);
        },
        (error) => {
          console.error("error", error);
        }
      );
  }

  /**
   * Gestisce l'invio del messaggio dell'utente al server chatterbot 
   * fornendo inoltre l'API KEY usata come metodo di autenticazione qualora presente
   */
  function handleSubmit(): void {
    const API_KEY = getApiKey();

    fetch(CHATTERBOT_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: message,
        api_key: API_KEY
      })
    })
      .then((res) => res.json())
      .then(
        (result) => {
          handleSession(result.text, message);
          sessionErrorHandler(result.text);
          setMessages([
            ...messages,
            {
              text: message,
              isSender: true
            },
            { text: result.text, isSender: false },
          ]);
          setMessage("");
        },
        (error) => {
          console.error("error", error);
        }
      );
  }

  useEffect(() => {
    getFirstMessage();
  }, []);

  useEffect(() => {
    scrollToLatestMessage();
  }, [messages]);

  return (
    <>
      <div className="flex flex-col h-screen w-screen bg-white">
        <div
          id="chat"
          className="flex flex-col mt-2 overflow-y-auto space-y-3 mb-20 pb-3"
        >
          {messages.map((message, index) => (
            <MessageBubble
              key={index}
              text={message.text}
              isSender={message.isSender}
            />
          ))}
          <div ref={messagesBottom} />
        </div>

        <MessageInput
          message={message}
          onChange={(event) => setMessage(event.target.value)}
          onSubmit={handleSubmit}
        />
      </div>
    </>
  );
};

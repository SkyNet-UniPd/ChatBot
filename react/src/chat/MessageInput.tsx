import React, { FC } from "react";

export interface MessageInputProps {
  message: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: () => void;
}

export const MessageInput: FC<MessageInputProps> = ({
  message,
  onChange,
  onSubmit,
  ...props
}) => {
  return (
    <form
      {...props}
      className="flex flex-row  items-center bottom-0 my-2 w-full fixed"
      onSubmit={(e) => {
        e.preventDefault();
        if (message !== "") onSubmit();
      }}
    >
      <div className="ml-2 mr-2 flex flex-row border-gray items-center w-full border rounded-3xl h-12 px-2 ">
        <label className="hidden" htmlFor="message">
          Messaggio da inviare:
        </label>
        <input
          type="text"
          id="message"
          className="pl-4 border rounded-2xl border-transparent w-full focus:outline-none text-sm h-10 flex items-center"
          placeholder="Scrivi il tuo messaggio...."
          value={message}
          onChange={onChange}
        />
      </div>
      <button
        id="other"
        className="mr-2 flex items-center justify-center min-h-[40px] min-w-[40px] rounded-full bg-blue-500 text-white focus:outline-none disabled:opacity-50"
        type="submit"
        disabled={message === ""}
        aria-label="Invia il messaggio"
      >
        <svg
          className="w-5 h-5 transform rotate-90 -mr-px"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
          ></path>
        </svg>
      </button>
    </form>
  );
};

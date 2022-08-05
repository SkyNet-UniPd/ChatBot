import React, { FC } from "react";

interface MessageInputProps {
  message: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: () => void;
}

export const MessageInput: FC<MessageInputProps> = ({
  message,
  onChange,
  onSubmit,
}) => {
  return (
    <form
      className="flex flex-row  items-center bottom-0 my-2 w-full fixed"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
    >
      <div className="ml-2 flex flex-row border-gray items-center w-full border rounded-3xl h-12 px-2 ">
        <input
          type="text"
          id="message"
          className="pl-4 border rounded-2xl border-transparent w-full focus:outline-none text-sm h-10 flex items-center"
          placeholder="Type your message...."
          value={message}
          onChange={onChange}
        />
      </div>
      <button
        id="other"
        className="mx-4  flex items-center justify-center h-10 w-10 rounded-full bg-blue-500 text-white focus:outline-none"
        type="submit"
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

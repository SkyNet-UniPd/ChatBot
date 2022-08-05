import React, { FC, ReactNode } from "react";

interface MessageBubbleProps {
  text: ReactNode;
  isSender?: boolean;
}

export const MessageBubble: FC<MessageBubbleProps> = ({
  text,
  isSender,
  ...props
}) => {
  return (
    <>
      <div
        className={`normal-case m-2 p-2 rounded-2xl w-1/3 ${
          isSender
            ? " bg-blue-500 text-white ml-auto rounded-br-none"
            : "bg-gray-300  text-black mr-auto rounded-bl-none"
        } `}
      >
        {text}
      </div>
    </>
  );
};

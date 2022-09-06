import React, { FC } from "react";

export interface MessageBubbleProps {
  text: string;
  isSender?: boolean;
}

export const MessageBubble: FC<MessageBubbleProps> = ({
  text,
  isSender,
  ...props
}) => {
  return (
    <div
      {...props}
      className={`normal-case m-2 p-2 rounded-2xl max-w-fit w-5/6 sm:w-4/6 md:w-3/6 prose ${
        isSender
          ? " bg-blue-500 text-white ml-auto rounded-br-none"
          : "bg-gray-300  text-black mr-auto rounded-bl-none"
      } `}
      dangerouslySetInnerHTML={{ __html: `${text.replaceAll("\n","<br/>")}` }}
    />
  );
};

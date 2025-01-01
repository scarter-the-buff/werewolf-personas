import React, { useState } from "react";

const TextBox = () => {
  const [text, setText] = useState("");

  const handleChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gray-100 min-h-screen">
      <link href="./output.css" rel="stylesheet"></link>
      <label
        htmlFor="textbox"
        className="mb-2 text-lg font-large text-gray-700"
      >
        Enter your text:
      </label>
      <input
        id="textbox"
        type="text"
        value={text}
        onChange={handleChange}
        className="w-64 p-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        placeholder="Type something here..."
      />
      <p className="mt-4 text-gray-600">
        You entered: <span className="font-italics">{text}</span>
      </p>
    </div>
  );
};

export default TextBox;

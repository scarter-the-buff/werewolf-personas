import React, { useState } from "react";

const TextBox = () => {
  const [text, setText] = useState("");

  const handleChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="flex flex-col w-[40%] items-center justify-center p-3 bg-gray-100 min-h-[80%]">
      {/* Non-editable display box */}
      <label>Speech Record:</label>
      <div
        id="textDisplay"
        className="w-full h-[60vh] p-2 border border-gray-300 shadow-sm bg-white overflow-auto text-left"
      >
        {text || "No content available..."}
      </div>

      {/* Editable textbox */}
      <label
        htmlFor="textbox"
        className="mt-4 mb-2 w-full text-lg font-large text-gray-700"
      >
        Enter Text:
      </label>
      <textarea
        id="textbox"
        value={text}
        onChange={handleChange}
        className="w-full h-[80px] p-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-left"
        placeholder="Type something here..."
      />
    </div>
  );
};

export default TextBox;

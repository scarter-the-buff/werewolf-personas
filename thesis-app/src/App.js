import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { BrowserRouter } from "react-router-dom";
import Home from "./Home";
import Menu from "./Menu";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Menu />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<Menu />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;

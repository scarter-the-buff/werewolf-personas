import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { BrowserRouter } from "react-router-dom";
import { Link } from "react-router-dom";

import Game from "./Game";
import Menu from "./Menu";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <div>
          <Link to="/">Menu </Link>
          <Link to="/game">Game </Link>
        </div>
        <Routes>
          <Route path="/" element={<Menu />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;

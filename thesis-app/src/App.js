import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { BrowserRouter } from "react-router-dom";
import { Link } from "react-router-dom";

import Home from "./Home";
import Menu from "./Menu";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <div>
          <Link to="/">Home </Link>
          <Link to="/menu">Menu </Link>
        </div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/menu" element={<Menu />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;

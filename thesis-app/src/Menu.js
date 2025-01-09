import "./styles.css";
import { Link } from "react-router-dom";
import Button from "react-button";

function Menu() {
  return (
    <>
      <div>
        <Button>Export</Button>
        <Button activeStyle={{ position: "relative", top: 1 }}>Save as</Button>
      </div>
    </>
  );
}

export default Menu;

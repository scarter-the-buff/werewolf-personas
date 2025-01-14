import "./styles.css";
import { Link } from "react-router-dom";

function Menu() {
  return (
    <>
      <div>Hello, it's a menu!</div>
      <div>
        <Link to="/" className="text-white mx-2">
          Home
        </Link>
      </div>
    </>
  );
}

export default Menu;

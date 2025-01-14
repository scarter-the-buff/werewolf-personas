import "./styles.css";
import { Link } from "react-router-dom";

function Menu() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        backgroundColor: "#333", // Adjust as needed
        color: "white",
      }}
    >
      <h1
        style={{ marginBottom: "2rem", fontSize: "8rem", textAlign: "center" }}
      >
        Werewolf
      </h1>
      <button
        style={{
          padding: "1rem 2rem",
          fontSize: "1.2rem",
          marginBottom: "1rem",
          cursor: "pointer",
          backgroundColor: "#555",
          color: "white",
          border: "none",
          borderRadius: "5px",
          width: "200px",
        }}
      >
        NEW GAME
      </button>
      <button
        style={{
          padding: "1rem 2rem",
          fontSize: "1.2rem",
          cursor: "pointer",
          backgroundColor: "#555",
          color: "white",
          border: "none",
          borderRadius: "5px",
          width: "200px",
        }}
      >
        LOAD GAME
      </button>
    </div>
  );
}

export default Menu;

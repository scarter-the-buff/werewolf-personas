import "./styles.css";
import { Link } from "react-router-dom";

function Menu() {
  const handleButtonClick = async (title) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/start_game_req/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title }),
      });
      const data = await response.json();
      console.log(data.message);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        backgroundColor: "#333",
        color: "white",
      }}
    >
      <h1
        style={{ marginBottom: "2rem", fontSize: "3rem", textAlign: "center" }}
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
        onClick={() => handleButtonClick("New Game")}
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
        onClick={() => handleButtonClick("Load Game")}
      >
        LOAD GAME
      </button>
    </div>
  );
}

export default Menu;

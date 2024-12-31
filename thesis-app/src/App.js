import table from "./table_illustration_nobg.png";
import Textbox from "./Textbox.js";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Textbox />
        <img src={table} className="table" alt="logo" />
        <p>Hello, React!</p>
      </header>
    </div>
  );
}

export default App;

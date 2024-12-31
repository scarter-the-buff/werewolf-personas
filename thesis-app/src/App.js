import table from "./table_illustration_nobg.png";
import Textbox from "./Textbox.js";
import "./App.css";
import { Helmet } from "react-helmet";

function App() {
  return (
    <>
      <Helmet>
        <link href="./output.css" rel="stylesheet"></link>
      </Helmet>
      <div className="App">
        <header className="App-header">
          <div className="flex items-center justify-between w-full">
            <Textbox />
            <img src={table} className="table w-1/3" alt="logo" />
          </div>
        </header>
      </div>
    </>
  );
}

export default App;

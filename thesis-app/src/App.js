import table from "./table_illustration_nobg.png";
import Textbox from "./Textbox.js";
import "./styles.css";
import { Helmet } from "react-helmet";

function App() {
  return (
    <>
      <Helmet>
        <link href="./styles.css" rel="stylesheet"></link>
      </Helmet>
      <div className="App">
        <header className="App-header">
          <div className={`bg-blue-500 text-white p-4`}>Hello, World!</div>
          <h1 className="bg-red-400">Hello Tailwind!</h1>
          <h2 className="bg-red-100 to-blue-500">And again!</h2>
          <div className="btn">This should be a button.</div>
          <div className="text-blue-500">This should be blue text?</div>
          <div className="flex items-center justify-between w-full">
            <Textbox />
            <img src={table} className="table w-1/3" alt="logo" />
          </div>
        </header>
      </div>
      S
    </>
  );
}

export default App;

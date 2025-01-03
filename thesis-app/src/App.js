import table from "./table_illustration_nobg.png";
import Textbox from "./Textbox.js";
import MenuButton from "./MenuButton.js";
import "./styles.css";
import { Helmet } from "react-helmet";
import AgentsButton from "./AgentsButton.js";

function App() {
  return (
    <>
      <Helmet>
        <link href="./styles.css" rel="stylesheet"></link>
      </Helmet>
      <div className="App">
        <div className={`bg-blue-500 text-white p-4 text-center`}>
          <h1 className="text-3xl font-bold">Werewolf With AIs</h1>
        </div>

        <div className="flex w-full">
          <Textbox />

          <img
            src={table}
            className="scale-100 table p-5 object-contain"
            alt="logo"
          />

          <div
            id="tlButtonHolder"
            className="flex flex-col pt-5 h-screen min-h-[80%] ml-auto"
            style={{ alignSelf: "flex-end" }}
          >
            <AgentsButton />
            <MenuButton />
          </div>
        </div>
        <div></div>
      </div>
    </>
  );
}

export default App;

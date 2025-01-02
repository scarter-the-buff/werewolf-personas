import table from "./table_illustration_nobg.png";
import Textbox from "./Textbox.js";
import MenuButton from "./MenuButton.js";
import "./styles.css";
import { Helmet } from "react-helmet";

function App() {
  return (
    <>
      <Helmet>
        <link href="./styles.css" rel="stylesheet"></link>
      </Helmet>
      <div className="App">
        <div className={`bg-blue-500 text-white p-4`}>Werewolf with AIs</div>

        <div className="flex items-center  w-full">
          <Textbox />
          <img src={table} className="table w-1/3 p-5 ml-[100px]" alt="logo" />
          <div id="tlButtonHolder" class="flex flex-col min-h-[80%]">
            <MenuButton />
            <MenuButton />
          </div>
        </div>
        <div></div>
      </div>
    </>
  );
}

export default App;

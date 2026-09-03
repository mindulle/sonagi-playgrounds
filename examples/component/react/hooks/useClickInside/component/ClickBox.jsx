import ClickBox from "../component/ClickBox.jsx";
import "../src/style.css";

export default function App() {
  return (
    <div className="App">
      <h1>React useClickInside hook</h1>
      <ClickBox onClickInside={() => alert("click inside")} />
    </div>
  );
}

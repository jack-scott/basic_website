import logo from './logo.svg';
import './App.css';
import {useState} from "react"
import {getSolutions} from "./solutions-service"

let i = 0

function App() {

  const [solutions, setSolutions] = useState(0);

  console.log(solutions)

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Gedit <code>src/App.js</code> and save to porn.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        <button onClick={()=>{
          getSolutions().then((result)=>{setSolutions(result)})
        }}>
          Click me
        </button>
        {/* {comsole.log(solutions)?.json?.()} */}
        <textarea></textarea>
      </header>
    </div>
  );
}

export default App;

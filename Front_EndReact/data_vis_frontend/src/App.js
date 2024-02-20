import logo from './logo.svg';
import './App.css';
import './App.css';



import axios from 'axios';


function App() {

  const [artistName, setArtistName] = useState('');
  const [artistInfo, setArtistInfo] = useState(null);


  // Starting Idea

  const searchArtist = (e) => {
    e.preventDefault(); // Prevent the form from refreshing the page

    // replace URL with actual Flask Endpoint
    axios.post('http://localhost:5000/search_artist', { artistName })
      .then(response => {
        console.log(response.data);
        setArtistInfo(response.data);
      })
      .catch(error => console.error('There was an error!', error));
  };



  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

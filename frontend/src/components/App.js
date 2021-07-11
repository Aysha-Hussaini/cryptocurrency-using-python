import React, {useState, useEffect} from 'react';
import logo from '../assets/logo.png';
import {API_BASE_URL} from '../config';
import Blockchain from './Blockchain'

function App() {
  const [walletInfo, setwalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
     .then(response => response.json())
     .then(json => setwalletInfo(json))
  }, []); 

  const {address, balance} = walletInfo;
  
  return (
    <div className="App" >
     <img className="logo" src={logo} alt="application-logo"  /> 
     <h3>Welcome to Pychain</h3> 
     <br/>
     <div className="WalletInfo">
       <div> Address: {address} </div>
       <div> Balance: {balance}</div>
     </div>
     <br />
     <Blockchain/>
    </div>
  );
}

export default App;

import { useEffect, useState } from "react";
import {Link} from 'react-router-dom';
import {Button} from 'react-bootstrap';
import Transaction from "./Transaction";
import {API_BASE_URL, SECONDS_JS} from "../config";
import history from '../history';

const POLL_INTERVAL = 10 * SECONDS_JS;

function TransactionPool(){
   const [transactions, setTransations] = useState([]);
   const fetchTransactions =() => {
      fetch(`${API_BASE_URL}/transactions`)
         .then(response => response.json())
         .then(json => {
            console.log('transaction_json', json);
            setTransations(json)});

   }

   useEffect( () => {
      fetchTransactions();

      const IntervalId = setInterval(fetchTransactions, POLL_INTERVAL);

      return () => clearInterval(IntervalId);
   },[]);

   const fetchMineBlock = () => {
      fetch(`${API_BASE_URL}/blockchain/mine`)
         .then(() => {
            alert('Success!');
            history.push('/blockchain');
         })
   }

   return(
      <div className="TransactionPool">
         <Link to="/"> Home </Link>
         <hr />
         <h3>Transaction Pool</h3>
         <hr />
         <div>
            {
               transactions.map(transaction => (
                  <div key={transaction.id} >
                     <Transaction  transaction={transaction}/>
                     <hr />
                  </div>
               )
               )
            }
         </div>
         <hr />
         <Button
         variant="danger" size="sm" onClick={fetchMineBlock}>
            Mine a block of these transactions
         </Button>
      </div>
   )

}

export default TransactionPool;
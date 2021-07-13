import React, {useState} from 'react';
import {Button} from 'react-bootstrap'
import {MILLISECONDS_PY} from '../config.js';
import Transaction from './Transaction';

function ToggleTransactionDisplay({block}){
    const [displayTransaction, setDisplayTransaction] = useState(false);
    const {data} = block;
    const toggleDisplaytransaction = () => {
        setDisplayTransaction(!displayTransaction);
    }

    if (displayTransaction){
        return(
            <div>
                {
                    data.map(transaction => (
                        <div key= {transaction.id}>
                            <hr/>
                            <Transaction transaction = {transaction}/>
                            </div>

                    ))
                }
                <br/>
                <Button
                variant='danger' 
                size='sm'
                onClick = {toggleDisplaytransaction}>
                    Show Less
                </Button>
            </div> 
            
        )}

    return(
        <div>
            <br/>
            <Button
            variant='danger' 
            size='sm'
            onClick = {toggleDisplaytransaction}
            >
                Show More
            </Button>
        </div>
    )

}

function Block({block}) {
    const {timestamp, hash, data} = block;
    const hashDisplay = hash.substring(0, 15) + '...';
    const timestampDisplay = new Date(timestamp/MILLISECONDS_PY).toLocaleString(); 

    return (
        <div className='Block'>
            <div> Hash: {hashDisplay}</div>
            <div> Timestamp: {timestampDisplay}</div>
            <ToggleTransactionDisplay block={block} />
        </div>
    )

}

export default Block;
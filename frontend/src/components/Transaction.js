import React from 'react';

function Transaction({transaction}) {
    const {input, output} = transaction;
    const recipients = Object.keys(output);
    

    const receiver = recipients.find(receipient => receipient!==input.address);
    const sender = recipients.find(sender_address => sender_address===input.address);
    
    function TransactionDisplay(){
        if (input.address === '*--official_mining_reward--*')
        {
            return(
                <div>
                    <div>From: {input.address}</div>
                    <div>To: {receiver} | Sent: {output[receiver]}</div>
                </div>
            )
        }
        return(
            <div>
                <div>From: {input.address}</div>
                <div>To: {receiver} | Sent: {output[receiver]}</div>
                <div>Sender_balance: {output[sender]}</div>
            </div>
        )
        
    }

    return (
        <div className='Transaction'>
            <TransactionDisplay />
        </div>
    )
}

export default Transaction;
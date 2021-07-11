import React from 'react';

function Transaction({transaction}) {
    const {input, output} = transaction;
    const recipients = Object.keys(output);

    const receiver = recipients.find(receipient => receipient!==input.address);
    const sender = recipients.find(sender_address => sender_address===input.address);
    console.log(receiver, sender);

    return (
        <div className='Transaction'>
            <div>From: {input.address}</div>
            <div>To: {receiver} | Sent: {output[receiver]}</div>
            <div>Sender_balance: {output[sender]}</div>
        </div>
    )
}

export default Transaction;
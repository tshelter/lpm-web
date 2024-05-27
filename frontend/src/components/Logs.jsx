import React from 'react';

function Logs({logs}) {
    return (
        <>
            <p>Logs:</p>
            <ul style={{minHeight: "400px", height: "400px", overflowY: "scroll", border: "1px solid white"}}>
                {logs.map((log, index) => {
                    return <li key={index}>{log}</li>;
                })}
            </ul>
        </>
    );
}

export default Logs;

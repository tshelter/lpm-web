import {v4 as uuid_v4} from "uuid";
import React, {useState} from 'react';
import {Button} from "react-bootstrap";


function Service({ctx, agent_id, name, is_active, is_enabled, memory}) {
    const callbacks = useState({});
    const handleRestart = () => {
        console.log("Restarting service", name);
        const uuid = uuid_v4();
        setIsRestarting(true);
        ctx.ws.send(JSON.stringify({
            agent_id,
            uuid,
            action: {
                action: "restart",
                service: name,
            }
        }));
        callbacks[uuid] = () => {
            setIsRestarting(false);
            callbacks[uuid] = null;
        }
    }
    document.addEventListener("lpm:action", (event) => {
        if (event.uuid in callbacks) {
            callbacks[event.uuid]();
        }
    });

    const [isRestarting, setIsRestarting] = useState(false);

    return (
        <li>
            <h2>{name}</h2>
            <p>Memory: {memory}</p>
            <p>Active: {is_active ? "Yes" : "No"}</p>
            <p>Enabled: {is_enabled ? "Yes" : "No"}</p>

            <Button onClick={handleRestart} disabled={isRestarting}>Restart</Button>
        </li>
    );
}

export default Service;

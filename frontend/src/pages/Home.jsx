import {v4 as uuid_v4} from "uuid";
import config from "../config";
import {useState} from "react";
import Agent from "../components/Agent";


function HomePage() {
    const client_id = uuid_v4().toString();
    const [agents, setAgents] = useState({});

    const ws = new WebSocket(`${config.WEBSOCKET_URL}/${client_id}`);
    const ctx = {ws, client_id};

    const dispatchEvent = (type, payload) => {
        document.dispatchEvent(new CustomEvent(
            type, payload
        ));
    }

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);

        if (msg.status) {
            const status = msg.status;
            setAgents({...agents, [msg.agent_id]: {services: status.services, agent_id: msg.agent_id}});
            dispatchEvent("lpm:status", msg);
        }
        if (msg.action) {
            dispatchEvent("lpm:action", msg);
        }
        if (msg.log) {
            dispatchEvent("lpm:log", msg);
        }
    };

    return (
        <div>
            {Object.values(agents).map((agent) => {
                return (
                    <Agent key={agent.agent_id} ctx={ctx} {...agent}/>
                );
            })}
        </div>
    );
}

export default HomePage;

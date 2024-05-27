import {v4 as uuid_v4} from "uuid";
import config from "../config";
import {useEffect, useRef, useState} from "react";
import Agent from "../components/Agent";
import {publish} from "../events";
import Container from "react-bootstrap/Container";


function HomePage() {
    const [agents, setAgents] = useState({});
    const ctx = useRef({});

    useEffect(() => {
        const client_id = uuid_v4().toString();
        const ws = new WebSocket(`${config.WEBSOCKET_URL}/${client_id}`);
        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);

            if (msg.status) {
                const status = msg.status;
                setAgents((prevAgents) => {
                    return {
                        ...prevAgents,
                        [msg.agent_id]: <Agent key={msg.agent_id} agent_id={msg.agent_id} ctx={ctx} {...status}/>
                    }
                });
            }
            if (msg.action) {
                publish("lpm:action", msg);
            }
            if (msg.log) {
                publish("lpm:log", msg);
            }
        };
        ctx.current.ws = ws;

        return () => {
            ws.close();
            ws.onmessage = null;
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // noinspection JSValidateTypes
    return (
        <Container>
            {Object.values(agents)}
        </Container>
    );
}

export default HomePage;

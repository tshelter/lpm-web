import {v4 as uuid_v4} from "uuid";
import React, {useEffect, useRef, useState} from 'react';
import {Button, Collapse} from "react-bootstrap";
import {subscribe, unsubscribe} from "../events";


function Service({ctx, agent_id, name, is_active, is_enabled, memory}) {
    const [isHandling, setIsHandling] = useState(false);
    const [isShowLogs, setIsShowLogs] = useState(false);
    const [logs, setLogs] = useState([]);
    const waitingForUuid = useRef(null);

    const handleAction = (action) => {
        setIsHandling(true);
        const uuid = uuid_v4();
        waitingForUuid.current = uuid;
        ctx.current.ws.send(JSON.stringify({
            agent_id,
            uuid,
            action: {
                action: action,
                service: name,
            }
        }));
    }

    const createHandler = (action) => {
        return () => {
            handleAction(action);
        }
    }

    useEffect(() => {
        const handleLogEvent = (event) => {
            const data = event.detail;
            if (data.agent_id !== agent_id || data.log.service !== name) {
                return;
            }
            setLogs(prevLogs => [...prevLogs, data.log.message]);
        }

        subscribe("lpm:log", handleLogEvent);
        return () => {
            unsubscribe("lpm:log", handleLogEvent)
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        const handleActionEvent = (event) => {
            const {uuid, action} = event.detail;
            console.log(uuid, action, waitingForUuid.current);
            if (uuid !== waitingForUuid.current) {
                return;
            }
            setIsHandling(false);
            if (typeof action.response === "string" && action.response !== "ok") {
                setLogs(prevLogs => [...prevLogs, `LPM Action Error: ${action.response}`]);
            }
        }

        subscribe("lpm:action", handleActionEvent);
        return () => {
            unsubscribe("lpm:action", handleActionEvent)
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <li>
            <h2>{name}</h2>
            <p>Memory: {memory}</p>
            <p>Active: {is_active ? "Yes" : "No"}</p>
            <p>Enabled: {is_enabled ? "Yes" : "No"}</p>

            <Button onClick={createHandler("start")} disabled={isHandling}>Start</Button>
            <Button onClick={createHandler("stop")} disabled={isHandling}>Stop</Button>
            <Button onClick={createHandler("restart")} disabled={isHandling}>Restart</Button>
            <Button onClick={createHandler("reload")} disabled={isHandling}>Reload</Button>
            <Button onClick={createHandler("remove")} disabled={isHandling}>Remove</Button>

            <Button onClick={() => setIsShowLogs(!isShowLogs)}>{isShowLogs ? "Hide" : "Show"} Logs</Button>
            <Collapse in={isShowLogs}>
                <div>
                    <p>Logs:</p>
                    <ul>
                        {logs.map((log, index) => {
                            return (
                                <li key={index}>{log}</li>
                            );
                        })}
                    </ul>
                </div>
            </Collapse>
        </li>
    );
}

export default Service;

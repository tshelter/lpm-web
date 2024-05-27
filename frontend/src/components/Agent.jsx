import React from 'react';
import Service from "./Service";

function Agent({ctx, agent_id, services}) {
    return (
        <div key={agent_id}>
            <h1>Agent: {agent_id}</h1>
            <ul>
                {services.map((service) => {
                    return (
                        <Service key={service.name} ctx={ctx} agent_id={agent_id} {...service} />
                    );
                })}
            </ul>
        </div>
    );
}

export default Agent;

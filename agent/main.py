import sys

import asyncio
import logging
import os
import shlex
import subprocess
import websockets

from schemas import (
    LogResponse,
    AgentRequest,
    AgentResponse,
    ActionResponse,
    StatusResponse,
    Service,
)

URL = os.getenv(
    "URL",
    sys.argv[1] if len(sys.argv) > 1 else "ws://localhost:8000/agent_ws/test_agent",
)
STATUS_INTERVAL = int(os.getenv("STATUS_INTERVAL", 3))
AGENT_ID = URL.split("/")[-1]
service_watcher_processes = {}
service_watchers = {}


def parse_services(output: list[str]) -> list[Service]:
    return [
        Service(
            name=name,
            is_active=is_active == "true",
            is_enabled=is_enabled == "true",
            memory=memory,
        )
        for name, is_active, is_enabled, memory in [
            line.split() if len(line.split()) == 4 else line.split() + [""]
            for line in output
            if line and len(line.split()) in (3, 4)
        ]
    ]


async def read_stream(service, stream, socket):
    while True:
        log = (await stream.readline()).decode().strip()
        if log:
            await socket.send(
                AgentResponse(
                    log=LogResponse(message=log, service=service),
                    agent_id=AGENT_ID,
                ).json(exclude_none=True)
            )


async def send_output(service, process, socket):
    await asyncio.gather(
        read_stream(service, process.stdout, socket),
        read_stream(service, process.stderr, socket),
    )


async def async_check_output(command):
    process = await asyncio.create_subprocess_exec(
        *command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode, command, output=stdout, stderr=stderr
        )

    return "\n".join([stdout.decode(), stderr.decode()]).strip()


async def send_status(socket: websockets.WebSocketClientProtocol):
    while True:
        output = (await async_check_output(shlex.split("lpm list --raw"))).split("\n")
        services = parse_services(output)
        current_services = {service.name for service in services}
        watched_services = set(service_watcher_processes.keys())

        new_services = current_services - watched_services
        for service in new_services:
            process = await asyncio.create_subprocess_exec(
                *shlex.split(f"lpm logs --follow {service}"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            service_watcher_processes[service] = process
            service_watchers[service] = asyncio.create_task(
                send_output(service, process, socket)
            )

        removed_services = watched_services - current_services
        for service in removed_services:
            process = service_watcher_processes.pop(service)
            process.kill()
            watcher = service_watchers.pop(service)
            watcher.cancel()

        await socket.send(
            AgentResponse(
                status=StatusResponse(
                    services=services,
                ),
                agent_id=AGENT_ID,
            ).json(exclude_none=True)
        )
        await asyncio.sleep(STATUS_INTERVAL)


async def run_lpm_command(action, service):
    command = shlex.split(f"lpm {action} {service}")

    process = await asyncio.create_subprocess_exec(
        *command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        return "\n".join([stdout.decode(), stderr.decode()]).strip()

    return "ok"


async def handle_request(socket: websockets.WebSocketClientProtocol):
    while True:
        try:
            request = AgentRequest.parse_raw(await socket.recv())
        except Exception as e:
            logging.exception(e)
            continue

        if request.action:
            response = AgentResponse(
                action=ActionResponse(
                    response=await run_lpm_command(
                        request.action.action, request.action.service
                    )
                ),
                uuid=request.uuid,
                agent_id=AGENT_ID,
            )
            await socket.send(response.json(exclude_none=True))

        if request.status:
            output = (
                subprocess.check_output(
                    shlex.split(f"lpm list --raw {request.status.service or ''}")
                )
                .decode()
                .strip()
                .split("\n")
            )
            services = parse_services(output)
            await socket.send(
                AgentResponse(
                    status=StatusResponse(services=services),
                    uuid=request.uuid,
                    agent_id=AGENT_ID,
                ).json(exclude_none=True)
            )


async def depend_on_loop(func, *args, **kwargs):
    try:
        await func(*args, **kwargs)
    except Exception as e:
        logging.exception(e)
        exit(1)


async def main():
    async with websockets.connect(URL) as socket:
        asyncio.create_task(depend_on_loop(handle_request, socket))
        asyncio.create_task(depend_on_loop(send_status, socket))
        await asyncio.Event().wait()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

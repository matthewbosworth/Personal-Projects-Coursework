# Concurrent Socket Server

## Overview

This project has two programs:

- **`ConcurrentServer.java`** — listens for client connections and answers requests for six pieces of system information (date/time, uptime, memory use, netstat, current users, running processes).
- **`MultiThreadedClient.java`** — connects to the server, can spawn many simultaneous client sessions, and measures how long each one takes to get a response.

Both connect over the same network address and port (`4998` in this setup).

## How the server works

1. The server opens a `ServerSocket` on port 4998 and calls `accept()`, which blocks until a client connects.
2. As soon as a client connects, the server does **not** handle the request itself. Instead, it wraps the connection in a `ClientHandler` and starts a new `Thread` to run it.
3. The main thread immediately loops back to `accept()` to wait for the next client — it does not wait for the thread it just spawned to finish.
4. Inside each `ClientHandler` thread, the server:
   - Reads the one-line request from the client (a number 1–6)
   - Maps that number to a Linux command (e.g. `3` → `free -h`)
   - Runs the command via `ProcessBuilder`, capturing its output
   - Sends the output back to the client, followed by a `##END##` delimiter so the client knows the response is complete
   - Closes the socket and the thread ends

Because every client gets its own thread, many clients can be mid-request at the same time — the server processes them in parallel instead of one at a time.

## How the client works

1. Prompts for the server's IP address and port once.
2. Then repeatedly prompts for:
   - An operation (1–6, or 7 to exit)
   - A number of client sessions to spawn (1, 5, 10, 15, 20, 25, or 100)
3. Spawns that many threads at once, each opening its own socket connection to the server, sending the chosen operation, and timing how long it takes to get a full response back.
4. Uses a `CountDownLatch` so the main thread waits until every spawned client thread has finished.
5. Reports:
   - Turnaround time for each individual client
   - Total turnaround time (sum of all clients)
   - Average turnaround time (total ÷ number of clients)

The client code itself is identical whether it's talking to the iterative server or the concurrent server — it doesn't need to know which kind of server is on the other end.

## How this differs from the Iterative Server

The client is unchanged between the two assignments. The entire difference is in how the server handles incoming connections:

| | Iterative Server | Concurrent Server |
|---|---|---|
| **Handling model** | Single thread does everything | Main thread accepts, worker threads handle |
| **After `accept()`** | Processes the request fully, *then* loops back to accept the next client | Spawns a thread and immediately loops back to accept the next client |
| **Multiple clients** | Served one at a time, in order | Served simultaneously |
| **Effect of more clients** | Each additional client waits for every client ahead of it — turnaround time grows roughly linearly with client count | Clients run in parallel — turnaround time stays roughly flat as client count grows |

In short: the iterative server is a single line at one checkout counter, while the concurrent server opens a new checkout counter for every customer who walks in. The line moves faster overall, but there is a small cost — each new "counter" (thread) takes some CPU and memory to set up, which is why the concurrent server's average turnaround time still creeps up slightly at high client counts rather than staying perfectly flat.

## Files

- `ConcurrentServer.java` / `run_server.sh` — run on the server machine (02a)
- `MultiThreadedClient.java` / `run_client.sh` — run on the client machine (01a)

## Running it

On the server (02a):
```
./run_server.sh
```

On the client (01a):
```
./run_client.sh
```
Then enter the server's IP address and port (`4998`) when prompted.

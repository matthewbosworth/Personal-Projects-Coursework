import java.io.*;
import java.net.*;

public class ConcurrentServer {

    // Runs a shell command and returns its output as a String
    private static String runCommand(String command) {
        StringBuilder output = new StringBuilder();
        try {
            ProcessBuilder pb = new ProcessBuilder("bash", "-c", command);
            pb.redirectErrorStream(true);
            Process process = pb.start();
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            process.waitFor();
        } catch (Exception e) {
            output.append("Error executing command: ").append(e.getMessage());
        }
        return output.toString().trim();
    }

    // Maps client request number to the appropriate Linux command
    private static String handleRequest(String request) {
        return switch (request.trim()) {
            case "1" -> runCommand("date");                          // Date and Time
            case "2" -> runCommand("uptime");                        // Uptime
            case "3" -> runCommand("free -h");                       // Memory Use
            case "4" -> runCommand("netstat -tuln");                 // Netstat
            case "5" -> runCommand("who");                           // Current Users
            case "6" -> runCommand("ps aux");                        // Running Processes
            default  -> "Invalid request.";
        };
    }

    // Each client connection is handled by its own thread, so the server
    // never blocks waiting on one client before it can accept the next.
    static class ClientHandler implements Runnable {
        private final Socket clientSocket;

        public ClientHandler(Socket clientSocket) {
            this.clientSocket = clientSocket;
        }

        @Override
        public void run() {
            String threadName = Thread.currentThread().getName();
            System.out.println("[" + threadName + "] Client connected: "
                    + clientSocket.getInetAddress());

            try {
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream()));
                PrintWriter out = new PrintWriter(
                    clientSocket.getOutputStream(), true);

                String request = in.readLine();
                System.out.println("[" + threadName + "] Request received: " + request);

                String response = handleRequest(request);

                // Send response — use a delimiter so client knows when it ends
                out.println(response);
                out.println("##END##");

            } catch (IOException e) {
                System.out.println("[" + threadName + "] Error with client: " + e.getMessage());
            } finally {
                try {
                    clientSocket.close();
                } catch (IOException e) {
                    System.out.println("[" + threadName + "] Error closing socket: " + e.getMessage());
                }
                System.out.println("[" + threadName + "] Client disconnected.\n");
            }
        }
    }

    public static void main(String[] args) throws IOException {
        int port = 4998; // Use a port in the allowed range: 1025-4998

        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("Concurrent server listening on port " + port);

        while (true) {
            // Blocks until a client connects, but each connection is immediately
            // handed off to its own thread so multiple clients are served in parallel
            Socket clientSocket = serverSocket.accept();

            // Spawn a new "server instance" (thread) to handle this request
            Thread workerThread = new Thread(new ClientHandler(clientSocket));
            workerThread.start();

            // Loop back to accept() right away — does NOT wait for the
            // previous client to finish, unlike the iterative server
        }
    }
}

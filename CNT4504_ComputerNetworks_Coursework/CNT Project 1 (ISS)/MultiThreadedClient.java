import java.io.*;
import java.net.*;
import java.util.Scanner;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

public class MultiThreadedClient {

    static String serverHost;
    static int serverPort;
    static String operation;

    // Each thread represents one client session
    static class ClientTask implements Runnable {
        private final int clientId;
        private final AtomicLong totalTime;
        private final CountDownLatch latch;

        public ClientTask(int clientId, AtomicLong totalTime, CountDownLatch latch) {
            this.clientId = clientId;
            this.totalTime = totalTime;
            this.latch = latch;
        }

        @Override
        public void run() {
            long startTime = System.currentTimeMillis();

            try (Socket socket = new Socket(serverHost, serverPort)) {
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));

                // Send the requested operation
                out.println(operation);

                // Read response until ##END## delimiter
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = in.readLine()) != null) {
                    if (line.equals("##END##")) break;
                    response.append(line).append("\n");
                }

                long elapsed = System.currentTimeMillis() - startTime;
                totalTime.addAndGet(elapsed);

                System.out.printf("Client %2d | Turnaround: %d ms%n", clientId, elapsed);
                // Uncomment below to print server response per client:
                 System.out.println("Response:\n" + response);

            } catch (IOException e) {
                System.out.println("Client " + clientId + " error: " + e.getMessage());
            } finally {
                latch.countDown();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException, IOException {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter server IP address: ");
        serverHost = scanner.nextLine().trim();

        System.out.print("Enter server port: ");
        serverPort = Integer.parseInt(scanner.nextLine().trim());

        System.out.println("\nSelect operation:");
        System.out.println("  1 - Date and Time");
        System.out.println("  2 - Uptime");
        System.out.println("  3 - Memory Use");
        System.out.println("  4 - Netstat");
        System.out.println("  5 - Current Users");
        System.out.println("  6 - Running Processes");
        System.out.print("Choice: ");
        operation = scanner.nextLine().trim();

        System.out.print("Number of clients (1, 5, 10, 15, 20, 25): ");
        int numClients = Integer.parseInt(scanner.nextLine().trim());

        System.out.printf("%nLaunching %d client thread(s)...%n%n", numClients);

        AtomicLong totalTime = new AtomicLong(0);
        CountDownLatch latch = new CountDownLatch(numClients);

        // Spawn all client threads simultaneously
        for (int i = 1; i <= numClients; i++) {
            new Thread(new ClientTask(i, totalTime, latch)).start();
        }

        // Wait for all clients to finish
        latch.await();

        long total = totalTime.get();
        double average = (double) total / numClients;

        System.out.println("\n========== Results ==========");
        System.out.printf("Clients spawned       : %d%n", numClients);
        System.out.printf("Total Turnaround Time : %d ms%n", total);
        System.out.printf("Avg Turnaround Time   : %.2f ms%n", average);
        System.out.println("==============================");
    }
}
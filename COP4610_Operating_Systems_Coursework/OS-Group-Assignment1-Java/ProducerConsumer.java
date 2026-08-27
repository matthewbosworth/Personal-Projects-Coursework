// Producer-Consumer Problem
// Uses wait() and notify() for thread synchronization

public class ProducerConsumer {
    
    public static final int EMPTY = 0;
    public static final int FULL = 1;
    
    private static final int BUFFER_SIZE = 5;
    private int[] buffer = new int[BUFFER_SIZE];
    
    private int count = 0;
    
    // Initialize buffer to EMPTY
    public ProducerConsumer() {
        for (int i = 0; i < BUFFER_SIZE; i++) {
            buffer[i] = EMPTY;
        }
    }
    
    public synchronized void produce() throws InterruptedException {
        // Wait while buffer is full
        while (count == BUFFER_SIZE) {
            System.out.println("Producer: Buffer is FULL. Waiting...");
            wait();
        }
        
        // Find EMPTY slot and produce
        for (int i = 0; i < BUFFER_SIZE; i++) {
            if (buffer[i] == EMPTY) {
                buffer[i] = FULL;
                count++;
                System.out.println("Producer: Produced at index " + i + ". Count = " + count);
                printBuffer();
                notify();
                break;
            }
        }
    }
    
    public synchronized void consume() throws InterruptedException {
        // Wait while buffer is empty
        while (count == 0) {
            System.out.println("Consumer: Buffer is EMPTY. Waiting...");
            wait();
        }
        
        // Find FULL slot and consume
        for (int i = 0; i < BUFFER_SIZE; i++) {
            if (buffer[i] == FULL) {
                buffer[i] = EMPTY;
                count--;
                System.out.println("Consumer: Consumed at index " + i + ". Count = " + count);
                printBuffer();
                notify();
                break;
            }
        }
    }
    
    private void printBuffer() {
        System.out.print("Buffer: [");
        for (int i = 0; i < BUFFER_SIZE; i++) {
            System.out.print(buffer[i] == FULL ? "FULL" : "EMPTY");
            if (i < BUFFER_SIZE - 1) System.out.print(", ");
        }
        System.out.println("]");
        System.out.println("----------------------------------------");
    }
    
    static class Producer extends Thread {
        private ProducerConsumer pc;
        private int itemsToProduce;
        
        public Producer(ProducerConsumer pc, int items) {
            this.pc = pc;
            this.itemsToProduce = items;
        }
        
        @Override
        public void run() {
            try {
                for (int i = 0; i < itemsToProduce; i++) {
                    pc.produce();
                    Thread.sleep(500);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    static class Consumer extends Thread {
        private ProducerConsumer pc;
        private int itemsToConsume;
        
        public Consumer(ProducerConsumer pc, int items) {
            this.pc = pc;
            this.itemsToConsume = items;
        }
        
        @Override
        public void run() {
            try {
                for (int i = 0; i < itemsToConsume; i++) {
                    pc.consume();
                    Thread.sleep(800);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        
        System.out.println("========================================================");
        System.out.println("   PRODUCER-CONSUMER PROBLEM DEMONSTRATION");
        System.out.println("   Buffer Size: " + BUFFER_SIZE);
        System.out.println("========================================================\n");
        
        System.out.println("\n*** SCENARIO 1: Buffer Full - Producer Waiting ***");
        System.out.println("Producer will produce 7 items, Consumer will consume 7 items");
        System.out.println("Producer is faster, so buffer will fill up\n");
        
        ProducerConsumer pc1 = new ProducerConsumer();
        
        Producer producer1 = new Producer(pc1, 7);
        Consumer consumer1 = new Consumer(pc1, 7);
        
        producer1.start();
        consumer1.start();
        
        producer1.join();
        consumer1.join();
        
        System.out.println("\n*** Scenario 1 Complete ***\n");
        Thread.sleep(1000);
        
        System.out.println("\n*** SCENARIO 2: Buffer Empty - Consumer Waiting ***");
        System.out.println("Consumer starts first and tries to consume from empty buffer\n");
        
        ProducerConsumer pc2 = new ProducerConsumer();
        
        Consumer consumer2 = new Consumer(pc2, 3);
        consumer2.start();
        
        Thread.sleep(1500);
        
        Producer producer2 = new Producer(pc2, 3);
        producer2.start();
        
        producer2.join();
        consumer2.join();
        
        System.out.println("\n*** Scenario 2 Complete ***\n");
        Thread.sleep(1000);
        
        System.out.println("\n*** SCENARIO 3: Partially Full Buffer ***");
        System.out.println("Producer and Consumer working at similar speeds\n");
        
        ProducerConsumer pc3 = new ProducerConsumer();
        
        Thread producer3 = new Thread(() -> {
            try {
                for (int i = 0; i < 8; i++) {
                    pc3.produce();
                    Thread.sleep(600);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread consumer3 = new Thread(() -> {
            try {
                for (int i = 0; i < 8; i++) {
                    pc3.consume();
                    Thread.sleep(700);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer3.start();
        consumer3.start();
        
        producer3.join();
        consumer3.join();
        
        System.out.println("\n*** Scenario 3 Complete ***");
        System.out.println("\n========================================================");
        System.out.println("   ALL SCENARIOS COMPLETED SUCCESSFULLY!");
        System.out.println("========================================================");
    }
}

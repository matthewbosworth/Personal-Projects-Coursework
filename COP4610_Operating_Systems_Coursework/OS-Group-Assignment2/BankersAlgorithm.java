public class BankersAlgorithm {

    private final int n;
    private final int m;
    private final int[] available;
    private final int[][] max;
    private final int[][] allocation;
    private final int[][] need;

    //constructor
    public BankersAlgorithm(int[] available, int[][] max, int[][] allocation) {
        this.n = allocation.length;
        this.m = available.length;
        this.available = copyArray(available);
        this.max = copyMatrix(max);
        this.allocation = copyMatrix(allocation);
        this.need = new int[n][m];

        for(int i = 0; i < n; i++) {
            for(int j = 0; j < m; j++) {
                this.need[i][j] = max[i][j] - allocation[i][j];
            }//end inner for
        }//end outer for

    }// end constructor

    public int[] safetyAlgorithm() {
        int[] work = copyArray(available);
        boolean[] finish = new boolean[n];
        int[] safeSeq = new int[n];
        int count = 0;

        boolean found = true;
        while(found) {
            found = false;
            for(int i = 0; i < n; i++) {
                if(!finish[i] && needLEWork(need[i], work)) {
                    for(int j = 0; j < m; j++) {
                        work[j] += allocation[i][j];
                    }
                    finish[i] = true;
                    safeSeq[count++] = i;
                    found = true;
                }
            }
        }//end while
        for (boolean f : finish) {
            if (!f) {
                return null; // No safe sequence found
            }
        }

        return safeSeq;
    }//end safety algo method

    public boolean requestResources(int threadId, int[] request) {
        
        System.out.println("====================================");
        System.out.printf("Request: Threat T%d requests %s%n", threadId, vectorToString(request));
        System.out.println("=====================================");

        //step 1
        if(!vecLE(request, need[threadId])) {
            System.out.println(" X DENIED - Request exceeds the thread's maximum need.");
            printState();
            return false;
        }

        //step 2
        if(!vecLE(request, available)) {
            System.out.println(" X DENIED - Not enough resources available.");
            printState();
            return false;
        }

        //step 3
        for(int j = 0; j < m; j++) {
            available[threadId] -= 0;
            available[j] -= request[j];
            allocation[threadId][j] += request[j];
            need[threadId][j] -= request[j];
        }

        int[] seq = safetyAlgorithm();

        if(seq != null) {
            System.out.println(" √ GRANTED - Request is safe. ");
            System.out.println("Safe sequence: ");
            for(int i = 0; i < seq.length; i++) {
                System.out.print("T" + seq[i]);
                if(i < seq.length - 1) {
                    System.out.print(" -> ");
                }
            }
            System.out.println();
        } else {
            // Rollback
            for(int j = 0; j < m; j++) {
                available[j] += request[j];
                allocation[threadId][j] -= request[j];
                need[threadId][j] += request[j];
            }
            System.out.println(" X DENIED - Granting this request would lead to an unsafe state.");
            
        }
        printState();
        return seq != null;

    }//end request resource method

    //helpers
    public void printState() {
        System.out.println();
        System.out.println("   Need Matrix:");
        System.out.println("            A     B    C");
        for(int i = 0; i < n; i++) {
            System.out.printf("    T%d      %3d  %3d  %3d%n",i,
            need[i][0], need[i][1], need[i][2]);
        }
        System.out.println();
        System.out.printf("  Available: %s%n%n", vectorToString(available));
        
    }

    public void printInitialState() {
        System.out.println("=================================================");
        System.out.println("|  Initial State of the Banker's Algorithm.     |");
        System.out.println("=================================================");
        System.out.println("  Allocation Matrix:             Max Matrix:");
        System.out.println("            A     B    C           A   B    C");
        for(int i = 0; i < n; i++) {
            System.out.printf("    T%d      %3d  %3d  %3d       %3d  %3d  %3d%n",i,
            allocation[i][0], allocation[i][1], allocation[i][2],
            max[i][0], max[i][1], max[i][2]);
        }
        System.out.println();
        System.out.println("  Need Matrix:");
        System.out.println("            A     B    C");
        for(int i = 0; i < n; i++) {
            System.out.printf("    T%d      %3d  %3d  %3d%n",i,
            need[i][0], need[i][1], need[i][2]);
        }
        System.out.printf("%n  Available: %s%n", vectorToString(available));
        System.out.println();
        int[] initSeq = safetyAlgorithm();
        if(initSeq != null) {
            System.out.println("  Initial Safe Sequence: ");
            for(int i = 0; i < initSeq.length; i++) {
                System.out.print("T" + initSeq[i]);
                if(i < initSeq.length - 1) {
                    System.out.print(" -> ");
                }
            }
            System.out.println();
        } else {
            System.out.println("  WARNING: Initial state is NOT safe.");
        }
        System.out.println();
    }

    private boolean vecLE(int[] v1, int[] v2) {
        for(int j = 0; j < m; j++) {
            if(v1[j] > v2[j]) {
                return false;
            }
        }
        return true;
    }
    private boolean needLEWork(int[] needRow, int[] work) {
        for(int j = 0; j < m; j++) {
            if(needRow[j] > work[j]) {
                return false;
            }
        }
        return true;
    }
    private static int[] copyArray(int[] src) {
        int[] copy = new int[src.length];
        System.arraycopy(src, 0, copy, 0, src.length);
        return copy;
    }
    private static int[][] copyMatrix(int[][] src) {
        int[][] copy = new int[src.length][];
        for(int i = 0; i < src.length; i++) {
            copy[i] = copyArray(src[i]);
        }
        return copy;
    }
    private String vectorToString(int[] v) {
        StringBuilder sb = new StringBuilder("(");
        for(int i = 0; i < v.length; i++) {
            sb.append(v[i]);
            if(i < v.length - 1) {
                sb.append(", ");
            }
        }
        sb.append(")");
        return sb.toString();
    }

    public static void main(String[] args) {
        int[] available = {3, 3, 2};
        int[][] max = {
            {7, 5, 3},
            {3, 2, 2},
            {9, 0, 2},
            {2, 2, 2},
            {4, 3, 3}
        };
        int[][] allocation = {
            {0, 1, 0},
            {2, 0, 0},
            {3, 0, 2},
            {2, 1, 1},
            {0, 0, 2}
        };

        //case 1: granted
        BankersAlgorithm bank1 = new BankersAlgorithm(available, max, allocation);
        bank1.printInitialState();

        System.out.println("================================================");
        System.out.println("   Case 1 - Request that should be GRANTED");
        System.out.println("=================================================");
        System.out.println();

        bank1.requestResources(1, new int[]{1, 0, 2});

        //case 2: denied
        int[] available2 = {2, 3, 0};
        int[][] allocation2 = {
            {0, 1, 0},
            {3, 0, 2},
            {3, 0, 2},
            {2, 1, 1},
            {0, 0, 2}
        };
        BankersAlgorithm bank2 = new BankersAlgorithm(available2, max, allocation2);

        System.out.println("================================================");
        System.out.println("   Case 2 - Request that should be DENIED");
        System.out.println("=================================================");
        System.out.println();

        bank2.requestResources(0, new int[]{0, 2, 0});


    }





}
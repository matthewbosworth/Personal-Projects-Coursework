# Producer-Consumer Problem

## Description
This program demonstrates the classic producer-consumer problem using Java threads with `wait()` and `notify()` for synchronization.

## How to Compile and Run
```bash
javac ProducerConsumer.java
java ProducerConsumer
```

## What It Does
- **Producer**: Sets buffer elements from EMPTY to FULL
- **Consumer**: Sets buffer elements from FULL to EMPTY
- Buffer size: 5 elements
- Uses synchronized methods with wait() and notify()

## Three Scenarios Demonstrated

### Scenario 1: Buffer Full - Producer Waiting
- Producer tries to produce 7 items
- Consumer consumes 7 items
- Producer is faster, so buffer fills up and producer must wait

### Scenario 2: Buffer Empty - Consumer Waiting
- Consumer starts first on empty buffer
- Consumer waits until producer creates items

### Scenario 3: Partially Full Buffer
- Producer and consumer work at balanced speeds
- Buffer stays partially full throughout execution

## Key Features
- Prevents buffer overflow (producer can't write when full)
- Prevents buffer underflow (consumer can't read when empty)
- Producer only writes to EMPTY slots
- Consumer only reads from FULL slots
- Thread synchronization using wait() and notify()

## Screenshots
1. **Scenario 1**: Buffer FULL with "Producer: Buffer is FULL. Waiting..." message
2. **Scenario 2**: Buffer EMPTY with "Consumer: Buffer is EMPTY. Waiting..." message  
3. **Scenario 3**: Buffer partially full (count = 2 or 3)


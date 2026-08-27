# Makefile for DOS Command Interpreter

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = dos_interpreter
SOURCE = dos_interpreter.c

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#define MAX_INPUT 256
#define MAX_COMMAND 512
// Test line comment
// Function to display current working directory
void show_pwd() {
    char cwd[MAX_INPUT];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("Current directory: %s\n", cwd);
    } else {
        perror("getcwd() error");
    }
}

// Function to trim whitespace from string
void trim(char *str) {
    int i, j = 0;
    int len = strlen(str);
    
    for (i = 0; i < len && (str[i] == ' ' || str[i] == '\t' || str[i] == '\n'); i++);
    
    for (; i < len; i++) {
        if (str[i] != '\n') {
            str[j++] = str[i];
        }
    }
    str[j] = '\0';
    
    j--;
    while (j >= 0 && (str[j] == ' ' || str[j] == '\t')) {
        str[j--] = '\0';
    }
}

// Function to parse input into command and arguments
int parse_input(char *input, char *command, char *arg1, char *arg2) {
    char *token;
    int count = 0;
    
    command[0] = '\0';
    arg1[0] = '\0';
    arg2[0] = '\0';
    
    // Get command
    token = strtok(input, " \t");
    if (token != NULL) {
        strcpy(command, token);
        count++;
        
        // Get first argument
        token = strtok(NULL, " \t");
        if (token != NULL) {
            strcpy(arg1, token);
            count++;
            
            // Get second argument
            token = strtok(NULL, " \t");
            if (token != NULL) {
                strcpy(arg2, token);
                count++;
                
                // Check for extra arguments
                token = strtok(NULL, " \t");
                if (token != NULL) {
                    count++;
                }
            }
        }
    }
    
    return count;
}

// Function to execute DOS commands
void execute_command(char *command, char *arg1, char *arg2, int arg_count) {
    char unix_command[MAX_COMMAND];
    
    // Convert command to lowercase for comparison
    for (int i = 0; command[i]; i++) {
        command[i] = tolower(command[i]);
    }
    
    // Show current directory before command execution
    printf("\nBefore command execution:\n");
    show_pwd();
    printf("\n");
    
    if (strcmp(command, "cd") == 0) {
        // Change directory
        if (arg_count == 2) {
            if (chdir(arg1) == 0) {
                printf("Directory changed successfully.\n");
            } else {
                perror("Error changing directory");
            }
        } else if (arg_count < 2) {
            printf("Error: Too few arguments. Usage: cd <directory>\n");
        } else {
            printf("Error: Too many arguments. Usage: cd <directory>\n");
        }
    }
    else if (strcmp(command, "dir") == 0) {
        // List directory
        if (arg_count == 1) {
            system("ls -la");
        } else if (arg_count == 2) {
            snprintf(unix_command, MAX_COMMAND, "ls -la %s", arg1);
            system(unix_command);
        } else {
            printf("Error: Too many arguments. Usage: dir [directory]\n");
        }
    }
    else if (strcmp(command, "type") == 0) {
        // Display file contents
        if (arg_count == 2) {
            snprintf(unix_command, MAX_COMMAND, "cat %s", arg1);
            system(unix_command);
        } else if (arg_count < 2) {
            printf("Error: Too few arguments. Usage: type <filename>\n");
        } else {
            printf("Error: Too many arguments. Usage: type <filename>\n");
        }
    }
    else if (strcmp(command, "del") == 0) {
        // Delete file
        if (arg_count == 2) {
            snprintf(unix_command, MAX_COMMAND, "rm %s", arg1);
            int result = system(unix_command);
            if (result == 0) {
                printf("File deleted successfully.\n");
            }
        } else if (arg_count < 2) {
            printf("Error: Too few arguments. Usage: del <filename>\n");
        } else {
            printf("Error: Too many arguments. Usage: del <filename>\n");
        }
    }
    else if (strcmp(command, "ren") == 0) {
        // Rename/move file
        if (arg_count == 3) {
            snprintf(unix_command, MAX_COMMAND, "mv %s %s", arg1, arg2);
            int result = system(unix_command);
            if (result == 0) {
                printf("File renamed successfully.\n");
            }
        } else if (arg_count < 3) {
            printf("Error: Too few arguments. Usage: ren <old_name> <new_name>\n");
        } else {
            printf("Error: Too many arguments. Usage: ren <old_name> <new_name>\n");
        }
    }
    else if (strcmp(command, "copy") == 0) {
        
        if (arg_count == 3) {
            snprintf(unix_command, MAX_COMMAND, "cp %s %s", arg1, arg2);
            int result = system(unix_command);
            if (result == 0) {
                printf("File copied successfully.\n");
            }
        } else if (arg_count < 3) {
            printf("Error: Too few arguments. Usage: copy <source> <destination>\n");
        } else {
            printf("Error: Too many arguments. Usage: copy <source> <destination>\n");
        }
    }
    else if (strcmp(command, "pwd") == 0) {
        // Show current directory
        show_pwd();
    }
    else if (strcmp(command, "help") == 0) {
        // Display help information
        printf("\nAvailable DOS Commands:\n");
        printf("  cd <directory>              - Change directory\n");
        printf("  dir [directory]             - List directory contents\n");
        printf("  type <filename>             - Display file contents\n");
        printf("  del <filename>              - Delete a file\n");
        printf("  ren <old_name> <new_name>   - Rename a file\n");
        printf("  copy <source> <destination> - Copy a file\n");
        printf("  pwd                         - Show current directory\n");
        printf("  help                        - Show this help message\n");
        printf("\n");
    }
    else if (strlen(command) == 0) {
        // Empty command
        return;
    }
    else {
        printf("Error: Unknown command '%s'. Type 'help' for available commands.\n", command);
    }
    
    // Show current directory after command execution
    printf("\nAfter command execution:\n");
    show_pwd();
    printf("\n");
}

int main() {
    char input[MAX_INPUT];
    char command[MAX_INPUT];
    char arg1[MAX_INPUT];
    char arg2[MAX_INPUT];
    int arg_count;
    
    // Display welcome message
    printf("====================================\n");
    printf("  DOS Command Interpreter in C\n");
    printf("====================================\n");
    printf("Type 'help' for available commands\n");
    printf("Type Ctrl-C to exit\n");
    printf("====================================\n\n");
    
    // Main command loop
    while (1) {
        printf("DOS> ");
        fflush(stdout);
        
        // Read input
        if (fgets(input, MAX_INPUT, stdin) == NULL) {
            break;
        }
        
        // Trim whitespace
        trim(input);
        
        // Skip empty lines
        if (strlen(input) == 0) {
            continue;
        }
        
        // Parse input
        arg_count = parse_input(input, command, arg1, arg2);
        
        // Execute command
        execute_command(command, arg1, arg2, arg_count);
    }
    
    printf("\nExiting DOS Command Interpreter.\n");
    return 0;
}

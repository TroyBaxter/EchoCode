import winsound
import time

def run_file(path):
    file_content = open(path, "r")
    for line in file_content:
        current_line = line
        if "print" in current_line:
            print_line = current_line.replace("print", "")
            print(print_line)

        elif "makesound" in current_line:
            refined_makesound = current_line.replace("makesound","")
            winsound.Beep(int(refined_makesound), 100)

        elif "math" in current_line:
            refined_math = current_line.replace("math","")
            math = refined_math.split()
            if "+" in math:
                print(int(math[0])+int(math[2]))

            elif "-" in math:
                print(int(math[0])-int(math[2]))

            elif "*" in math:
                print(int(math[0])*int(math[2]))

            elif "/" in math:
                print(int(math[0])/int(math[2]))


        elif "help" in current_line:
            print("""The current commands supported are:
    print: Prints a message to the console
    makesound: Makes a low, mid or high sound
    math: Do simple arithmatic
    pause: DISABLED DUE TO BUGS
    help: Displays current supported commands
            """)

        else:
            print("Error: Unknown command")

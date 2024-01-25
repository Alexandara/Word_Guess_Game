import sys

if __name__ == '__main__':
    # Instruction 1
    # Opens the file passed in as a system argument or else terminates
    try:
        file = open(str(sys.argv[1]), "r")
    except:
        print("Please provide the filename as a system argument.")
        exit(1)
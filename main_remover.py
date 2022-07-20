import os, sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def remove_main(file_path):
    with open(file_path, "r") as f:
        content = f.readlines()

    for i, l in enumerate(content):
        if l.startswith("#include") and "unistd" not in l:
            print(bcolors.OKGREEN + "found not authorized include, removing it on file " + file_path)
            content[i] = "//" + content[i]
        if "int	main(void)" in l:
            print(bcolors.OKBLUE + "found main on file: " + file_path)
            if i == 0 or not "/*" in content[i - 1]:
                print(bcolors.OKCYAN + "start comment not found on file: " + file_path)
                print(bcolors.OKGREEN + "adding starting comment...")
                content.insert(i, "/*\n")
            
                while i < len(content):
                    if content[i].startswith("}"):
                        print(bcolors.OKBLUE + "found end of main function on file: " + file_path)
                        if (i + 1 < len(content) and "*/" not in content[i + 1]) or i + 1 == len(content):
                            print(bcolors.OKCYAN + "end comment not found on file: " + file_path)
                            print(bcolors.OKGREEN + "adding ending comment...")
                            if i + 1 > len(content):
                                content.append("\n*/")
                            else:
                                content.insert(i + 1, "*/")
                        break
                    i += 1
                break
    
    print(bcolors.OKGREEN + "writing content on file " + file_path)
    with open(file_path, "w") as f:
        f.writelines(content)

if __name__ == "__main__":
    count = 0
    path = sys.argv[1]
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith(".c"):
                    print(bcolors.ENDC + "testing " + os.path.join(root, name))
                    count += 1
                    remove_main(os.path.join(root, name))
        print(bcolors.OKGREEN + f"Found {count} .c files")
    else:
        remove_main(path)
    print(bcolors.ENDC)
    norminette = os.system("norminette " + path)
    if(norminette != 0):
        print(bcolors.FAIL + "Erreur de norme !")
        exit(norminette)
    else:
        print(bcolors.OKGREEN + "Norminette : OK !")

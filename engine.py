import json
import os, sys
import time
from colorama import Fore, Style, init
"""
    CONSOLE

    - A console to handle users requests, to manipulate the templates and the Storage
"""
class CONSOLE():

    def __init__(self):
        self.__templates = {}
        self.__html_pages = {}
        self.__preattify = True# SET PRETIFIE
        self.__search_margin = 100
        # check directories and load templates
        self.__directory_checker()

    
    def __help(self):
        commands_help = {
            "clear":"Clear console",
            "render":"Render all_files",
            "reloadall":"reaload all <template.html> into memorie",
            "show": "show loaded html files from templates",
            "exit": "exit the console",
        }
        print("+++++++++++++HELP+++++++++++++++++", file=sys.stdout)
        for key, value in commands_help.items():
            print(f"{key} :  {value}"+"\n", file=sys.stdout)
        print("++++++++++++++++++++++++++++++++++", file=sys.stdout)
    def __clear(self):
        try:
            os.system("clear")
            return
        except:
            pass

        try:
            os.system("clear")
            return
        except:
            pass
    def __showloaded(self):
        for file in self.__templates.keys():
            print(file, file=sys.stdout)
    def __reloadall(self):
        # flush dict
        self.__templates = {}
        # reaload all
        self.__directory_checker()
    def __exit(self):
        print("SEE YA !", file=sys.stdout)
        sys.exit(0)


    def __directory_checker(self):
        """__directory_checker
            - this function checks the current path for the needed directories for the engine
            to function.
        """

        # list of needed directories
        dirs = ("html_pages","templates") 
        # the path the script is currently runing on
        path = (os.getcwd())
        # a list of all files/directories in the path
        dir_list = os.listdir(path)

        # check for the needed files
        dir1_found = False
        dir2_found = False

        for dirs_or_files in dir_list:
            if (dirs_or_files == dirs[0]):
                dir1_found = True
            if (dirs_or_files == dirs[1]):
                dir2_found = True

            # if the two are found break
            if (dir1_found and dir2_found):
                break

        # handle missing
        if (dir1_found == False):
            print("[-] [ html_pages ] dir is Missing , please create the directory", file=sys.stderr)
        if (dir2_found == False):
            print("[-] [ templates ] dir is Missing , please create the directory", file=sys.stderr)

        # since one of the  dirs does not exist return
        if (dir1_found is False or dir2_found is False):
            return

        self.__load_render_list(path)

    def __load_render_list(self, current_path):
        """__load_render_list

            - load files from the templates directory, into memorie (dict)

            ARGS:
                current_path: the path passed by the __directory_checker
                after checking if the dirs are set
        """
        # list of two paths , 1> html_pages 2> templates
        paths = [current_path+"/html_pages", current_path+"/templates"]
        
        for path in range(len(paths)):
            # get all files iside of the path
            dir_list = os.listdir(paths[path])
            for file in dir_list:

                # only load files with html extention
                splited_file_name = file.split('.') # example  index.html > ["index", "html"]
                if (splited_file_name[1] == "html"):

                    if (path == 0):# if we're loading the html_pages
                        self.__html_pages[splited_file_name[0]] = f"{current_path}/html_pages/{file}"
                    elif (path == 1):# if we're loading the templates
                        self.__templates[splited_file_name[0]] = f"{current_path}/templates/{file}"

    def __render(self):
        # start a time to log to the user how mush time the render took
        start_time = time.time()



        # render each html_page
        for html_page, page_path in self.__html_pages.items():
            lines = None
            with open(f"{page_path}" , "r+") as page:
                lines = page.readlines()
                target_line = -1
                # for each line in the lines read
                for line in lines:
                    target_line += 1

                    # for each charachter in a line
                    for char in range(len(line)):

                        # if the special character for the template declaration is found
                        if (line[char] == "{"):
                            # keep track of how many character did we search , not exceed the self.__search_margin 
                            # see __init__
                            chars_searched = 0
                            # set the starting pointer
                            start = (char + 1)
                            # find the closing special character, with respect to the self.__search_margin
                            while (line[char] != "}"):
                                if (char > self.__search_margin):
                                    break
                                chars_searched += 1
                                char+=1
                            # if we acceded the search_ margin then ignore the rest and search
                            # for the next opening token
                            if (char > self.__search_margin):
                                    break
                            # get the slice
                            template_name = line[start:char]
                            
                            
                            # check if the template is loaded
                            # if not print error
                            if (template_name not in  self.__templates):
                                print(f"[x] line> {target_line}:{start} Template with name `{template_name}` does't exist", file=sys.stderr)
                                return

                            
                                
                            with open(f"templates/{template_name}.html", 'r') as template:
                                # load the template into it's respected line
                                # with respect to how many spaces we've found "{"

                                # load the template into its respected line
                                # with respect to how many spaces we've found "{"
                                template_content = template.read().strip('\n')

                                # if preattify is false, then load the template as a one liner
                                if not self.__preattify:
                                    lines[target_line] = (" " * (start-1)) + template_content.strip('\n') + '\n'
                                elif self.__preattify:
                                    lines[target_line] = (" " * (start-1)) + template_content + '\n'

            with open(f"{html_page}.html", 'w') as file:
                file.writelines(lines)
                file.truncate()

        end_time = time.time()
        # Initialize colorama
        init(autoreset=True)
        print("[RENDER RUNTIME]",(end_time-start_time) * 10**3,"ms", file=sys.stdout)



                            
                    
                
                










        
        
    def run_console(self):
        mapper = {
            "clear" : self.__clear,
            "show": self.__showloaded,
            "reloadall": self.__reloadall,
            "exit": self.__exit,
            "render": self.__render,
            "help":self.__help
        }

        while (True):
            prompt = input("$ ")
            
            if (prompt in mapper):
                mapper[prompt.strip()]()
            else:
                print ("[-] command not found  , type help to see availble commands", file=sys.stdout)
        



CONSOL = CONSOLE()
CONSOL.run_console()

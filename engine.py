import copy
import os, sys
import time
import threading
import datetime


"""
    CONSOLE

    - A console to handle users requests, to manipulate the templates and the Storage
"""
class CONSOLE():

    def __init__(self):
        self.__templates = {}
        self.__html_pages = {}
        self.__files_time_stamp = {}
        self.__preattify = True# SET PRETIFIE
        self.__search_margin = 100
        self._msg_stack = []
        # check for system , to handle the path formating
        self.__path_formater = '/'
        if sys.platform.startswith('win'):
            self.__path_formater = "\\"
        elif not sys.platform.startswith('linux'):
            print("[!] May not work on this system", file=sys.stdout)
            input("Return to continue")


        # check directories and load templates
        self.__directory_checker()
        # thread exit flag
        self.__thread_exit_Flag = False
        # auto reload thread
        self._th = threading.Thread(target=self.auto_render_)
        # start thread at the initialization of the object
        self._th.start()

    def auto_render_(self):
        """auto_render_
            auto render is the function that will be called by the auto reload
            thread.
        :return: None
        """
        while self.__thread_exit_Flag is False:
            time.sleep(1)  # cycle every (sec)

            # well since self.... is a reference to a chunk of memory it wouldn't make
            # any sense to keep referencing the same snapshot of it , this is why we need a copy
            # of that chunk at every cycle
            tmp_curr_timestamp = copy.copy(self.__files_time_stamp)
            
            # reload files
            self.__reloadall()
            # if the two dicts are not the same , a file has been changed
            if (tmp_curr_timestamp != self.__files_time_stamp):
                # trigger re rendering
                self.__render()

    def __help(self):
        commands_help = {
            "cl":"Clear console",
            "render":"Render all_files",
            "reloadall":"reaload all <template.html> into memorie",
            "show": "show loaded html files from templates",
            "exit": "exit the console",
        }
        print("+++++++++++++HELP+++++++++++++++++", file=sys.stdout)
        for key, value in commands_help.items():
            print(f"{key} :  {value}"+"\n", file=sys.stdout)
        print("++++++++++++++++++++++++++++++++++", file=sys.stdout)


    def __directory_checker(self):
        """__directory_checker
            - this function checks the current path for the needed directories for the engine
            to function.
        """

        # empty all dicts at every render for realtime file tracking
        self.__Template_files_time_stamp, self.__Html_files_time_stamp = {},{}
        self.__html_pages = {}
        self.__templates = {}


        # list of needed directories
        dirs = ("html_pages","templates") 
        # the path the script is currently running on
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

            - load files from the templates directory, into memory (dict)

            ARGS:
                current_path: the path passed by the __directory_checker
                after checking if the dirs are set
        """
        # list of two paths , 1> html_pages 2> templates
        paths = [current_path+self.__path_formater+"html_pages", current_path+self.__path_formater+"templates"]
        
        for path in range(len(paths)):
            # get all files in the path
            dir_list = os.listdir(paths[path])
            for file in dir_list:

                # only load files with html extension
                splited_file_name = file.split('.') # example  index.html > ["index", "html"]
                if (splited_file_name[1] == "html"):

                    if (path == 0):# if we're loading the html_pages
                        file_full_path = f"{current_path}{self.__path_formater}html_pages{self.__path_formater}{file}"
                        self.__html_pages[splited_file_name[0]] = file_full_path
                        # get time stamp of the file

                        self.__files_time_stamp[splited_file_name[0]] = round(os.path.getmtime(file_full_path), 2)

                    elif (path == 1):# if we're loading the templates
                        file_full_path = f"{current_path}{self.__path_formater}templates{self.__path_formater}{file}"
                        self.__templates[splited_file_name[0]] = file_full_path
                        # get time stamp of the file

                        self.__files_time_stamp[splited_file_name[0]] = round(os.path.getmtime(file_full_path), 2)

    def __render(self, *skip_list):
        # start a time to log to the user how mush time the render took
        start_time = time.time()

        # render each html_page
        for html_page, page_path in self.__html_pages.items():

            if (html_page in skip_list): break

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

                            
                                
                            with open(f"templates{self.__path_formater}{template_name}.html", 'r') as template:
                                # load the template into it's respected line
                                # with respect to how many spaces we've found "{"

                                # load the template into its respected line
                                # with respect to how many spaces we've found "{"
                                template_content = template.read().strip('\n')

                                # if preattify is false, then load the template as oneliner
                                if not self.__preattify:
                                    lines[target_line] = (" " * (start-1)) + template_content.strip('\n') + '\n'
                                elif self.__preattify:
                                    lines[target_line] = (" " * (start-1)) + template_content + '\n'

            with open(f"{html_page}.html", 'w') as file:
                file.writelines(lines)
                file.truncate()
                file.close()

        end_time = time.time()

        # add message to the message stack
        self._msg_stack.append("[RENDER RUNTIME]"+str((end_time-start_time) * 10**3)+"ms")

    """THE CONSOLE LOGIC"""
    def run_console(self):
        mapper = {
            "clear" : self.__clear,
            "show": self.__showloaded,
            "reloadall": self.__reloadall,
            "exit": self.__exit,
            "render": self.__render,
            "help":self.__help,
        }

        while (True):
            for x in self._msg_stack:
                print (x)
                self._msg_stack = []

            prompt = input("[console]$ ")
            
            if (prompt in mapper):
                mapper[prompt.strip()]()
            else:
                print ("[-] command not found  , type help to see availble commands", file=sys.stdout)

    """HERE IS THE CONSOLE FUNCTION"""
    def __clear(self):
        try:
            os.system("clear")
            os.system("cls")
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
        # signal to the thread to end
        self.__thread_exit_Flag = True
        self._th.join()
        sys.exit(0)




if __name__ == "__main__":
    print("""

     ███▄    █ ▒█████  ▄▄▄█████▓              
     ██ ▀█   █▒██▒  ██▒▓  ██▒ ▓▒              
    ▓██  ▀█ ██▒██░  ██▒▒ ▓██░ ▒░              
    ▓██▒  ▐▌██▒██   ██░░ ▓██▓ ░               
    ▒██░   ▓██░ ████▓▒░  ▒██▒ ░               
    ░ ▒░   ▒ ▒░ ▒░▒░▒░   ▒ ░░                 
    ░ ░░   ░ ▒░ ░ ▒ ▒░     ░                  
       ░   ░ ░░ ░ ░ ▒    ░                    
             ░    ░ ░                         

     ██▀███  ▓█████ ▄▄▄      ▄████▄  ▄▄▄█████▓
    ▓██ ▒ ██▒▓█   ▀▒████▄   ▒██▀ ▀█  ▓  ██▒ ▓▒
    ▓██ ░▄█ ▒▒███  ▒██  ▀█▄ ▒▓█    ▄ ▒ ▓██░ ▒░
    ▒██▀▀█▄  ▒▓█  ▄░██▄▄▄▄██▒▓▓▄ ▄██▒░ ▓██▓ ░ 
    ░██▓ ▒██▒░▒████▒▓█   ▓██▒ ▓███▀ ░  ▒██▒ ░ 
    ░ ▒▓ ░▒▓░░░ ▒░ ░▒▒   ▓▒█░ ░▒ ▒  ░  ▒ ░░   
      ░▒ ░ ▒░ ░ ░  ░ ▒   ▒▒ ░ ░  ▒       ░    
      ░░   ░    ░    ░   ▒  ░          ░      
       ░        ░  ░     ░  ░ ░               
                            ░ 
    """)
    CONSOL = CONSOLE()
    CONSOL.run_console()

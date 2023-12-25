
# NOT REACT
A simple html injector, works by injecting templates into an html file.



## how to use it

#### Clone the project


First of all NOT REACT works with specific directories, you dont have to worry about that since cloning this repo get the directories needed.

```bash
└───NOT_REACT-main
    ├───html_pages
    └───templates
```
#### ! the script wont function if these two dirs dont exist

#### Go to the project directory


## run the engine
 ```cmd
python3 engine.py
 ```

#### the script shell will run , you can use the command help to see what you can do 
```cmd
$ help
+++++++++++++HELP+++++++++++++++++
clear :  Clear console

render :  Render all_files

reloadall :  reaload all <template.html> into memorie

show :  show loaded html files from templates

exit :  exit the console

++++++++++++++++++++++++++++++++++

```

#### now , let's talk about the `render` command and what it will do , but first how to use NOT REACT.

# 1) Create an html page in the `html_page` folder
## note you can create as many pages as you like to

### you specifie wich template to inject at what position by mentioning the name of the template inside {}
#### the name of the template must exist to be rendered , or an error will be thrown
![carbon](https://github.com/AMINEXD33/NOT_REACT/assets/89471262/bafec072-9d4a-4eb3-8769-eb17fa3c9bd8)


# 2) Create some templates
## note you can create as many templates as you like to

### The `navbar` template 
![carbon (1)](https://github.com/AMINEXD33/NOT_REACT/assets/89471262/4c3f6f08-56df-4b7a-b31f-79f35bc9ae7b)

### The `list` template 
![carbon (2)](https://github.com/AMINEXD33/NOT_REACT/assets/89471262/5d598b9f-0489-4791-911d-05442c851ac9)


# 2) render the final pages 
```cmd
$ render
```
## after rendering the templates the full html pages will be writen into the root directory with the same names as the html files iside `html_files` 


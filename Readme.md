## A new casual way to format your md files

![mdpickmelink.gif](https://oneyardline.cn/mdpickmelink.gif)


## action workflow

 * select line
 * a new focus window from bottom
 * a selection list with markup suggestions
 * render the selected line


When you choose a header
![mdpickmeheader.gif](https://oneyardline.cn/mdpickmeheader.gif)

## baseline project

[https://github.com/chmp/mdnav]( https://github.com/chmp/mdnav)

1. it use python language to do the buffer parser work
2. it use python 'print' to debug the python file
3. it has similar interaction I want to create, choose a line, and parser the line, and then do the result action

	nvim -V9myvim.log

with this nvim launch code line, you can log out the print code you embeded into,both
in the log file 'myvim.log', and the vim output window

## Installation

### Installation using [Vim-Plug](https://github.com/junegunn/vim-plug)

Add the following to the plugin-configuration in your vimrc:

	Plug 'tbxy09/mdpickme'

Then run `:PlugInstall`.



![mdpickme.gif](http://192.168.1.102:7778/mdpickmeheader.gif)

## action workflow

 * choosed line
 * a new focus window
 * with the markup suggestions render as a selection list
 * sync back to original buffer

## baseline project

[mdnav](mdnav.md)

1. it use python language to do the buffer parser work
2. it use python 'print' to debug the python file
3. it has similar interaction I want to create, choose a line, and parser the line, and then do the result action

```
nvim -V9myvim.log
```
with this nvim launch code line, you can log out the print code you embeded into,both
in the log file 'myvim.log', and the vim output window

## improvement and bug

1. the chinese character handeling
2. multiline code choosing and format
3. a blank line after each header
some thoughts here
setline is the main API to get the buffer from python parser, it can not recognize the breakline from linebuffer, can it input with a multilines, need further check here

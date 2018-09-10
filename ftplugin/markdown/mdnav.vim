" if exists('g:mdnav#PythonScript')
"    finish
"endif

let g:mdnav#PythonScript = expand('<sfile>:r') . '.py'
let g:mdsug#PythonScript = '/data/dotfiles_xy/nvim/plugged/mdnav/ftplugin/markdown/mdsug.py'

function! BPop(mylist)
  let color = '{ x = $1; $1 = ""; z = $3; $3 = ""; printf "\033[34m%s\033[0m:\033[31m%s\033[0m\011\033[37m%s\033[0m\n", x,z,$0; }'
  " \ 'source':  "cscope -dL" . a:option . " " . a:query . " | awk '" . color . "'",
  " \ 'source':  "ls"."|awk '" . color . "'",
  " \ 'source':  map(mylist, 's:format_list(v:val)')
  let opts = {
  \ 'source':  a:mylist,
  \ 'options': ['--ansi', '--prompt', '> ',
  \             '--multi', '--bind', 'alt-a:select-all,alt-d:deselect-all',
  \             '--color', 'fg:188,fg+:222,bg+:#3a3a3a,hl+:104'],
  \ 'down': '40%'
  \ }
  function! opts.sink(line)
    echom a:line
    setlocal cursorline
		" let parsedLine  = substitute(a:line, ',\s*', '\r', "g")
    call setline(line('.'), [a:line])
		silent! exec 's/```\s*/\r```\r/g'
  endfunction
  call fzf#run(opts)
endfunction

command! MDNavExec execute 'pyfile ' . g:mdnav#PythonScript
command! MDSugExec execute 'pyfile ' . g:mdsug#PythonScript

nnoremap <buffer> <leader>n :MDNavExec<CR>
nnoremap <buffer> <CR> :MDSugExec<CR>

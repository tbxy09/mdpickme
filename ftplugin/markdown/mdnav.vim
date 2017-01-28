" if exists('g:mdnav#PythonScript')
"    finish
"endif

let g:mdnav#PythonScript = expand('<sfile>:r') . '.py'

command! MDNavExec execute 'pyfile ' . g:mdnav#PythonScript
nnoremap <CR> :MDNavExec<CR>

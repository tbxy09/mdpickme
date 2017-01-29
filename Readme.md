# mdnav - vim plugin for navigating links in markdown files

Vim plugin for navigating links in markdown files.
It can handle:

- **internal link**:
    for example `[Section 1](#section-1)`, will link to the heading 
    `# Section 1`.
- **direct links**:
    for example `[foo](bar.md)`.
- **indirect links**:
    for links of the form `[foo][label]`, mdnav will lookup the corresponding
    label and open the target referenced there.
- **non text files**:
    if the option `g:mdnav#Extensions` is set, non text files will be opened
    via the operating system. This behavior is handy when linking to binary
    documents, for example PDFs.
- **local link format of pelican**:
    mdnav handles `|filename| ...` links as expected.

While mdnav is inspired by [follow-markdown-links][fml], mdnav can handle many
more link formats and types of link targets (MD files, URLs, non text files,
...).

[fml]: https://github.com/prashanthellina/follow-markdown-links

## Usage

Install the plugin via your favorite plugin manager, say [Vundle][vundle].
Inside normal model with an open markdown document, you may press enter on a
markdown link to open it.
If the link is a local file it will be opened in vim, otherwise it will be
opened by the current webbrowser.

The following links can be used (the possible cursor positions are indicated by
`^`):


    This [link](https://example.com) will be opened inside the browser.
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^

    This [link](./foo.md) will open `./foo.md` inside vim.
         ^^^^^^^^^^^^^^^^

    This [link](|filename|./foo.md) will open `./foo.md` inside vim.
         ^^^^^^^^^^^^^^^^^^^^^^^^^^

    If `g:mdnav#Extensions` is set to `.md, .MD`, enter will open
    `example.pdf` inside the default PDF reader for this
    [link](|filename|./example.pdf).
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Indirect [links][indirect-link] work too.
             ^^^^^^^^^^^^^^^^^^^^^^

    [indirect-link]: http://example.com


The behavior of mdnav can be configured via the following options:

- `g:mdnav#Extensions`:
    a comma separated list of file extensions.
    Only file s with the given extensions will be opened in vim, all other
    files will be opened via the configured application (using `open` on OSX
    and `xdg-open` on linux).
    This option may be useful to link to non-text documents, say PDF files.

- `g:mdnav#DebugMode`:
    if set to `true` it, extensive debug information will be logged.

To work, vim needs to be configured with python support.

## Running tests

	pip install -r test-requirements.txt
	python -m pytest tests

## License

>  The MIT License (MIT)
>  Copyright (c) 2017 Christopher Prohm
>
>  Permission is hereby granted, free of charge, to any person obtaining a copy
>  of this software and associated documentation files (the "Software"), to
>  deal in the Software without restriction, including without limitation the
>  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
>  sell copies of the Software, and to permit persons to whom the Software is
>  furnished to do so, subject to the following conditions:
>
>  The above copyright notice and this permission notice shall be included in
>  all copies or substantial portions of the Software.
>
>  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
>  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
>  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
>  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
>  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
>  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
>  DEALINGS IN THE SOFTWARE.

[vundle]: https://github.com/VundleVim/Vundle.vim


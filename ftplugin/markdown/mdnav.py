from __future__ import print_function

import collections
import json
import os.path
import re
import sys
import subprocess
import webbrowser

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class FakeLogger(object):
    def __init__(self, active=False):
        self.active = active

    def info(self, fmt, *args):
        if not self.active:
            return

        print(fmt % args)


_logger = FakeLogger()


def plugin_entry_point():
    import vim

    if int(vim.eval("exists('g:mdnav#Extensions')")):
        extensions = vim.eval('g:mdnav#Extensions')
        extensions = [ext.strip() for ext in extensions.split(',')]

    else:
        extensions = []

    if int(vim.eval("exists('g:mdnav#DebugMode')")):
        _logger.active = vim.eval('g:mdnav#DebugMode') == 'true'

    row, col = vim.current.window.cursor
    cursor = (row - 1, col)
    lines = vim.current.buffer

    target = parse_link(cursor, lines)
    _logger.info('open %s', target)
    action = open_link(
        target,
        current_file=vim.eval("expand('%:p')"),
        open_in_vim_extensions=extensions,
    )
    action()


def open_link(target, current_file, open_in_vim_extensions=set()):
    """
    :returns: a callable that encapsulates the action to perform
    """
    if target is not None:
        target = target.strip()

    if not target:
        _logger.info('no target')
        return NoOp(target)

    if target.startswith('#'):
        return JumpToAnchor(target)

    if has_scheme(target):
        _logger.info('has scheme -> open in browser')
        return BrowserOpen(target)

    if not has_extension(target, open_in_vim_extensions):
        _logger.info('has no extension for opening in vim')
        return OSOpen(anchor_path(target, current_file))

    if target.startswith('|filename|'):
        target = target[len('|filename|'):]

    return VimOpen(anchor_path(target, current_file))


def anchor_path(target, current_file):
    if os.path.isabs(target):
        return target

    _logger.info('anchor path relative to %s', current_file)
    return os.path.join(os.path.dirname(current_file), target)


def has_extension(path, extensions):
    if not extensions:
        return True

    path = parse_path(path)
    _, ext = os.path.splitext(path.path)
    return ext in extensions


def has_scheme(target):
    return bool(urlparse(target).scheme)


class Action(object):
    def __init__(self, target):
        self.target = target

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.target)


class NoOp(Action):
    def __call__(self):
        print('<mdnav: no link>')


class BrowserOpen(Action):
    def __call__(self):
        print('<mdnav: open browser tab>')
        webbrowser.open_new_tab(self.target)


class OSOpen(Action):
    def __call__(self):
        if sys.platform.startswith('linux'):
            call(['xdg-open', self.target])

        elif sys.platform.startswith('darwin'):
            call(['open', self.target])

        else:
            os.startfile(self.target)


class VimOpen(Action):
    def __call__(self):
        import vim

        path = parse_path(self.target)

        # TODO: make space handling more robust?
        vim.command('e {}'.format(path.path.replace(' ', '\\ ')))
        if path.line is not None:
            vim.command(':{}'.format(path.line))


class JumpToAnchor(Action):
    heading_pattern = re.compile(r'^#+(?P<title>.*)$')

    def __call__(self):
        import vim
        line = self.find_anchor(self.target, vim.current.buffer)

        if line is None:
            return

        vim.current.window.cursor = (line + 1, 0)

    @classmethod
    def find_anchor(cls, target, buffer):
        needle = cls.norm_target(target)

        for (idx, line) in enumerate(buffer):
            m = cls.heading_pattern.match(line)
            if m is None:
                continue

            anchor = cls.title_to_anchor(m.group('title'))

            if needle == anchor:
                return idx

    @staticmethod
    def title_to_anchor(title):
        return '-'.join(fragment.lower() for fragment in title.split())

    @staticmethod
    def norm_target(target):
        if target.startswith('#'):
            target = target[1:]

        return target.lower()


def call(args):
    """If available use vims shell mechanism to work around display issues
    """
    try:
        import vim

    except ImportError:
        subprocess.call(args)

    else:
        args = ['shellescape(' + json.dumps(arg) + ')' for arg in args]
        vim.command('execute "! " . ' + ' . " " . '.join(args))


def parse_path(path):
    path, ext = os.path.splitext(path)
    if ':' in ext:
        ext, line = ext.rsplit(':', 1)
        return ParsedPath(path=path + ext, line=line)

    return ParsedPath(path=path + ext, line=None)


class ParsedPath(collections.namedtuple('ParsedPath', ['path', 'line'])):
    pass


def parse_link(cursor, lines):
    row, column = cursor
    line = lines[row]

    _logger.info('handle line %s (%s, %s)', line, row, column)
    link_text, rel_column = select_from_start_of_link(line, column)

    if not link_text:
        _logger.info('could not find link text')
        return None

    m = link_pattern.match(link_text)

    if not m:
        _logger.info('does not match link pattern')
        return None

    if m.end('link') <= rel_column:
        _logger.info('cursor outside link')
        return None

    _logger.info('found match: %s', m.groups())
    assert (m.group('direct') is None) != (m.group('indirect') is None)

    if m.group('direct') is not None:
        _logger.info('found direct link: %s', m.group('direct'))
        return m.group('direct')

    _logger.info('follow indirect link %s', m.group('indirect'))
    indrect_link_pattern = re.compile(
        r'^\[' + re.escape(m.group('indirect')) + r'\]:(.*)$'
    )

    for line in lines:
        m = indrect_link_pattern.match(line)

        if m:
            return m.group(1).strip()

    _logger.info('could not match for indirect link')
    return None


link_pattern = re.compile(r'''
    ^
    (?P<link>
        \[                  # start of link text
            [^\]]*          # link text
        \]                  # end of link text
        (?:
            \(                  # start of target
                (?P<direct>
                    [^\)]*
                )
            \)                  # collect
            |
            \[
                (?P<indirect>
                    [^\]]*
                )
            \]
        )
    )
    .*                  # any non matching characters
    $
''', re.VERBOSE)


def select_from_start_of_link(line, pos):
    """Return the start of the link string and the new cursor
    """
    if pos < len(line) and line[pos] == '[':
        start = pos

    else:
        start = line[:pos].rfind('[')

    # TODO: handle escapes

    if start < 0:
        return None, pos

    # check for indirect links
    if start != 0 and line[start - 1] == ']':
        alt_start = line[:start].rfind('[')
        if alt_start >= 0:
            start = alt_start

    return line[start:], pos - start


if __name__ == "__main__":
    plugin_entry_point()


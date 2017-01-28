import pytest
import mdnav

# NOTE: the cursor is indicated with ^, the cursor will be placed on the
# following character
parse_link_cases = [
    # default cases
    (['foo [b^ar](baz.md)'], 'baz.md'),
    (['foo [b^ar](baz.md) [bar](bar.md)'], 'baz.md'),
    (['foo [b^ar][bar]', '[bar]: baz.md'], 'baz.md'),
    (['foo [b^ar][bar]', '[bar]: |filename|./baz.md'], '|filename|./baz.md'),
    (['foo [b^ar][bar] [bar][baz]', '[bar]: |filename|./baz.md'], '|filename|./baz.md'),

    # cursor outside link area
    (['foo^  [bar](baz.md) '], None),
    (['foo ^ [bar](baz.md) '], None),
    (['foo [bar](baz.md) ^ '], None),
    (['foo [bar](baz.md)^  '], None),

    # cursor inside target part
    (['foo [bar][b^ar]', '[bar]: baz.md'], 'baz.md'),
    (['foo [bar](b^az.md) [bar](bar.md)'], 'baz.md'),

    # malformed links
    (['][b^ar](bar.md)'], 'bar.md'),
]


@pytest.mark.parametrize('lines, expected', parse_link_cases)
def test_parse_link(lines, expected):
    cursor, mod_lines = _find_cursor(lines)
    actual = mdnav.parse_link(cursor, mod_lines)
    assert actual == expected


def _find_cursor(lines):
    lines_without_cursor = []
    cursor = None

    for (row, line) in enumerate(lines):
        pos = line.find('^')

        if pos < 0:
            lines_without_cursor.append(line)

        else:
            cursor = (row, pos)
            lines_without_cursor.append(line[:pos] + line[pos + 1:])

    return cursor, lines_without_cursor


open_link_cases = [
    (None, {}, mdnav.NoOp(None)),
    ('baz.md', {}, mdnav.VimOpen('/abs/baz.md')),
    ('baz.MD', {'open_in_vim_extensions': ['md']}, mdnav.OSOpen('baz.MD')),
    ('|filename|/foo/baz.md', {}, mdnav.VimOpen('/foo/baz.md')),
    ('/foo/bar.md', {}, mdnav.VimOpen('/foo/bar.md')),
    ('http://example.com', {}, mdnav.BrowserOpen('http://example.com')),
]


@pytest.mark.parametrize('target, open_link_kwargs, expected', open_link_cases)
def test_open_link(target, open_link_kwargs, expected):
    open_link_kwargs.setdefault('current_file', '/abs/foo.md')
    actual = mdnav.open_link(target, **open_link_kwargs)

    assert actual == expected


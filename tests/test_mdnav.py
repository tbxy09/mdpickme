import pytest
import mdnav

parse_link_cases = [
    ((0, 7), ['foo [bar](baz.md)'], 'baz.md'),
    ((0, 7), ['foo [bar](baz.md) [bar](bar.md)'], 'baz.md'),
    ((0, 7), ['foo [bar][bar]', '[bar]: baz.md'], 'baz.md'),
    ((0, 7), ['foo [bar][bar]', '[bar]: |filename|./baz.md'], '|filename|./baz.md'),
    ((0, 7), ['foo [bar][bar] [bar][baz]', '[bar]: |filename|./baz.md'], '|filename|./baz.md'),
]


@pytest.mark.parametrize('cursor, lines, expected', parse_link_cases)
def test_parse_link(cursor, lines, expected):
    actual = mdnav.parse_link(cursor, lines)
    assert actual == expected


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


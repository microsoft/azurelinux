from pathlib import Path
from textwrap import dedent

from pyproject_requirements_txt import convert_requirements_txt


def test_requirements_add_pkgname():
    reqs_txt = dedent(r"""
        good@git+https://github.com/monty/spam.git@master#egg=bad
        git+https://github.com/monty/spam.git@master#egg=ugly
        https://example.com/undead.tar.gz#egg=undead ; python_version > 3.0
    """)
    result = convert_requirements_txt(reqs_txt.splitlines())

    expected = [
        'good@git+https://github.com/monty/spam.git@master#egg=bad',
        'ugly@git+https://github.com/monty/spam.git@master#egg=ugly',
        'undead@https://example.com/undead.tar.gz#egg=undead ; python_version > 3.0',
    ]
    assert result == expected


def test_requirements_preprocess(monkeypatch):
    reqs_txt = dedent(r"""
        Normal_Req ~= 1.2.0
           whitespace-stripped < 3    <END>

        # indentation is preserved in continuations:
        foo <=\
            30
        bar<=   \
        30
        # names and operators can be split:
        this-was-\
        too-long<\
        =30  

        # this is not a multi-line comment \
        some-dep
             # neither is this \
        other-dep
        another-dep  # but this *is* a multi-line coment \
        so any garbage can be here
        dep-a # and this comment ends with the blank line below \

        dep-b
        ${ENVVAR}
        whitespace-stripped-before-substitution   ${SPACE}
        ${MISSING_ENVVAR}
    """.replace('<END>', ''))
    monkeypatch.setenv('ENVVAR', 'package-from-env')
    monkeypatch.setenv('SPACE', ' ')
    monkeypatch.delenv('MISSING_ENVVAR', raising=False)
    result = convert_requirements_txt(reqs_txt.splitlines())

    expected = [
        'Normal_Req ~= 1.2.0',
        'whitespace-stripped < 3',
        'foo <=    30',
        'bar<=   30',
        'this-was-too-long<=30',
        'some-dep',
        'other-dep',
        'another-dep',
        'dep-a',
        'dep-b',
        'package-from-env',
        'whitespace-stripped-before-substitution    ',
        '${MISSING_ENVVAR}',
    ]
    #result = expected
    assert result == expected

    # This test uses pip internals, so it might break in the future.
    from pip._internal.req.req_file import preprocess
    expected = [line for lineno, line in preprocess(reqs_txt)]
    assert result == expected


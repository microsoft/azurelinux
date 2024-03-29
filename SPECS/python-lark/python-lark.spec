Summary:        Lark is a modern general-purpose parsing library for Python
Name:           python-lark
Version:        1.1.7
Release:        4%{?dist}
# License breakdown:
# lark/tools/standalone.py - MPL-2.0
# lark/__pyinstaller/hook-lark.py - GPL-2.0-or-later
# the rest is MIT
License:        MIT AND MPL-2.0 AND GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/lark-parser/lark
Source0:        %{pypi_source lark}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildArch:      noarch

%description
Lark is a modern general-purpose parsing library for Python.

Lark focuses on simplicity and power. It lets you choose between
two parsing algorithms:

Earley : Parses all context-free grammars (even ambiguous ones)!
It is the default.

LALR(1): Only LR grammars. Outperforms PLY and most if not all
other pure-python parsing libraries.

Both algorithms are written in Python and can be used interchangeably
with the same grammar (aside for algorithmic restrictions).
See "Comparison to other parsers" for more details.

Lark can auto magically build an AST from your grammar, without any
more code on your part.

Features:

- EBNF grammar with a little extra
- Earley & LALR(1)
- Builds an AST auto magically based on the grammar
- Automatic line & column tracking
- Automatic token collision resolution (unless both tokens are regexps)
- Python 2 & 3 compatible
- Unicode fully supported

%package -n python3-lark
Summary:        %{summary}
BuildRequires:  python3-devel
Obsoletes:      python3-lark-parser < 1
%py_provides    python3-lark-parser

%description -n python3-lark
Lark is a modern general-purpose parsing library for Python. With Lark, you can
parse any context-free grammar, efficiently, with very little code.

Main Features:
    - Builds a parse-tree (AST) automagically, based on
      the structure of the grammar
    - Earley parser
    - Can parse all context-free grammars
    - Full support for ambiguous grammars
    - LALR(1) parser
    - Fast and light, competitive with PLY
    - Can generate a stand-alone parser
    - CYK parser, for highly ambiguous grammars
    - EBNF grammar
    - Unicode fully supported
    - Automatic line & column tracking
    - Standard library of terminals (strings, numbers, names, etc.)
    - Import grammars from Nearley.js
    - Extensive test suite
    - And much more! Since version 1.0, only Python versions 3.6 and up
      are supported.

%prep
%autosetup -p1 -n lark-%{version}

# Fix wrong-file-end-of-line-encoding.
sed -i 's/\r$//' README.md examples/*.py


%build
%{pyproject_wheel}
# This package was renamed from python-lark-parser and we want to provide the old distinfo
# for packages that still need it.
%global legacy_distinfo lark_parser-%{version}.dist-info
mkdir %{legacy_distinfo}
cat > %{legacy_distinfo}/METADATA << EOF
Metadata-Version: 2.1
Name: lark-parser
Version: %{version}
EOF
echo rpm > %{legacy_distinfo}/INSTALLER

%install
%{pyproject_install}
%pyproject_save_files lark

cp -a %{legacy_distinfo} %{buildroot}%{python3_sitelib}

%check
%{python3} -m tests

%files -n python3-lark -f %{pyproject_files}
%doc README.md examples
%{python3_sitelib}/%{legacy_distinfo}/

%changelog
* Fri Mar 29 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.1.7-4
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 27 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.1.7-1
- Rename from lark-parser to lark
- Update to 1.1.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.9.0-10
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-7
- Don't import deprecated sre_parse and sre_constants modules

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.9.0-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 05 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8.2-2
- Rebuilt for Python 3.9

* Sat Mar 07 2020 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.8.2-1
- Update to 0.8.2

* Mon Feb 24 2020 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.8.1-1
- Update to 0.8.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Thomas Andrejak <thomas.andrejak@c-s.fr> - 0.7.8-1
- Update to 0.7.8

* Fri Oct 25 2019 Thomas Andrejak <thomas.andrejak@c-s.fr> - 0.7.7-1
- Update to 0.7.7

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Scott K Logan <logans@cottsay.net> - 0.7.1-1
- Update to 0.7.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.6.4-2
- Fix package naming

* Mon Sep 24 2018 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.6.4-1
- Initial package

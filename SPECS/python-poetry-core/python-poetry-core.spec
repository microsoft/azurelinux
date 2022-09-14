%global pypi_name poetry-core

Summary:        Poetry PEP 517 Build Backend
Name:           python-poetry-core
Version:        1.0.7
Release:        2%{?dist}

# We bundle a lot of libraries with poetry, which itself is under MIT license.
# Here is the list of the libraries with corresponding licenses:

# attrs: MIT
# jsonschema: MIT
# lark-parser: MIT
# packaging: ASL 2.0 or BSD
# pyparsing: MIT
# pyrsistent: MIT
# six: MIT
# tomlkit: MIT

License:        MIT and (ASL 2.0 or BSD)
URL:            https://github.com/python-poetry/poetry-core
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
Requires:       python3

%global _description %{expand:
A PEP 517 build backend implementation developed for Poetry.
This project is intended to be a light weight, fully compliant, self-contained
package allowing PEP 517 compatible build frontends to build Poetry managed
projects.}

%description %_description

%package -n python3-poetry-core
Summary:        %{summary}

# Previous versions of poetry included poetry-core in it
Conflicts:      python%{python3_version}dist(poetry) < 1.1
# The bundled versions are taken from poetry/core/_vendor/vendor.txt
Provides:       bundled(python3dist(attrs)) = 20.3
Provides:       bundled(python3dist(jsonschema)) = 3.2
Provides:       bundled(python3dist(lark-parser)) = 0.9
Provides:       bundled(python3dist(packaging)) = 20.9
Provides:       bundled(python3dist(pyparsing)) = 2.4.7
Provides:       bundled(python3dist(pyrsistent)) = 0.16.1
Provides:       bundled(python3dist(six)) = 1.15
Provides:       bundled(python3dist(tomlkit)) = 0.7

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# We sed out shebang from non-execeutable-script to fix rpmlint error.
# This can be removed once we again devendor python-poetry-core and
# the Patch1 is enabled again.
# Upstream PR: https://github.com/Julian/jsonschema/pull/833
sed -i '1!b;/^#!/d' poetry/core/_vendor/jsonschema/benchmarks/issue232.py
sed -i '1!b;/^#!/d' poetry/core/_vendor/jsonschema/benchmarks/json_schema_test_suite.py

%build
# we debundle the deps after we use the bundled deps in previous step to parse the deps 🤯
#rm -r poetry/core/_vendor
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files poetry

%check
# don't use %%tox here because tox.ini runs "poetry install"
# TODO investigate failures in test_default_with_excluded_data, test_default_src_with_excluded_data
%{python3} -m pip install pytest-mock pytest-cov pep517 virtualenv
%pytest -k "not with_excluded_data"

%files -n python3-poetry-core -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Wed Sep 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.0.7-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Adding as build requirements for python-dns
- License verified

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.7-1
- Update to 1.0.7

* Fri Oct 01 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.6-1
- Update to 1.0.6

* Tue Sep 07 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Thu Aug 19 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.3-5
- Bundle vendored libraries again, to fix poetry install

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Lumír Balhar <lbalhar@redhat.com> - 1.0.3-3
- Allow newer packaging version
- Allow newer pyrsistent version

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.3-2
- Rebuilt for Python 3.10

* Thu Apr 15 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Thu Feb 25 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-1
- Initial package

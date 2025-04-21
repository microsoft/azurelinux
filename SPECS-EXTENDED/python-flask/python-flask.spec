Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global modname flask
%global srcname flask
Name:           python-%{modname}
Version:        3.1.0
Release:        1%{?dist}
Epoch:          1
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions
License:        BSD-3-Clause
URL:            http://flask.pocoo.org/
Source0:        %{pypi_source}
BuildArch:      noarch
 
%global _description \
Flask is called a “micro-framework” because the idea to keep the core\
simple but extensible. There is no database abstraction layer, no form\
validation or anything else where different libraries already exist\
that can handle that. However Flask knows the concept of extensions\
that can add this functionality into your application as if it was\
implemented in Flask itself. There are currently extensions for object\
relational mappers, form validation, upload handling, various open\
authentication technologies and more.
%description %{_description}
%package -n python3-%{modname}
Summary:        %{summary}
BuildRequires:      make
BuildRequires:      python3-devel
BuildRequires:      python3-pip
BuildRequires:      python3-wheel
BuildRequires:      python3-flit-core
BuildRequires:      python3-pytest
BuildRequires:      python3-werkzeug
BuildRequires:      python3-markupsafe
BuildRequires:      python3-click
BuildRequires:      python3-blinker
BuildRequires:      python3-jinja2
BuildRequires:      python3-itsdangerous
%description -n python3-%{modname} %{_description}
Python 3 version.
%if %{with doc}
%package doc
Summary:        Documentation for %{name}
%description doc
Documentation and examples for %{name}.
%endif
%pyproject_extras_subpkg -n python3-%{modname} async
%generate_buildrequires
# -t picks test.txt by default which contains too tight pins
%pyproject_buildrequires -x async requirements/tests.in %{?with_doc:requirements/docs.in}
%prep
%autosetup -n %{srcname}-%{version}
rm -rf examples/flaskr/
rm -rf examples/minitwit/
%build
%pyproject_wheel
%install
%pyproject_install
%pyproject_save_files %{modname}
mv %{buildroot}%{_bindir}/%{modname}{,-%{python3_version}}
ln -s %{modname}-%{python3_version} %{buildroot}%{_bindir}/%{modname}-3
ln -sf %{modname}-3 %{buildroot}%{_bindir}/%{modname}
%if %{with doc}
pushd docs
# PYTHONPATH to prevent "'Flask' must be installed to build the documentation."
make PYTHONPATH=%{buildroot}/%{python3_sitelib} SPHINXBUILD=sphinx-build-3 html
rm -v _build/html/.buildinfo
popd
%endif
%check
%pytest -Wdefault
%files -n python3-%{modname} -f %{pyproject_files}
%license LICENSE.txt
%doc CHANGES.rst README.md
%{_bindir}/%{modname}
%{_bindir}/%{modname}-3
%{_bindir}/%{modname}-%{python3_version}
%if %{with doc}
%files doc
%license LICENSE.txt
%doc docs/_build/html examples
%endif

%changelog
* Tue Apr 22 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 3.1.0-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
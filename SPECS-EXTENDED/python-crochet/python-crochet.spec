Vendor:        Microsoft Corporation
Distribution:  Azure Linux

%bcond_without check

%global pypi_name crochet

Name:           python-%{pypi_name}
Version:        2.1.1
Release:        1%{?dist}
Summary:        A library that makes it easier to use Twisted from blocking code
License:        MIT
URL:            https://github.com/itamarst/crochet
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

%if %{with check}
BuildRequires:  python3-twisted
BuildRequires:  python3-wrapt
%endif

%global _description %{expand:
Crochet is an MIT-licensed library that makes it easier to use Twisted from
regular blocking code. Some use cases include:

* Easily use Twisted from a blocking framework like Django or Flask.
* Write a library that provides a blocking API, but uses Twisted for its
  implementation.
* Port blocking code to Twisted more easily, by keeping a backwards
  compatibility layer.
* Allow normal Twisted programs that use threads to interact with Twisted more
  cleanly from their threaded parts.}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}
Requires:       python3-twisted
Requires:       python3-wrapt
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
sed -i -e 's/configparser.SafeConfigParser()/configparser.ConfigParser()/' \
       -e 's/parser.readfp(f)/parser.read_file(f)/' versioneer.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%if %{with check}
%check
%{py3_test_envvars} %{python3} -m unittest discover -v %{pypi_name}.tests
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst docs/news.rst

%changelog
* Thu Jun 11 2026 Adit Jha <aditjha@microsoft.com> - 2.1.1-1
- Initial Azure Linux import from Fedora rawhide (license: MIT). License verified.

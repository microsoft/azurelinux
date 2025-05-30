%global srcname paramiko

Summary:       Should assertions in Python in as clear and readable a way as possible
Name:          python-should_dsl
Version:       2.1.2
Release:       5%{?dist}
License:       MIT
URL:           https://github.com/nsi-iff/should-dsl
#Source0:      https://files.pythonhosted.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
Source0:       https://files.pythonhosted.org/packages/source/s/%{srcname}/%{name}-%{version}.tar.gz
BuildArch:     noarch
BuildRequires: coreutils
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
The goal of Should-DSL is to write should expectations in Python in as clear
and readable a way as possible, using "almost" natural language (limited -
sometimes - by the Python language constraints).

%package -n python3-should_dsl
Summary:	Should assertions in Python in as clear and readable a way as possible
%{?python_provide:%python_provide python3-should_dsl}

%description -n python3-should_dsl
The goal of Should-DSL is to write should expectations in Python in as clear
and readable a way as possible, using "almost" natural language (limited -
sometimes - by the Python language constraints).

%prep
%setup -q -n should_dsl-%{version}

# Remove bundled egg-info
rm -rf should_dsl.egg-info

%build
%py3_build

%install
%py3_install

%check
# run_all_examples.py references non-existent files and hence fails
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} run_examples.py README.rst

%files -n python3-should_dsl
%license LICENSE
%doc CONTRIBUTORS README.rst
%{python3_sitelib}/should_dsl/
%{python3_sitelib}/should_dsl-%{version}-py3.*.egg-info/

%changelog
* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 2.1.2-5
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.1.2-3
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Thu Dec 12 2019 Paul Howarth <paul@city-fan.org> - 2.1.2-1
- Initial RPM version
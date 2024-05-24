%{?python_enable_dependency_generator}
%global pypi_name pssh
%global sum PSSH provides parallel version of OpenSSH and related tools
%global desc PSSH provides parallel version of OpenSSH and related tools,\
including pssh, pscp, prsync, pnuke and pslurp.\
This project includes psshlib which can be used within custm applications.

Name:           python-%{pypi_name}
Version:        2.3.5
Release:        1%{?dist}
Summary:        %{sum}

License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/lilydjwg/%{pypi_name}
Source0:        https://github.com/lilydjwg/pssh/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

%description
%{desc}

%package -n     python3-%{pypi_name}
Summary:        %{sum}
BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}

%prep
%setup -q -n %{pypi_name}-%version
sed -i -e '1 d' psshlib/askpass_{client,server}.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

install -D -m 0755 %{buildroot}%{_bindir}/pssh-askpass \
    %{buildroot}%{_libexecdir}/pssh/pssh-askpass
rm -f %{buildroot}%{_bindir}/pssh-askpass
mv %{buildroot}%{_bindir}/pscp %{buildroot}%{_bindir}/pscp.pssh
install -d %{buildroot}%{_mandir}/man1
install -p -m 0644 man/man1/*.1  %{buildroot}%{_mandir}/man1
mv %{buildroot}%{_mandir}/man1/pscp.1 %{buildroot}%{_mandir}/man1/pscp.pssh.1

# No tests


%files
%license COPYING
%doc AUTHORS ChangeLog
%{_bindir}/pnuke
%{_bindir}/prsync
%{_bindir}/pscp.pssh
%{_bindir}/pslurp
%{_bindir}/pssh
%{_mandir}/man1/pnuke.1*
%{_mandir}/man1/prsync.1*
%{_mandir}/man1/pscp.pssh.1*
%{_mandir}/man1/pslurp.1*
%{_mandir}/man1/pssh.1*
%{_libexecdir}/pssh
%{python3_sitelib}/pssh-%{version}*
%{python3_sitelib}/psshlib

%changelog
* Mon May 20 2024 Alberto David Perez Guevara <aperezguevaar@microsoft.com> - 2.3.5-6
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified


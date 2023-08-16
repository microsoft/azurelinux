Name:           python-rpm-spec
Version:        0.14.1
Release:        1%{?dist}
Summary:        A Python library for parsing RPM spec files.

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/bkircher/python-rpm-spec
Source0:        https://github.com/bkircher/python-rpm-spec/archive/refs/tags/v0.14.1.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
%description
A Python library for parsing RPM spec files.

%package -n       python3-rpm-spec
Summary:          A Python library for parsing RPM spec files.

%description -n python3-rpm-spec
python-rpm-spec is a Python library for parsing RPM spec files.
tl;dr If you want to quickly parse a spec file on the command line you might want to give rpmspec --parse a try.
rpmspec --parse file.spec | awk '/Source/ {print $2}'
If you write Python, have no /usr/bin/rpm around, or want to do something slightly more complicated, try using this Python library.
RPMs are build from a package's sources along with a spec file. The spec file controls how the RPM is built. This library allows you to parse spec files and gives you simple access to various bits of information that is contained in the spec file.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/%{python3_sitelib}/
cp -r pyrpm %{buildroot}/%{python3_sitelib}/


%files -n python3-rpm-spec
%license LICENSE
%doc README.md
%{python3_sitelib}/*


%changelog
* Tue Aug 15 2023 Andy Zaugg <azaugg@linkedin.com> - 0.14.1-1
- Original version for CBL-Mariner
- License verified

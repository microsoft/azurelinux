# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-rpm-spec
Version:        0.14.1
Release:        1%{?dist}
Summary:        A Python library for parsing RPM spec files.

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/bkircher/python-rpm-spec
Source0:       https://github.com/bkircher/python-rpm-spec/archive/refs/tags/v0.14.1.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
%description
A Python library for parsing RPM spec files.

%package -n       python3-rpm-spec
Summary:          python-rpm-spec

%description -n python3-rpm-spec
python-rpm-spec is a Python library for parsing RPM spec files.
tl;dr If you want to quickly parse a spec file on the command line you might want to give rpmspec --parse a try.
rpmspec --parse file.spec | awk '/Source/ {print $2}'
If you write Python, have no /usr/bin/rpm around, or want to do something slightly more complicated, try using this Python library.
RPMs are build from a package's sources along with a spec file. The spec file controls how the RPM is built. This library allows you to parse spec files and gives you simple access to various bits of information that is contained in the spec file.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{python3_sitelib}/
cp -r pyrpm $RPM_BUILD_ROOT/%{python3_sitelib}/


%files -n python3-rpm-spec
%license LICENSE
%doc README.md
# For noarch packages: sitelib
%{python3_sitelib}/*


%changelog
* Tue Aug 15 2023 Andy Zaugg <azaugg@linkedin.com> - 0.14.1
- Initial creation of RPM

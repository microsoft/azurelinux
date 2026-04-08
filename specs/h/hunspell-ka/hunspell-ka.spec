# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: hunspell-ka
Summary: Georgian hunspell dictionaries
Version: 0.1
Release: 2%{?dist}
Source: ka_GE-%{version}.tar.gz
URL: https://github.com/gamag/ka_GE.spell/archive/refs/tags/0.1.tar.gz
License: MIT AND CC-BY-4.0
BuildArch: noarch

Requires: hunspell-filesystem

%description
Georgian hunspell dictionaries.

%prep
%setup -q -n ka_GE-%{version}

%build
chmod -x *

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hunspell
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/hunspell


%files
%doc README.md
%{_datadir}/hunspell/*

%changelog
* Tue Mar 4  2025 Temuri Doghonadze <temuri.doghonadze@gmail.com> - 0.1-2
- Changed versioning
- spec file cleanup

* Fri Feb 28 2025 Temuri Doghonadze <temuri.doghonadze@gmail.com> - 0.1-1
- initial version

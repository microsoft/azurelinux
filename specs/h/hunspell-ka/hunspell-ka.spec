# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%global dict_dirname hunspell
%else
%global dict_dirname myspell
%endif

Name: hunspell-ka
Summary: Georgian hunspell dictionaries
Version: 0.1
Release: 5%{?dist}
Source: https://github.com/gamag/ka_GE.spell/archive/refs/tags/%{version}.tar.gz#/ka_GE-%{version}.tar.gz
URL: https://github.com/gamag/ka_GE.spell/
License: MIT AND CC-BY-4.0
BuildArch: noarch

Requires: hunspell-filesystem
Supplements: (hunspell and langpacks-ka)

%description
Georgian hunspell dictionaries.

%prep
%setup -q -n ka_GE.spell-%{version}

%build
# nothing here to build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p dictionaries/*.dic dictionaries/*.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}


%files
%doc README.md LICENSE.mit
%{_datadir}/%{dict_dirname}/*

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Apr 24 2025 Parag Nemade <pnemade AT redhat DOT com> - 0.1-3
- Fix Source and URL tags
- Use correct upstream source tarball
- Add Supplements for langpacks-ka
- Enable this package to be used for EL < 9 version

* Tue Mar 4  2025 Temuri Doghonadze <temuri.doghonadze@gmail.com> - 0.1-2
- Changed versioning
- spec file cleanup

* Fri Feb 28 2025 Temuri Doghonadze <temuri.doghonadze@gmail.com> - 0.1-1
- initial version

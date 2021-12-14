Name:		tpm-quote-tools
Version:	1.0.4
Release:	6%{?dist}
Source0:	http://downloads.sourceforge.net/tpmquotetools/%{name}-%{version}.tar.gz

Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		http://sf.net/projects/tpmquotetools

Summary:	TPM-based attestation using the TPM quote operation (tools)
License:	BSD

BuildRequires:	gcc, trousers-devel

%description
TPM Quote Tools is a collection of programs that provide support
for TPM based attestation using the TPM quote operation.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/*
%{_mandir}/man8/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 21 2018 John D. Ramsdell <ramsdell@mitre.org> - 1.0.4-1
- fixed tpm_mkaik.c for the case in which the SRK password is in effect

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 John D. Ramsdell <ramsdell@mitre.org> - 1.0.3-1
- Added program descriptions to NAME sections in manual pages
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 John D. Ramsdell <ramsdell@gootoo.mitre.org> - 1.0.2-1
- Add support for ARM 64 bit CPU architecture (aarch64)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 John D. Ramsdell <ramsdell@mitre.org> - 1.0.1-1
- Tagged as 1.0.1
- Changed source to SourceForge development site.

* Thu Jul 14 2011 John D. Ramsdell <ramsdell@mitre.org> - 1.0-6
- Changed URL to SourceForge development site.
- Changed source to NEU site.
- Quoted % references in macros within changelog.
- README: Note tpm-tools only needed to take ownership of a TPM.

* Fri Jul 8 2011 John D. Ramsdell <ramsdell@mitre.org> - 1.0-5
- Fixed changelog

* Fri Jul 8 2011 John D. Ramsdell <ramsdell@mitre.org> - 1.0-4
- Removed use of %%makeinstall

* Thu Jun 2 2011 John D. Ramsdell <ramsdell@mitre.org> - 1.0-3
- Added %%changelog

* Wed Mar 9 2011 John D. Ramsdell <ramsdell@mitre.org> - 1.0-2
- Fixed spec to meet Fedora standards.

* Wed Mar 9 2011 John D. Ramsdell <ramsdell@mitre.org> - 1.0-1
- Initial package

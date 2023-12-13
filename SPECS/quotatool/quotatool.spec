Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           quotatool
Version:        1.6.2
Release:        24%{?dist}
Summary:        Command-line utility for filesystem quotas
License:        GPLv2
URL:            http://quotatool.ekenberg.se
Source0:        http://quotatool.ekenberg.se/%{name}-%{version}.tar.gz
# Upstream fixes
Patch0:         https://github.com/ekenberg/quotatool/commit/ad6944baaa73cf6230f9a2bef2399b31c2130547.patch
Patch1:         https://github.com/ekenberg/quotatool/commit/09695c944947d804cbe3b5c7e2c854953984413e.patch
Patch2:         https://github.com/ekenberg/quotatool/commit/ca68628de86d18fda67ebcc4191c2b37891ed36e.patch
Patch3:         https://github.com/ekenberg/quotatool/commit/58cdec3cdc6ae94864891a4e179ad68d4d136864.patch
Patch4:         https://github.com/ekenberg/quotatool/commit/af27842d1a6640d932407999ceec57f54a225a78.patch

BuildRequires:  make
BuildRequires:  gcc

%description
Quotatool is a utility to manipulate filesystem quotas from the commandline.
Most quota-utilities are interactive, requiring manual intervention from the
user. Quotatool on the other hand is not, making it suitable for use in
scripts and other non-interactive situations.

%prep
%setup -q
%patch0 -p1 -b .fix-compiler-warnings
%patch1 -p1 -b .fix-implicit-fallthrough
%patch2 -p1 -b .make-sure-make-clean-works-if-configure-has-not-run
%patch3 -p1 -b .improved-error-message
%patch4 -p1 -b .fix-compiler-warnings-again

%build
%configure
%make_build

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
%make_install INSTALL_PROGRAM="%{_bindir}/install -p"

%files
%doc AUTHORS ChangeLog COPYING README TODO
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*

%changelog
* Wed Dec 13 2023 Sindhu Karri <lakarri@microsoft.com> - 1.6.2-24
- Initial CBL-Mariner import from Fedora 39 (license: MIT)
- Source license verified to be GPLv2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 13 2022 Tom Callaway <spot@fedoraproject.org> - 1.6.2-21
- apply fixes from upstream

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-16
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Christopher Meng <rpm@cicku.me> - 1.6.2-1
- Initial Package.

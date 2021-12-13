Vendor:         Microsoft Corporation
Distribution:   Mariner
%global debug_package %{nil}

Name:		libkkc-data
Version:	0.2.7
Release:	18%{?dist}
Summary:	Language model data for libkkc

License:	GPLv3+
URL:		https://github.com/ueno/libkkc/
Source0:	https://github.com/ueno/libkkc/releases/download/v0.3.5/%{name}-%{version}.tar.xz
Patch0:		https://github.com/ueno/libkkc/commit/ba1c1bd3eb86d887fc3689c3142732658071b5f7.patch

BuildRequires:	gcc
BuildRequires:	python3-devel
BuildRequires:	python3-marisa

%description
The %{name} package contains the language model data that libkkc uses
at run time.


%prep
%setup -q
%patch0 -p4 -b .orig


%build
export PYTHON=%{__python3}
%configure --disable-static
make %{?_smp_mflags}


%install
%make_install INSTALL="install -p"


%files
%doc COPYING
%{_libdir}/libkkc


%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.2.7-18
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.2.7-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Jens Petersen <petersen@redhat.com> - 1:0.2.7-14
- build with python3 (upstream patch by fujiwara, #1675287)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:0.2.7-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Sep 20 2013 Daiki Ueno <dueno@redhat.com> - 1:0.2.7-2
- bump release to avoid NVR conflict

* Fri Sep 20 2013 Daiki Ueno <dueno@redhat.com> - 1:0.2.7-1
- add COPYING to %%doc
- disable debuginfo
- add Epoch to avoid conflict with the libkkc package

* Tue Sep 17 2013 Daiki Ueno <dueno@redhat.com> - 0.2.7-1
- initial packaging for Fedora, splitting from libkkc


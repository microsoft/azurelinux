# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-xapp
Version:        2.4.2
Release:        8%{?dist}
Summary:        Python bindings for xapps

# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2
URL:            https://github.com/linuxmint/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
%{summary}.


%package -n python3-xapp
Summary:       %{summary}

BuildRequires: meson
BuildRequires: python3-rpm-macros

Requires:      gtk3
Requires:      python3-gobject-base
Requires:      python3-psutil
Requires:      xapps

%description -n python3-xapp
%{summary}.


%prep
%autosetup -p1 -n python3-xapp-%{version}


%build
%meson
%meson_build


%install
%meson_install


%files -n python3-xapp
%license COPYING debian/copyright
%doc PKG-INFO debian/changelog
%{python3_sitelib}/xapp/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.4.2-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.4.2-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.4.2-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Leigh Scott <leigh123linux@gmail.com> - 2.4.2-2
- Rebuilt for Python 3.13

* Tue Jun 04 2024 Leigh Scott <leigh123linux@gmail.com> - 2.4.2-1
- Update to 2.4.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Leigh Scott <leigh123linux@gmail.com> - 2.4.1-2
- Rebuilt for Python 3.12

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 2.4.1-1
- Update to 2.4.1 release

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 18 2022 Leigh Scott <leigh123linux@gmail.com> - 2.4.0-1
- Update to 2.4.0 release

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Leigh Scott <leigh123linux@gmail.com> - 2.2.2-3
- Add the requires needed for the imports

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.2.2-2
- Rebuilt for Python 3.11

* Sat Jun 11 2022 Leigh Scott <leigh123linux@gmail.com> - 2.2.2-1
- Update to 2.2.2 release

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.1-1
- Update to 2.2.1 release

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.0-2
- Rebuilt for Python 3.10

* Fri May 28 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.0-1
- Update to 2.2.0 release

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.2-1
- Update to 2.0.2 release

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.1-1
- Update to 2.0.1 release

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.8.1-1
- Update to 1.8.1 release

* Sat Nov 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.8.0-1
- Update to 1.8.0 release

* Sun Sep 15 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-4
- Fix summary

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Leigh Scott <leigh123linux@gmail.com> - 1.6.0-1
- Update to 1.6.0 release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Update to 1.4.0 release

* Sun Oct 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-4
- Drop EPEL/RHEL support
- Drop python2 support

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-2
- Rebuilt for Python 3.7

* Mon Apr 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-1
- Update to 1.2.0 release

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.1-7
- Use unified Provides for EPEL7

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.1-6
- Use unified macros for Python 3

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.1-5
- Build a Python3 compat pkg on RHEL7

* Tue Aug 29 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.1-4
- Fix for EPEL

* Tue Aug 29 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.1-3
- Conditionalize Python3 for EPEL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 release (rhbz#1460408)

* Mon May 01 2017 Leigh Scott <leigh123linux@gmail.com> - 1.0.0-1
- Initial rpm-release (rhbz#1448559)

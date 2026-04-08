# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           sensible-utils
Version:        0.0.25
Release:        2%{?dist}
Summary:        Utilities for sensible alternative selection

BuildArch:      noarch
License:        GPL-2.0-or-later
URL:            https://packages.debian.org/unstable/admin/%{name}
Source0:        http://ftp.de.debian.org/debian/pool/main/s/%{name}/%{name}_%{version}.tar.xz

BuildRequires:  automake autoconf
BuildRequires:  make
BuildRequires:  po4a

# See Patch0
Requires:       /usr/bin/gettext
Requires:       /usr/bin/realpath


%description
This package provides a number of small utilities which are used by programs to
sensibly select and spawn an appropriate browser, editor, or pager.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
# Needed for Patch0
autoreconf -ifv

%configure
%make_build


%install
%make_install


%files
%license debian/copyright
%doc debian/changelog
%{_bindir}/sensible-*
%{_bindir}/select-editor
%{_mandir}/man1/*.1*
%{_mandir}/*/man1/*.1*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Apr 23 2025 Sandro Mani <manisandro@gmail.com> - 0.0.25-1
- Update to 0.0.25

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 25 2024 Sandro Mani <manisandro@gmail.com> - 0.0.24-1
- Update to 0.0.24

* Tue Jun 18 2024 Sandro Mani <manisandro@gmail.com> - 0.0.23-1
- Update to 0.0.23

* Tue Feb 06 2024 Sandro Mani <manisandro@gmail.com> - 0.0.22-1
- Update to 0.0.22

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Sandro Mani <manisandro@gmail.com> - 0.0.21-1
- Update to 0.0.21

* Sun Jun 18 2023 Sandro Mani <manisandro@gmail.com> - 0.0.20-1
- Update to 0.0.20

* Tue May 09 2023 Sandro Mani <manisandro@gmail.com> - 0.0.19-1
- Update to 0.0.19

* Sun Mar 19 2023 Sandro Mani <manisandro@gmail.com> - 0.0.18-1
- Update to 0.0.18

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 30 2022 Sandro Mani <manisandro@gmail.com> - 0.0.17-4
- Require gettext-runtime

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 30 2021 Sandro Mani <manisandro@gmail.com> - 0.0.17-1
- Update to 0.0.17

* Fri Aug 27 2021 Sandro Mani <manisandro@gmail.com> - 0.0.16-1
- Update to 0.0.16

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Sandro Mani <manisandro@gmail.com> - 0.0.14-1
- Update to 0.0.14

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 13 2018 Sandro Mani <manisandro@gmail.com> - 0.0.12-1
- Update to 0.0.12

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 13 2017 Sandro Mani <manisandro@gmail.com> - 0.0.11-1
- Update to 0.0.11

* Tue Oct 31 2017 Sandro Mani <manisandro@gmail.com> - 0.0.10-1
- Update to 0.0.10

* Wed Sep 06 2017 Sandro Mani <manisandro@gmail.com> - 0.0.9-8
- Use --config instead of --list in update-alternatives --config editor

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Sandro Mani <manisandro@gmail.com> - 0.0.9-6
- Silence stderr when looking for $EDITOR, $VISUAL and $SELECTED_EDITOR (#1467077)
- Modernize spec

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Sandro Mani <manisandro@gmail.com> - 0.0.9-1
- Initial package

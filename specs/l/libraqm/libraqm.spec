# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:				libraqm
Version:			0.10.1
Release: 4%{?dist}
License:			MIT
Summary:			Complex Textlayout Library
Summary(ar):		مكتبة رقم للنّصوص المركّبة
URL:				https://github.com/HOST-Oman/libraqm
Source:				%{url}/releases/download/v%{version}/raqm-%{version}.tar.xz

BuildRequires:		meson
BuildRequires:		gcc
BuildRequires:		freetype-devel
BuildRequires:		harfbuzz-devel
BuildRequires:		fribidi-devel
BuildRequires:		gtk-doc

%package docs
Summary:			Libraqm Documentation
Summary(ar):		وثائق مكتبة رقم
BuildArch:			noarch

%package devel
Summary:			Complex Textlayout Library
Summary(ar):		مكتبة رقم للنّصوص المركّبة
Requires:			libraqm%{?_isa} = %{version}-%{release}

%description
Library that encapsulates the logic for complex
text layout and provides a convenient API.

%description -l ar
مكتبة تستخدم لتأطير النًصوص المركّبة، مقدمة
مدخلًا برمجيًا مريحًا.


%description devel
Library that encapsulates the logic for complex
text layout and provides a convenient API.

%description -l ar devel
مكتبة تستخدم لتأطير النًصوص المركّبة، مقدمة
مدخلًا برمجيًا مريحًا.

%description docs
This package contains documentation files for raqm.

%description -l ar docs
وثائق مكتبة رقم.

%prep
%autosetup -p1 -n raqm-%{version}

%build
%meson -Ddocs=true
%meson_build

%check
export LC_ALL=C.utf8
%meson_test

%install
%meson_install
rm -f %{buildroot}%{_libdir}/*.{la,a}

%files
%license COPYING
%{_libdir}/libraqm.so.*

%files devel
%license COPYING
%{_includedir}/raqm.h
%{_includedir}/raqm-version.h
%{_libdir}/libraqm.so
%{_libdir}/pkgconfig/raqm.pc

%files docs
%license COPYING
%doc AUTHORS NEWS README.md
%{_datadir}/gtk-doc/html/raqm

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 22 2024 Carl George <carlwgeorge@fedoraproject.org> - 0.10.1-1
- Update to version 0.10.1 rhbz#1900481

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Peter Fordham <peter.fordham@gmail.com> - 0.8.0-3
- Patch in fix from upstream for C99 compatibilty issue with strdup in test.
  https://github.com/HOST-Oman/libraqm/commit/3f50e35d239059823162cbfba3c7adfe8e5f1907

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 03 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.7.2-1
- Update to 0.7.2
- Minor cleanups to the spec

* Sat Oct 02 2021 Kalev Lember <klember@redhat.com> - 0.7.0-9
- Backport upstream patch to fix failing self tests (#1987659)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Mosaab Alzoubi <moceap@hotmail.com> - 0.7.0-4
- First build on EPEL8
- Use one branch to build on Fedora and EPEL
- Use python3 as BR except EPEL7
- Use LC_ALL=en_US.UTF-8 in EPEL7

* Sun Sep 8 2019 Mosaab Alzoubi <moceap@hotmail.com> - 0.7.0-1
- Updated to 0.7.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.0-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 14 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.5.0-1
- Update to latest version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 1 2016 Mosaab Alzoubi <moceap@hotmail.com> - 0.1.1-1
- Updated to 0.1.1

* Mon Apr 25 2016 Mosaab Alzoubi <moceap@hotmail.com> - 0.1.0-3
- Use lib prefix in %%name
- Depends on same version -devel

* Sun Apr 24 2016 Mosaab Alzoubi <moceap@hotmail.com> - 0.1.0-2
- General revision

* Sat Apr 23 2016 Mosaab Alzoubi <moceap@hotmail.com> - 0.1.0-1
- Initial build

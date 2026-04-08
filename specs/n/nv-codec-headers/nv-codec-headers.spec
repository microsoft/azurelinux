# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           nv-codec-headers
Version:        13.0.19.0
Release:        2%{?dist}
Summary:        FFmpeg version of Nvidia Codec SDK headers
License:        MIT
URL:            https://github.com/FFmpeg/nv-codec-headers
Source0:        %{url}/archive/n%{version}/%{name}-n%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make

%description
FFmpeg version of headers required to interface with Nvidias codec APIs.


%prep
%autosetup -n %{name}-n%{version}
sed -i -e 's@/include@/include/ffnvcodec@g' ffnvcodec.pc.in

# Extract license
sed -n '4,25p' include/ffnvcodec/nvEncodeAPI.h > LICENSE
sed -i '1,22s/^.\{,3\}//' LICENSE

%build
%make_build PREFIX=%{_prefix} LIBDIR=/share


%install
%make_install PREFIX=%{_prefix} LIBDIR=/share


%files
%doc README
%license LICENSE
%{_includedir}/ffnvcodec/
%{_datadir}/pkgconfig/ffnvcodec.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Mar 18 2025 Leigh Scott <leigh123linux@gmail.com> - 13.0.19.0-1
- Update to 13.0.19.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.2.72.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Nicolas Chauvet <kwizart@gmail.com> - 12.2.72.0-1
- Update to 12.2.72.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 19 2023 Leigh Scott <leigh123linux@gmail.com> - 12.1.14.0-1
- Update to 12.1.14.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 12.0.16.0-1
- Update to 12.0.16.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Leigh Scott <leigh123linux@gmail.com> - 11.1.5.2-1
- Update to 11.1.5.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Leigh Scott <leigh123linux@gmail.com> - 11.1.5.1-1
- Update to 11.1.5.1

* Wed Dec 08 2021 Leigh Scott <leigh123linux@gmail.com> - 11.1.5.0-1
- Update to 11.1.5.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 21 2021 Leigh Scott <leigh123linux@gmail.com> - 11.0.10.1-1
- Update to 11.0.10.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 15 2020 Leigh Scott <leigh123linux@gmail.com> - 11.0.10.0-1
- Update to 11.0.10.0

* Tue Oct  6 2020 Leigh Scott <leigh123linux@gmail.com> - 10.0.26.1-1
- Update to 10.0.26.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 02 2020 Leigh Scott <leigh123linux@gmail.com> - 10.0.26.0-1
- Update to 10.0.26.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Leigh Scott <leigh123linux@gmail.com> - 9.1.23.1-1
- Update to 9.1.23.1

* Tue Sep 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 9.1.23.0-1
- Update to 9.1.23.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 9.0.18.1-2
- Use correct path for pkg-config file

* Sat May 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 9.0.18.1-1
- Update to 9.0.18.1

* Fri Mar 01 2019 Leigh Scott <leigh123linux@googlemail.com> - 9.0.18.0-1
- Update to 9.0.18.0

* Sun Feb 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 8.2.15.7-1
- Update to 8.2.15.7

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.15.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 8.2.15.6-1
- Update to 8.2.15.6

* Tue Nov 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 8.2.15.5-1
- Update to 8.2.15.5

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Leigh Scott <leigh123linux@googlemail.com> - 8.1.24.2-1
- Update to 8.1.24.2

* Sun Apr 15 2018 Leigh Scott <leigh123linux@googlemail.com> - 8.1.24.1-1
- Update to 8.1.24.1

* Tue Feb 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 8.0.14.1-1
- First build

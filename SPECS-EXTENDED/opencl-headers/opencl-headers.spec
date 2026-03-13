Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global commit0 4ea6df132107e3b4b9407f903204b5522fdffcd6
%global date 20241023
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global cl_hpp_ver 2024.10.24

Name:           opencl-headers
Version:        3.0
Release:        32%{?dist}
Summary:        OpenCL (Open Computing Language) header files

License:        Apache-2.0
URL:            https://www.khronos.org/registry/cl/

Source0:        https://github.com/KhronosGroup/OpenCL-Headers/archive/%{commit0}/OpenCL-Headers-%{shortcommit0}.tar.gz#/OpenCL-Headers-%{shortcommit0}.tar.gz
Source1:        https://github.com/KhronosGroup/OpenCL-CLHPP/archive/v%{cl_hpp_ver}/OpenCL-CLHPP-v%{cl_hpp_ver}.tar.gz

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n OpenCL-Headers-%{commit0}

tar -xf %{SOURCE1}
cp -p OpenCL-CLHPP-%{cl_hpp_ver}/include/CL/{cl2,opencl}.hpp .

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_includedir}/CL/
install -p -m 0644 *hpp CL/* -t %{buildroot}%{_includedir}/CL/
# We're not interested in Direct3D things
rm -vf %{buildroot}%{_includedir}/CL/cl_{dx9,d3d}*
# Install pkgconfig files
mkdir -p %{buildroot}%{_datadir}/pkgconfig
sed -e 's|@CMAKE_INSTALL_PREFIX@|%{_prefix}|' -e 's|@OPENCL_INCLUDEDIR_PC@|%{_includedir}|' OpenCL-Headers.pc.in > %{buildroot}%{_datadir}/pkgconfig/OpenCL-Headers.pc
sed -e 's|@CMAKE_INSTALL_PREFIX@|%{_prefix}|' -e 's|@OPENCLHPP_INCLUDEDIR_PC@|%{_includedir}|' OpenCL-CLHPP-%{cl_hpp_ver}/OpenCL-CLHPP.pc.in > %{buildroot}%{_datadir}/pkgconfig/OpenCL-CLHPP.pc

%files
%dir %{_includedir}/CL
%{_includedir}/CL/cl2.hpp
%{_includedir}/CL/cl_egl.h
%{_includedir}/CL/cl_ext.h
%{_includedir}/CL/cl_ext_intel.h
%{_includedir}/CL/cl_function_types.h
%{_includedir}/CL/cl_gl_ext.h
%{_includedir}/CL/cl_gl.h
%{_includedir}/CL/cl.h
%{_includedir}/CL/cl_half.h
%{_includedir}/CL/cl_icd.h
%{_includedir}/CL/cl_layer.h
%{_includedir}/CL/cl_platform.h
%{_includedir}/CL/cl_va_api_media_sharing_intel.h
%{_includedir}/CL/cl_version.h
%{_includedir}/CL/opencl.h
%{_includedir}/CL/opencl.hpp
%{_datadir}/pkgconfig/OpenCL-Headers.pc
%{_datadir}/pkgconfig/OpenCL-CLHPP.pc

%changelog
* Tue Jan 07 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 3.0-32
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Tue Dec 03 2024 František Zatloukal <fzatlouk@redhat.com> - 3.0-31.20241023git4ea6df1
- Resync to 20241023

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-30.20240412git8275634
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 František Zatloukal <fzatlouk@redhat.com> - 3.0-29.20240412git8275634
- Fixup autorelease extra versioning

* Tue Jul 02 2024 František Zatloukal <fzatlouk@redhat.com> - 3.0-28
- Resync to 20240412

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-21.20231212git2368105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-20.20231212git2368105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Frantisek Zatloukal <fzatlouk@redhat.com> - 3.0-19.20231212git2368105
- Resync to 20231212

* Thu Oct 05 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 3.0-18.20231003git9ce9a72
- Resync to 20231003

* Fri Sep 15 2023 Dave Airlie <airlied@redhat.com> - 3.0-17.20230509gite049b16
- SPDX license update

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-16.20230509gite049b16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 05 2023 Orion Poplawski <orion@nwra.com> - 3.0-15.20230509gite049b16
- Resync to 20230509
- Skip pkgconfig files (bz#2212323)

* Sat Mar 18 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 3.0-14.20230201git4c82e9c
- Resync to 20230201
- Drop cl.hpp (CL 1.4 is provided by opencl.h according to upstream)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-13.20220510gitdef8be9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-12.20220510gitdef8be9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 3.0-11.20220510gitdef8be9
- Resync to 20220510

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-10.20211007git1aa1139
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 13 2021 Dave Airlie <airlied@redhat.com> - 3.0-9.20211007git1aa1139
- update for new extensions

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-8.20210216gitd1b936b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 01 2021 Nicolas Chauvet <kwizart@gmail.com> - 3.0-7.20210216gitd1b936b
- Fix missing c++ header - should now use <CL/opencl.hpp>

* Tue Apr 27 2021 Nicolas Chauvet <kwizart@gmail.com> - 3.0-6.20210216gitd1b936b
- Resync to 20210216

* Mon Apr 26 2021 Nicolas Chauvet <kwizart@gmail.com> - 3.0-5.20210426git1d3dc4e
- Update latest headers

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 07 2020 Dave Airlie <airlied@redhat.com> - 3.0-2git20201007gitd65bcc5
- Update latest headers

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Karol Herbst <kherbst@redhat.com> - 3.0-1.20200512gitd082d42
- Update to latest upstream, pick up new extensions for OpenCL-CTS build fix
- Rework CLHPP handling as file is not downloadable anymore
- Bump CLHPP version to 2.0.12

* Wed May 20 2020 Karol Herbst <kherbst@redhat.com> - 3.0-0.20200512git5cc337c
- Update to latest upstream, pick up new extensions for OpenCL-CTS build fix
- Bump CLHPP version to 2.0.11

* Fri Feb 28 2020 Karol Herbst <kherbst@redhat.com> - 2.2-7.20200218git96f5bde
- Update to latest upstream, pick up new extensions for OpenCL-CTS build fix

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-6.20190205git49f07d3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-5.20190205git49f07d3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 05 2019 Dave Airlie <airlied@redhat.com> - 2.2-4.20190205git49f07d3
- Update to latest upstream, pick up the ppc fix

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3.20180306gite986688
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2.20180306gite986688
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Simone Caronni <negativo17@gmail.com> - 2.2-1.20180306gite986688
- Update to 2.2.
- Use packaging guidelines for snapshots.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 31 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.1-1
- Update to 2.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 17 2016 Dave Airlie <airlied@redhat.com> - 1.2-8
- add cl_egl.h

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 1.2-5
- Pull patch application into pre

* Fri Apr 25 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 1.2-4
- Add patch for cl.hpp to be usable on arm rhbz#1027199

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Dave Airlie <airlied@redhat.com> 1.2-2
- fix missing dir and remove defattr.

* Wed Feb 27 2013 Dave Airlie <airlied@redhat.com> 1.2-1
- OpenCL header files from Khronos for OpenCL 1.2

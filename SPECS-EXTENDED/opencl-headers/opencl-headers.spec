Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global commit0 49f07d313344ddb22701847ea5c18cb7db03b0d7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global cl_hpp_ver 2.0.10

Name:           opencl-headers
Version:        2.2
Release:        7%{?dist}
Summary:        OpenCL (Open Computing Language) header files

License:        MIT
URL:            https://www.khronos.org/registry/cl/

Source0:        https://github.com/KhronosGroup/OpenCL-Headers/archive/%{commit0}/OpenCL-Headers-%{commit0}.tar.gz#/OpenCL-Headers-%{shortcommit0}.tar.gz
Source1:        https://github.com/KhronosGroup/OpenCL-CLHPP/releases/download/v%{cl_hpp_ver}/cl2.hpp
# OCL 1.2 compatibility
Source2:        https://www.khronos.org/registry/cl/api/2.1/cl.hpp

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n OpenCL-Headers-%{commit0}

cp -p %{SOURCE1} %{SOURCE2} .

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_includedir}/CL/
install -p -m 0644 *hpp CL/* -t %{buildroot}%{_includedir}/CL/
# We're not interested in Direct3D things
rm -vf %{buildroot}%{_includedir}/CL/cl_{dx9,d3d}*

%files
%license LICENSE
%dir %{_includedir}/CL
%{_includedir}/CL/opencl.h
%{_includedir}/CL/cl_platform.h
%{_includedir}/CL/cl.h
%{_includedir}/CL/cl_ext.h
%{_includedir}/CL/cl_egl.h
%{_includedir}/CL/cl_gl.h
%{_includedir}/CL/cl_gl_ext.h
%{_includedir}/CL/cl_ext_intel.h
%{_includedir}/CL/cl_va_api_media_sharing_intel.h
%{_includedir}/CL/cl_version.h
%{_includedir}/CL/cl2.hpp
%{_includedir}/CL/cl.hpp

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

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


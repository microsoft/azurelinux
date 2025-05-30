%global sdkver 1.3.275.0


Name:           spirv-headers
Version:        1.5.5
Release:        2%{?dist}
Summary:        Header files from the SPIR-V registry

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/KhronosGroup/SPIRV-Headers/
Source0:        %{url}/archive/refs/tags/vulkan-sdk-%{sdkver}.tar.gz#/%{name}-sdk-%{sdkver}.tar.gz

BuildArch:      noarch

BuildRequires:  cmake3
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++

%description
%{summary}

This includes:

* Header files for various languages.
* JSON files describing the grammar for the SPIR-V core instruction
  set, and for the GLSL.std.450 extended instruction set.
* The XML registry file

%package        devel
Summary:        Development files for %{name}

%description    devel
%{summary}

This includes:

* Header files for various languages.
* JSON files describing the grammar for the SPIR-V core instruction
  set, and for the GLSL.std.450 extended instruction set.
* The XML registry fil

%prep
%autosetup -n SPIRV-Headers-vulkan-sdk-%{sdkver}
chmod a-x include/spirv/1.2/spirv.py


%build
%cmake3 -DCMAKE_INSTALL_LIBDIR=%{_lib} -GNinja
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE
%doc README.md
%{_includedir}/spirv/
%{_datadir}/cmake/SPIRV-Headers/*.cmake
%{_datadir}/pkgconfig/SPIRV-Headers.pc

%changelog
* Thu Feb 29 2024 Vince Perri <viperri@microsoft.com> - 1.5.5-2
- Promote and upgrade to SDK 1.3.275 (commit 1c6bb2743599e6eb6f37b2969acc0aef812e32e3) based on Fedora 40.
- License verified.

* Mon Mar 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.5-1
- Updating to version 1.5.5 + 1.6.1 pre-release commits using Fedora 36 spec (license: MIT) for guidance.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.1-4
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.5.1-3
- Update to latest spirv headers

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.5.1-2
- Update to latest spirv headers

* Tue Nov 12 2019 Dave Airlie <airlied@redhat.com> - 1.5.1-1
- Latest git snapshot building vulkan

* Thu Aug 01 2019 Dave Airlie <airlied@redhat.com> - 1.4.2-0.1
- Latest git snapshot for building vulkan.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 03:08:22 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 1.4.1-1
- Release 1.4.1

* Thu Mar 07 2019 Dave Airlie <airlied@redhat.com> - 1.2-0.12.20190307.git03a0815
- Update to latest version

* Mon Feb 04 2019 Dave Airlie <airlied@redhat.com> - 1.2-0.11.20190125.git8bea0a2
- Update to latest version

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.10.20180703.gitff684ff
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.9.20180703.gitff684ff
- Revert last commit

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.8.20180919.gitd5b2e12
- Update for SPIRV-Tools-2018.5

* Mon Jul 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.7.20180703.gitff684ff
- Update for SPIRV-Tools-2018.4

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.6.20180405.git12f8de9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.5.20180405.git12f8de9
- Update for vulkan 1.0.73.0

* Fri Feb 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.4.20180201.gitce30920
- Update for vulkan 1.0.68.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.3.20171015.git0610978
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.2.20171015.git0610978
- fix rpmlint error

* Thu Jul 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.1.20171015.git0610978
- First build


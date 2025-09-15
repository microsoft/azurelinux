Summary:        Vulkan Header files and API registry
Name:           vulkan-headers
Version:        1.3.275.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/KhronosGroup/Vulkan-Headers
#WARNING: the source file downloads as 'vulkan-sdk-%%{version}.tar.gz' and MUST be re-named to match the 'Source0' tag.
#Source0:       %%{url}/archive/vulkan-sdk-%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc

%description
Vulkan Header files and API registry

%prep
%autosetup -n Vulkan-Headers-vulkan-sdk-%{version}


%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%make_build


%install
%make_install


%files
%license LICENSE.md
%doc README.md
%{_includedir}/vulkan/
%{_includedir}/vk_video/
%dir %{_datadir}/vulkan/
%dir %{_datadir}/cmake/VulkanHeaders/
%{_datadir}/vulkan/registry/
%{_datadir}/cmake/VulkanHeaders/*.cmake

%changelog
* Fri Mar 29 2024 Nan Liu <liunan@microsoft.com> - 1.3.275.0-1
- Upgrade to 1.3.275.0.

* Mon Mar 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.148.0-3
- Changed source tarball name.

* Fri Jan 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.148.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Replaced 'cmake_(build|install)' macros with 'make_(build|install)'.
- Replaced BR 'cmake3' with 'cmake'.

* Tue Aug 04 2020 Dave Airlie <airlied@redhat.com> - 1.2.148.0-1
- Update to 1.2.148.0 headers

* Thu Jul 30 2020 Adam Jackson <ajax@redhat.com> - 1.2.135.0-2
- Explicitly pass -C %%{_vpath_builddir} to fix F33's cmake

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.135.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.2.135.0-1
- Update to 1.2.135.0 headers

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.2.131.1-1
- Update to 1.2.131.1 headers

* Tue Nov 12 2019 Dave Airlie <airlied@redhat.com> - 1.1.126.0-1
- Update to 1.1.126.0 headers

* Mon Jul 29 2019 Dave Airlie <airlied@redhat.com> - 1.1.114.0-2
- Update to 1.1.114.0 headers

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.108.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Dave Airlie <airlied@redhat.com> - 1.1.108.0-1
- Update to 1.1.108.0 headers

* Thu Apr 18 2019 Dave Airlie <airlied@redhat.com> - 1.1.106.0-1
- Update to 1.1.106.0 headers

* Wed Mar 06 2019 Dave Airlie <airlied@redhat.com> - 1.1.101.0-1
- Update to 1.1.101.0 headers

* Wed Feb 13 2019 Dave Airlie <airlied@redhat.com> - 1.1.97.0-1
- Update to 1.1.97.0 headers

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Dave Airlie <airlied@redhat.com> - 1.1.92.0-1
- Update to 1.1.92.0

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.85.0-1
- Update to 1.1.85.0

* Tue Aug 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.82.0-1
- Update to 1.1.82.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.77.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-1
- Initial package

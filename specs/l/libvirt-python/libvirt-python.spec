# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*- rpm-spec -*-

# This spec file assumes you are building on a Fedora or RHEL version
# that's still supported by the vendor. It may work on other distros
# or versions, but no effort will be made to ensure that going forward
%define min_rhel 8
%define min_fedora 33

%if (0%{?fedora} && 0%{?fedora} >= %{min_fedora}) || (0%{?rhel} && 0%{?rhel} >= %{min_rhel})
    %define supported_platform 1
%else
    %define supported_platform 0
%endif

Summary: The libvirt virtualization API python3 binding
Name: libvirt-python
Version: 11.6.0
Release: 4%{?dist}
Source0: https://libvirt.org/sources/python/%{name}-%{version}.tar.gz
Url: https://libvirt.org
License: LGPL-2.1-or-later
BuildRequires: libvirt-devel == %{version}
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-lxml
BuildRequires: python3-setuptools
BuildRequires: gcc

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python3_sitearch}/.*\.so}
%{?filter_setup}

%description
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%package -n python3-libvirt
Summary: The libvirt virtualization API python3 binding
Url: http://libvirt.org
License: LGPLv2+
%{?python_provide:%python_provide python3-libvirt}
Provides: libvirt-python3 = %{version}-%{release}
Obsoletes: libvirt-python3 <= 3.6.0-1%{?dist}

%description -n python3-libvirt
The python3-libvirt package contains a module that permits applications
written in the Python 3.x programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%prep
%setup -q

# Unset execute bit for example scripts; it can introduce spurious
# RPM dependencies, like /usr/bin/python3
# for the -python3 package
find examples -type f -exec chmod 0644 \{\} \;

%build
%if ! %{supported_platform}
echo "This RPM requires either Fedora >= %{min_fedora} or RHEL >= %{min_rhel}"
exit 1
%endif

%py3_build

%install
%py3_install

%check
%pytest

%files -n python3-libvirt
%doc ChangeLog AUTHORS README COPYING examples/
%{python3_sitearch}/libvirt.py*
%{python3_sitearch}/libvirtaio.py*
%{python3_sitearch}/libvirt_qemu.py*
%{python3_sitearch}/libvirt_lxc.py*
%{python3_sitearch}/__pycache__/libvirt.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirt_qemu.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirt_lxc.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirtaio.cpython-*.py*
%{python3_sitearch}/libvirtmod*
%{python3_sitearch}/*egg-info


%changelog
* Mon Sep 29 2025 Daniel P. Berrangé <berrange@redhat.com> - 11.6.0-3
- Rebuilt for Python 3.14.0rc3 bytecode (rhbz #2396717)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 11.6.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 05 2025 Cole Robinson <crobinso@redhat.com> - 11.6.0-1
- Update to version 11.6.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Cole Robinson <crobinso@redhat.com> - 11.5.0-1
- Update to version 11.5.0

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 11.4.0-2
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Cole Robinson <crobinso@redhat.com> - 11.4.0-1
- Update to version 11.4.0

* Wed May 07 2025 Cole Robinson <crobinso@redhat.com> - 11.3.0-1
- Update to version 11.3.0

* Thu Apr 03 2025 Cole Robinson <crobinso@redhat.com> - 11.2.0-1
- Update to version 11.2.0

* Mon Mar 03 2025 Cole Robinson <crobinso@redhat.com> - 11.1.0-1
- Update to version 11.1.0

* Fri Jan 17 2025 Cole Robinson <crobinso@redhat.com> - 11.0.0-1
- Update to version 11.0.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 03 2024 Cole Robinson <crobinso@redhat.com> - 10.10.0-1
- Update to version 10.10.0

* Mon Nov 04 2024 Cole Robinson <crobinso@redhat.com> - 10.9.0-1
- Update to version 10.9.0

* Wed Oct 02 2024 Cole Robinson <crobinso@redhat.com> - 10.8.0-1
- Update to version 10.8.0

* Mon Sep 02 2024 Cole Robinson <crobinso@redhat.com> - 10.7.0-1
- Update to version 10.7.0

* Tue Aug 06 2024 Cole Robinson <crobinso@redhat.com> - 10.6.0-1
- Update to version 10.6.0

* Fri Jul 26 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 10.5.0-1
- Update to version 10.5.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Miro Hrončok <mhroncok@redhat.com> - 10.4.0-1
- Update to version 10.4.0

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 10.2.0-2
- Rebuilt for Python 3.13

* Sat Apr 06 2024 Cole Robinson <crobinso@redhat.com> - 10.2.0-1
- Update to version 10.2.0

* Fri Mar 01 2024 Cole Robinson <crobinso@redhat.com> - 10.1.0-1
- Update to version 10.1.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Cole Robinson <crobinso@redhat.com> - 10.0.0-1
- Update to version 10.0.0

* Sun Dec 03 2023 Cole Robinson <crobinso@redhat.com> - 9.10.0-1
- Update to version 9.10.0

* Wed Nov 01 2023 Cole Robinson <crobinso@redhat.com> - 9.9.0-1
- Update to version 9.9.0

* Fri Oct 06 2023 Cole Robinson <crobinso@redhat.com> - 9.8.0-1
- Update to version 9.8.0

* Fri Sep  1 2023 Daniel P. Berrangé <berrange@redhat.com> - 9.7.0-1
- Update to version 9.7.0

* Tue Aug 01 2023 Cole Robinson <crobinso@redhat.com> - 9.6.0-1
- Update to version 9.6.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Cole Robinson <crobinso@redhat.com> - 9.5.0-1
- Update to version 9.5.0

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 9.4.0-2
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Cole Robinson <crobinso@redhat.com> - 9.4.0-1
- Update to version 9.4.0

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 9.3.0-2
- Rebuilt for Python 3.12

* Tue May 02 2023 Cole Robinson <crobinso@redhat.com> - 9.3.0-1
- Update to version 9.3.0

* Wed Apr 05 2023 Cole Robinson <crobinso@redhat.com> - 9.2.0-1
- Update to version 9.2.0

* Sun Mar 05 2023 Cole Robinson <crobinso@redhat.com> - 9.1.0-1
- Update to version 9.1.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Cole Robinson <crobinso@redhat.com> - 9.0.0-1
- Update to version 9.0.0

* Sat Dec 03 2022 Cole Robinson <crobinso@redhat.com> - 8.10.0-1
- Update to version 8.10.0

* Sat Nov 05 2022 Cole Robinson <crobinso@redhat.com> - 8.9.0-1
- Update to version 8.9.0

* Tue Oct 04 2022 Cole Robinson <crobinso@redhat.com> - 8.8.0-1
- Update to version 8.8.0

* Tue Sep 06 2022 Cole Robinson <crobinso@redhat.com> - 8.7.0-1
- Update to version 8.7.0

* Tue Aug 02 2022 Cole Robinson <crobinso@redhat.com> - 8.6.0-1
- Update to version 8.6.0

* Thu Jul 21 2022 Cole Robinson <crobinso@redhat.com> - 8.5.0-1
- Update to version 8.5.0

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 8.4.0-2
- Rebuilt for Python 3.11

* Thu Jun 02 2022 Cole Robinson <crobinso@redhat.com> - 8.4.0-1
- Update to version 8.4.0

* Mon May 02 2022 Cole Robinson <crobinso@redhat.com> - 8.3.0-1
- Update to version 8.3.0

* Fri Apr 01 2022 Cole Robinson <crobinso@redhat.com> - 8.2.0-1
- Update to version 8.2.0

* Tue Mar 01 2022 Cole Robinson <crobinso@redhat.com> - 8.1.0-1
- Update to version 8.1.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Cole Robinson <crobinso@redhat.com> - 8.0.0-1
- Update to version 8.0.0

* Tue Jan 11 2022 Cole Robinson <crobinso@redhat.com> - 7.10.0-1
- Update to version 7.10.0

* Wed Nov  3 2021 Daniel P. Berrangé <berrange@redhat.com> - 7.9.0-1
- Update to 7.9.0 release

* Fri Oct  1 2021 Daniel P. Berrangé <berrange@redhat.com> - 7.8.0-1
- Update to 7.8.0 release

* Mon Aug  2 2021 Daniel P. Berrangé <berrange@redhat.com> - 7.6.0-1
- Update to 7.6.0 release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 01 2021 Cole Robinson <crobinso@redhat.com> - 7.5.0-1
- Update to version 7.5.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 7.4.0-2
- Rebuilt for Python 3.10

* Tue Jun 01 2021 Cole Robinson <crobinso@redhat.com> - 7.4.0-1
- Update to version 7.4.0

* Mon Apr 05 2021 Cole Robinson <crobinso@redhat.com> - 7.2.0-1
- Update to version 7.2.0

* Mon Mar 01 2021 Cole Robinson <crobinso@redhat.com> - 7.1.0-1
- Update to version 7.1.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Cole Robinson <crobinso@redhat.com> - 7.0.0-1
- Update to version 7.0.0

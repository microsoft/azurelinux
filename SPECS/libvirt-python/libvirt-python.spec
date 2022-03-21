# Don't want provides for python shared objects
%{?filter_provides_in: %{filter_provides_in} %{python3_sitearch}/.*\.so}

Summary:        The libvirt virtualization API python3 binding
Name:           libvirt-python
Version:        7.10.0
Release:        1%{?dist}
License:        GPLv2+ and LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://libvirt.org
Source0:        https://libvirt.org/sources/python/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libvirt-devel = %{version}
BuildRequires:  python3-devel
BuildRequires:  python3-lxml
%if 0%{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif

%{?filter_setup}

%description
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%package -n python3-libvirt
Summary:        The libvirt virtualization API python3 binding
URL:            https://libvirt.org
%{?python_provide:%python_provide python3-libvirt}
Provides:       libvirt-python3 = %{version}-%{release}
Obsoletes:      libvirt-python3 <= 3.6.0-1%{?dist}

%description -n python3-libvirt
The python3-libvirt package contains a module that permits applications
written in the Python 3.x programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%prep
%autosetup

# Unset execute bit for example scripts; it can introduce spurious
# RPM dependencies, like /usr/bin/python3
# for the -python3 package
find examples -type f -exec chmod 0644 \{\} \;

%build
%py3_build

%install
%py3_install

%check
pip3 install \
    more-itertools \
    pluggy
python3 setup.py test

%files -n python3-libvirt
%license COPYING COPYING.LESSER
%doc ChangeLog AUTHORS README examples/
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
* Wed Jan 05 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.10.0-1
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.
- Updated version to 7.10.0.
- Added BRs for tests.

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

* Tue Dec 01 2020 Cole Robinson <crobinso@redhat.com> - 6.10.0-1
- Update to version 6.10.0

* Tue Nov 03 2020 Cole Robinson <crobinso@redhat.com> - 6.9.0-1
- Update to version 6.9.0

* Thu Oct 15 2020 Daniel P. Berrangé <berrange@redhat.com> - 6.8.0-2
- Fix regression with snapshot handling (rhbz #1888709)

* Fri Oct 02 2020 Cole Robinson <crobinso@redhat.com> - 6.8.0-1
- Update to version 6.8.0

* Wed Sep 02 2020 Cole Robinson <crobinso@redhat.com> - 6.7.0-1
- Update to version 6.7.0

* Tue Aug 04 2020 Cole Robinson <crobinso@redhat.com> - 6.6.0-1
- Update to version 6.6.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 04 2020 Cole Robinson <crobinso@redhat.com> - 6.5.0-1
- Update to version 6.5.0

* Tue Jun 02 2020 Cole Robinson <crobinso@redhat.com> - 6.4.0-1
- Update to version 6.4.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 6.3.0-2
- Rebuilt for Python 3.9

* Tue May 05 2020 Cole Robinson <crobinso@redhat.com> - 6.3.0-1
- Update to version 6.3.0

* Thu Apr 02 2020 Cole Robinson <crobinso@redhat.com> - 6.2.0-1
- Update to version 6.2.0

* Wed Mar 04 2020 Cole Robinson <crobinso@redhat.com> - 6.1.0-1
- Update to version 6.1.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Cole Robinson <crobinso@redhat.com> - 6.0.0-1
- Update to version 6.0.0

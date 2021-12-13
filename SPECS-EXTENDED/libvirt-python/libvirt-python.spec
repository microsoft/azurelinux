# -*- rpm-spec -*-

Summary: The libvirt virtualization API python3 binding
Name: libvirt-python
Version: 6.1.0
Release: 2%{?dist}
Source0: http://libvirt.org/sources/python/%{name}-%{version}.tar.gz
Url: http://libvirt.org
License: LGPLv2+
BuildRequires: libvirt-devel == %{version}
BuildRequires: python3-devel
BuildRequires: python3-nose
BuildRequires: python3-lxml
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

%py3_build


%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-libvirt
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
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
* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 6.1.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora and REHL version checks.

* Wed Mar 04 2020 Cole Robinson <crobinso@redhat.com> - 6.1.0-1
- Update to version 6.1.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Cole Robinson <crobinso@redhat.com> - 6.0.0-1
- Update to version 6.0.0

* Tue Nov 12 2019 Cole Robinson <crobinso@redhat.com> - 5.9.0-1
- Update to version 5.9.0

* Tue Oct 08 2019 Cole Robinson <crobinso@redhat.com> - 5.8.0-1
- Update to version 5.8.0

* Tue Sep 03 2019 Cole Robinson <crobinso@redhat.com> - 5.7.0-1
- Update to version 5.7.0

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 5.6.0-2
- Rebuilt for Python 3.8

* Tue Aug 06 2019 Cole Robinson <crobinso@redhat.com> - 5.6.0-1
- Update to version 5.6.0
- Drop python2 bindings for f31+

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Cole Robinson <crobinso@redhat.com> - 5.5.0-1
- Rebased to version 5.5.0

* Wed Jun 12 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.4.0-1
- Update to 5.4.0 release

* Tue May  7 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.3.0-1
- Update to 5.3.0 release

* Wed Apr  3 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.2.0-1
- Update to 5.2.0 release

* Mon Mar  4 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-1
- Update to 5.1.0 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.0.0-1
- Update to 5.0.0 release

* Mon Nov 12 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.9.0-1
- Update to 4.9.0 release

* Fri Oct  5 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.8.0-2
- Update to 4.8.0 release

* Tue Sep  4 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.7.0-2
- Postpone python2 disablement to Fedora 31

* Tue Sep  4 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.7.0-1
- Update to 4.7.0 release

* Mon Aug  6 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.6.0-1
- Update to 4.6.0 release

* Mon Jul 23 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.5.0-3
- Add BR on gcc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul  3 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.5.0-1
- Update to 4.5.0 release

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-2
- Rebuilt for Python 3.7

* Tue Jun  5 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.4.0-1
- Update to 4.4.0 release

* Sat May 05 2018 Miro Hrončok <mhroncok@redhat.com> - 4.3.0-2
- Update Python macros to new packaging standards
  (See https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build)

* Thu May  3 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.3.0-1
- Update to 4.3.0 release

* Tue Apr  3 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.2.0-1
- Update to 4.2.0 release
- Set python2 to be disabled from Fedora 30 onwards

* Mon Mar  5 2018 Daniel P. Berrange <berrange@redhat.com> - 4.1.0-1
- Update to 4.1.0 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Daniel P. Berrange <berrange@redhat.com> - 4.0.0-1
- Update to 4.0.0 release

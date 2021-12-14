Vendor:         Microsoft Corporation
Distribution:   Mariner
# Define `python3_sitearch' if there is no one:
%{!?python3_sitearch:%global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

# Enable Python 3 in Fedora and RHEL > 7 as default:
# Add `--without python3' option (enable python3 by default):
%bcond_without python3

# Drop Python 2 in Fedora >= 30 and RHEL > 7 as default:
%global drop_python2 1
%global configure_with_python2 no

%if %{with python3}
%global configure_with_python3 yes
%else
%global configure_with_python3 no
%endif

# Additional configure options:
%global with_pythons --with-python=%{configure_with_python2} --with-python3=%{?configure_with_python3}

Summary: An utility for manipulating storage encryption keys and passphrases
Name: volume_key
Version: 0.3.12
Release: 8%{?dist}
# lib/{SECerrs,SSLerrs}.h are both licensed under MPLv1.1, GPLv2 and LGPLv2
License: GPLv2 and (MPLv1.1 or GPLv2 or LGPLv2)
URL: https://pagure.io/%{name}/
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

Source0: https://releases.pagure.org/%{name}/%{name}-%{version}.tar.xz
# Support all LUKS devices
# - backport of 26c09768662d8958debe8c9410dae9fda02292c3
Patch0: volume_key-0.3.12-support_LUKS2_and_more.patch
BuildRequires: gcc
BuildRequires: cryptsetup-luks-devel, gettext-devel, glib2-devel, /usr/bin/gpg2
BuildRequires: gpgme-devel, libblkid-devel, nss-devel, python3-devel
%if 0%{?drop_python2} < 1
BuildRequires: python2-devel
%endif
# Needed by %%check:
BuildRequires: nss-tools

%global desc_common The main goal of the software is to allow restoring access to an encrypted\
hard drive if the primary user forgets the passphrase.  The encryption key\
back up can also be useful for extracting data after a hardware or software\
failure that corrupts the header of the encrypted volume, or to access the\
company data after an employee leaves abruptly.

%global desc_app This package provides a command-line tool for manipulating storage volume\
encryption keys and storing them separately from volumes.\
\
%{desc_common}

%global desc_lib This package provides lib%{name}, a library for manipulating storage volume\
encryption keys and storing them separately from volumes.\
\
%{desc_common}

%global desc_python(V:) This package provides %%{-V:Python %%{-V*}}%%{!-V:Python} bindings for lib%{name}, a library for\
manipulating storage volume encryption keys and storing them separately from\
volumes.\
\
%{desc_common}\
\
%{name} currently supports only the LUKS volume encryption format.  Support\
for other formats is possible, some formats are planned for future releases.

%description
%{desc_app}

%package devel
Summary: A library for manipulating storage encryption keys and passphrases
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
%{desc_lib}

%package libs
Summary: A library for manipulating storage encryption keys and passphrases
Requires: /usr/bin/gpg2

%description libs
%{desc_lib}

%if 0%{?drop_python2} < 1
%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary: Python bindings for lib%{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description -n python2-%{name}
%desc_python
%endif

%if %{with python3}
%package -n python3-%{name}
%{?python_provide:%python_provide python3-%{name}}
Summary: Python 3 bindings for lib%{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
%desc_python -V 3
%endif

%prep
%setup -q
%patch0 -p1

%build
%configure %{?with_pythons}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

# Remove libtool archive
find %{buildroot} -type f -name "*.la" -delete

%find_lang %{name}

%check
make check || { \
echo "======================== ./test-suite.log ========================"; \
cat ./test-suite.log; \
echo "=================================================================="; \
exit 1; \
}

%ldconfig_scriptlets libs

%files
%doc README contrib
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so

%files libs -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS
%{_libdir}/lib%{name}.so.*

%if 0%{?drop_python2} < 1
%files -n python2-%{name}
%{python2_sitearch}/_%{name}.so
%{python2_sitearch}/%{name}.py*
%endif

%if %{with python3}
%files -n python3-%{name}
%{python3_sitearch}/_%{name}.so
%{python3_sitearch}/%{name}.py*
%{python3_sitearch}/__pycache__/%{name}.*
%endif

%changelog
* Mon Mar 16 2021 Henry Li <lihl@microsoft.com> - 0.3.12-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable python2 build and enable python3 build

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.12-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.12-5
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Jiri Kucera <jkucera@redhat.com> - 0.3.12-2
- Add support for LUKS2 and more
- Fix License tag

* Mon Oct 08 2018 Jiri Kucera <jkucera@redhat.com> - 0.3.12-1
- Update to volume_key-0.3.12
  Resolves: #1634850

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 16 2018 Jiri Kucera <jkucera@redhat.com> - 0.3.10-1
- Update to volume_key-0.3.10
  Resolves: #1479349, #1517016

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.9-20
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.9-18
- Switch to %%ldconfig_scriptlets

* Tue Nov 7 2017 Miloslav Trmač <mitr@redhat.com> - 0.3.9-17
- Update for libcryptsetup ABI change

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.3.9-16
- Python 2 binary package renamed to python2-volume_key
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Miloslav Trmač <mitr@redhat.com> - 0.3.9-13
- Point URL: and Source: to the new home at pagure.io
  Resolves: 1456378

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3.9-11
- Rebuild for gpgme 1.18

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-10
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 13 2015 Miloslav Trmač <mitr@redhat.com> - 0.3.9-7
- Don't #include <config.h> in libvolume_key.h
  Patch by Vratislav Podzimek <vpodzime@redhat.com>.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.9-2
- Fix a crash when trying to use passphrase encryption in FIPS mode

* Sat Sep 22 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.9-1
- Update to volume_key-0.3.9

* Mon Aug  6 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.8-4
- Use BuildRequires: /usr/bin/gpg instead of gnupg, for compatibility with RHEL

* Mon Jul 23 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.8-3
- Add Requires: /usr/bin/gpg
  Resolves: #842074

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar  3 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.8-1
- Update to volume_key-0.3.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.7-2
- Rebuild with newer libcryptsetup

* Wed Aug 24 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.7-1
- Update to volume_key-0.3.7

* Fri Jun 10 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.6-2
- Fix a typo
  Resolves: #712256

* Thu Mar 31 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.6-1
- Update to volume_key-0.3.6

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.5-2
- Use %%{?_isa} in Requires:

* Wed Nov 24 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.5-1
- Update to volume_key-0.3.5

* Mon Oct 18 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-4
- Tell the user if asking for the same passphrase again
  Resolves: #641111
- Check certificate file before interacting with the user
  Resolves: #643897

* Fri Oct  8 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-3
- Make it possible to interrupt password prompts
  Resolves: #641111

* Wed Sep 29 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-2
- Clarify which block device should be passed as an argument
  Resolves: #636541
- Recognize SSL error messages from NSS as well
  Resolves: #638732

* Fri Aug 27 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-1
- Update to volume_key-0.3.4

* Mon Jul 26 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.3-3
- Fix build with new gpgme

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Mar 26 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.3-1
- Update to volume_key-0.3.3

* Thu Mar  4 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.2-1
- Update to volume_key-0.3.2
- Drop no longer necessary references to BuildRoot:

* Fri Feb  5 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.1-2
- Fix a crash when an empty passphrase is provided
  Resolves: #558410

* Fri Dec 11 2009 Miloslav Trmač <mitr@redhat.com> - 0.3.1-1
- Update to volume_key-0.3.1.

* Wed Sep 30 2009 Miloslav Trmač <mitr@redhat.com> - 0.3-1
- Update to volume_key-0.3.
- Drop bundled libcryptsetup.

* Sat Aug  8 2009 Miloslav Trmač <mitr@redhat.com> - 0.2-3
- Handle changed "TYPE=crypto_LUKS" from libblkid
- Preserve file timestamps during installation

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Miloslav Trmač <mitr@redhat.com> - 0.2-1
- Initial build.

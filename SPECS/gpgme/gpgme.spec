# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond check 1
# No Qt5 on RHEL 10 and higher
%bcond qt5 %[ 0%{?rhel} < 10 ]
%bcond qt6 1

%global gnupg2_min_ver 2.2.24
%global libgpg_error_min_ver 1.36

# we are doing out of source build
%global _configure ../configure

Name:           gpgme
Summary:        GnuPG Made Easy - high level crypto API
Version:        1.24.3
Release:        6%{?dist}

# MIT: src/cJSON.{c,h} (used by gpgme-json)
License:        LGPL-2.1-or-later AND MIT
URL:            https://gnupg.org/related_software/gpgme/
Source0:        https://gnupg.org/ftp/gcrypt/gpgme/gpgme-%{version}.tar.bz2
Source1:        https://gnupg.org/ftp/gcrypt/gpgme/gpgme-%{version}.tar.bz2.sig
Source3:        https://gnupg.org/signature_key.asc
Source2:        gpgme-multilib.h

## downstream patches
# Don't add extra libs/cflags in gpgme-config/cmake equivalent
Patch1001:      0001-don-t-add-extra-libraries-for-linking.patch
# add -D_FILE_OFFSET_BITS... to gpgme-config, upstreamable
Patch1002:      gpgme-1.3.2-largefile.patch
# Allow extra options to be passed to setup.py during installation
Patch1004:      0002-setup_py_extra_opts.patch

## temporary downstream fixes
# Skip lang/qt/tests/t-remarks on gnupg 2.4+
Patch3001:      1001-qt-skip-test-remarks-for-gnupg2-2.4.patch


BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gawk
BuildRequires:  texinfo
BuildRequires:  gnupg2 >= %{gnupg2_min_ver}
BuildRequires:  gnupg2-smime
BuildRequires:  libgpg-error-devel >= %{libgpg_error_min_ver}
BuildRequires:  libassuan-devel >= 2.4.2

# For python bindings
BuildRequires:  swig

# to remove RPATH
BuildRequires:  chrpath

# For AutoReq cmake-filesystem
BuildRequires:  cmake

Requires:       gnupg2 >= %{gnupg2_min_ver}

# On the following architectures workaround multiarch conflict of -devel packages:
%define multilib_arches %{ix86} x86_64 ia64 ppc ppc64 s390 s390x %{sparc}

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.  It provides a high-level crypto API for
encryption, decryption, signing, signature verification and key
management.

%package devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libgpg-error-devel%{?_isa} >= %{libgpg_error_min_ver}

%description devel
%{summary}.

%package -n %{name}pp
Summary:        C++ bindings/wrapper for GPGME
Obsoletes:      gpgme-pp < 1.8.0-7
Provides:       gpgme-pp = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       gpgme-pp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}pp
%{summary}.

%package -n %{name}pp-devel
Summary:        Development libraries and header files for %{name}-pp
Obsoletes:      gpgme-pp-devel < 1.8.0-7
Provides:       gpgme-pp-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       gpgme-pp-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}pp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-devel%{?_isa}

%description -n %{name}pp-devel
%{summary}

%if %{with qt5}
%package -n q%{name}-qt5
Summary:        Qt5 API bindings/wrapper for GPGME
Requires:       %{name}pp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Test)
Obsoletes:      q%{name} < 1.20.0
Provides:       q%{name}

%description -n q%{name}-qt5
%{summary}.
%endif

%if %{with qt6}
%package -n q%{name}-qt6
Summary:        Qt6 API bindings/wrapper for GPGME
Requires:       %{name}pp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Test)

%description -n q%{name}-qt6
%{summary}.
%endif

%if %{with qt5} || %{with qt6}
%package -n q%{name}-common-devel
Summary:        Common development header files for %{name}-qt5 and %{name}-qt6
Requires:       %{name}pp-devel%{?_isa}

%description -n q%{name}-common-devel
%{summary}.
%endif

%if %{with qt5}
%package -n q%{name}-qt5-devel
Summary:        Development libraries and header files for %{name}-qt5
# before libqgpgme.so symlink was moved to avoid conflict
Conflicts:      kdepimlibs-devel < 4.14.10-17
Requires:       q%{name}-qt5%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       q%{name}-common-devel%{?_isa}
Obsoletes:      q%{name}-devel < 1.20.0
Provides:       q%{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       q%{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n q%{name}-qt5-devel
%{summary}.
%endif

%if %{with qt6}
%package -n q%{name}-qt6-devel
Summary:        Development libraries and header files for %{name}-qt6
Requires:       q%{name}-qt6%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       q%{name}-common-devel%{?_isa}

%description -n q%{name}-qt6-devel
%{summary}.
%endif

%package -n python3-gpg
Summary:        %{name} bindings for Python 3
BuildRequires:  python3-devel
# Needed since Python 3.12+ drops distutils
BuildRequires:  python3-setuptools
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      platform-python-gpg < %{version}-%{release}

%description -n python3-gpg
%{summary}.

%prep
%autosetup -p1 -S gendiff
gpg2 --import --import-options import-export,import-minimal %{SOURCE3} > ./gpg-keyring.gpg
gpgv2 --keyring ./gpg-keyring.gpg %{SOURCE1} %{SOURCE0}

## HACK ALERT
# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g' src/gpgme-config.in

# The build machinery does not support the newest Pythons
sed -i 's/3.13/%{python3_version}/g' configure

%build
# People neeed to learn that you can't run autogen.sh anymore
#./autogen.sh

# Since 1.16.0, we need to explicitly pass -D_LARGEFILE_SOURCE and
# -D_FILE_OFFSET_BITS=64 for the QT binding to build successfully on 32-bit
# platforms.
export CFLAGS='%{optflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'
export CXXFLAGS='%{optflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'
# Explicit new lines in C(XX)FLAGS can break naive build scripts
export CFLAGS="$(echo ${CFLAGS} | tr '\n\\' '  ')"
export CXXFLAGS="$(echo ${CXXFLAGS} | tr '\n\\' '  ')"
export SETUPTOOLS_USE_DISTUTILS=local
#export PYTHON=%{python3}
#export PYTHON_VERSION=%{python3_version}

# Also build either qt5 or qt6
mkdir build
pushd build
%configure --disable-static --disable-silent-rules --enable-languages=cpp,%{?with_qt5:qt,}%{!?with_qt5:%{?with_qt6:qt6,}}python
%make_build
popd

# Build qt6 in extra step if qt5 has been build
%if %{with qt5} && %{with qt6}
mkdir build-qt6
pushd build-qt6
%configure --disable-static --disable-silent-rules --enable-languages=cpp,qt6,python
%make_build
popd
%endif

%install
# When using distutils from setuptools 60+, ./setup.py install use
# the .egg format. This forces setuptools to use .egg-info format.
# SETUP_PY_EXTRA_OPTS is introduced by the Patch1004 above.
export SETUPTOOLS_USE_DISTUTILS=local
export SETUP_PY_EXTRA_OPTS="--single-version-externally-managed --root=/"
# Aliso install either qt5 or qt6
pushd build
%make_install
popd
# Install qt6 in extra step if qt5 has been installed
%if %{with qt5} && %{with qt6}
pushd build-qt6
%make_install
popd
%endif

# unpackaged files
rm -fv %{buildroot}%{_infodir}/dir
rm -fv %{buildroot}%{_libdir}/lib*.la

# Hack to resolve multiarch conflict (#341351)
%ifarch %{multilib_arches}
mv %{buildroot}%{_bindir}/gpgme-config{,.%{_target_cpu}}
cat > gpgme-config-multilib.sh <<__END__
#!/bin/sh
exec %{_bindir}/gpgme-config.\$(arch) \$@
__END__
install -D -p gpgme-config-multilib.sh %{buildroot}%{_bindir}/gpgme-config
mv %{buildroot}%{_includedir}/gpgme.h \
   %{buildroot}%{_includedir}/gpgme-%{__isa_bits}.h
install -m644 -p -D %{SOURCE2} %{buildroot}%{_includedir}/gpgme.h
%endif
chrpath -d %{buildroot}%{_bindir}/%{name}-tool
chrpath -d %{buildroot}%{_bindir}/%{name}-json
chrpath -d %{buildroot}%{_libdir}/lib%{name}pp.so*
# qt5
%if %{with qt5}
chrpath -d %{buildroot}%{_libdir}/libq%{name}.so*
%endif
# qt6
%if %{with qt6}
chrpath -d %{buildroot}%{_libdir}/libq%{name}qt6.so*
%endif

# autofoo installs useless stuff for uninstall
rm -vf %{buildroot}%{python2_sitelib}/gpg/install_files.txt
rm -vf %{buildroot}%{python3_sitelib}/gpg/install_files.txt

%if %{with check}
%check
pushd build
make check
popd
%endif

%files
%license COPYING* LICENSES
%doc AUTHORS NEWS README*
%{_bindir}/%{name}-json
%{_libdir}/lib%{name}.so.11*
%{_mandir}/man1/%{name}-json.*

%files devel
%{_bindir}/%{name}-config
%{_bindir}/%{name}-tool
%ifarch %{multilib_arches}
%{_bindir}/%{name}-config.%{_target_cpu}
%{_includedir}/%{name}-%{__isa_bits}.h
%endif
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_datadir}/aclocal/%{name}.m4
%{_infodir}/%{name}.info*
%{_libdir}/pkgconfig/%{name}*.pc

%files -n %{name}pp
%doc lang/cpp/README
%{_libdir}/lib%{name}pp.so.6*

%files -n %{name}pp-devel
%{_includedir}/%{name}++/
%{_libdir}/lib%{name}pp.so
%{_libdir}/cmake/Gpgmepp/

%if %{with qt5}
%files -n q%{name}-qt5
%doc lang/qt/README
%{_libdir}/libq%{name}.so.15*
%endif

%if %{with qt6}
%files -n q%{name}-qt6
%{_libdir}/libq%{name}qt6.so.15*
%endif

%if %{with qt5} || %{with qt6}
%files -n q%{name}-common-devel
%endif

%if %{with qt5}
%files -n q%{name}-qt5-devel
%{_includedir}/q%{name}-qt5/
%{_libdir}/libq%{name}.so
%{_libdir}/cmake/QGpgme/
%endif

%if %{with qt6}
%files -n q%{name}-qt6-devel
%{_includedir}/q%{name}-qt6/
%{_libdir}/libq%{name}qt6.so
%{_libdir}/cmake/QGpgmeQt6/
%endif

%files -n python3-gpg
%doc lang/python/README
%{python3_sitearch}/gpg-*.egg-info/
%{python3_sitearch}/gpg/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.24.3-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.24.3-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Michal Hlavinka <mhlavink@redhat.com> - 1.24.3-2
- drop %%autochangelog
- restore and truncate changelog to +- last 2 years

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.24.3-2
- Rebuilt for Python 3.14

* Tue May 20 2025 Michal Hlavinka <mhlavink@redhat.com> - 1.24.3-1
- updated to 1.24.3 (#2367321)

* Mon Feb 10 2025 Michal Hlavinka <mhlavink@redhat.com> - 1.24.2-1
- updated to 1.24.2 (#2344637)

* Tue Jan 21 2025 Michal Hlavinka <mhlavink@redhat.com> - 1.24.1-1
- updated to 1.24.1 (#2330378)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 Michal Hlavinka <mhlavink@redhat.com> - 1.24.0-1
- local build

* Tue Oct 22 2024 Michal Hlavinka <mhlavink@redhat.com> - 1.23.2-6
- fix building with setuptools 74+ (rhbz#2319628)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.23.2-4
- Rebuilt for Python 3.13

* Sat Jan 13 2024 Marie Loise Nolden <loise@kde.org> - 1.23.2-2
- add signature file

* Sat Jan 13 2024 Marie Loise Nolden <loise@kde.org> - 1.23.2-1
- Update to 1.23.2

* Wed Oct 11 2023 Michal Hlavinka <mhlavink@redhat.com> - 1.22.0-2
- add tarball signature verification

* Tue Oct 10 2023 Michal Hlavinka <mhlavink@redhat.com> - 1.22.0-1
- updated to 1.22.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild


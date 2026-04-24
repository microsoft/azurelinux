# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           brotli
Version:        1.2.0
Release: 2%{?dist}
Summary:        Lossless compression algorithm

License:        MIT
URL:            https://github.com/google/brotli
Source0:        %{url}/archive/v%{version}/brotli-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++

Requires: libbrotli%{?_isa} = %{version}-%{release}

%global _description %{expand:
Brotli is a generic-purpose lossless compression algorithm that compresses data
using a combination of a modern variant of the LZ77 algorithm, Huffman coding
and 2nd order context modeling, with a compression ratio comparable to the best
currently available general-purpose compression methods. It is similar in speed
with deflate but offers more dense compression.}

%description %{_description}

%package -n libbrotli
Summary:        Library for brotli lossless compression algorithm

%description -n libbrotli %{_description}

%package -n python3-brotli
Summary:        Lossless compression algorithm (python 3)

%description -n python3-brotli %{_description}

This package installs a Python 3 module.

%package devel
Summary:        Lossless compression algorithm (development files)
Requires: brotli%{?_isa} = %{version}-%{release}
Requires: libbrotli%{?_isa} = %{version}-%{release}

%description devel %{_description}

This package installs the development files.

%prep
%autosetup -p1
# fix permissions for -debuginfo
# rpmlint will complain if I create an extra %%files section for
# -debuginfo for this so we'll put it here instead
chmod 644 c/enc/*.[ch]
chmod 644 c/include/brotli/*.h
chmod 644 c/tools/brotli.c

%generate_buildrequires
%pyproject_buildrequires

%build
%cmake \
    -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    -DCMAKE_INSTALL_LIBDIR="%{_libdir}"
%cmake_build
%pyproject_wheel

%install
%cmake_install
# Names of C API (section 3) man pages are too generic; rename them from .3 to
# .3brotli (which is how they were manually installed in the past anyway)
find %{buildroot}%{_mandir}/man3 -name '*.3' -exec mv -v '{}' '{}brotli' ';'
%pyproject_install
%pyproject_save_files -l brotli _brotli

%check
%ctest
%pyproject_check_import
cd python
%{py3_test_envvars} %{python3} -m tests.bro_test
%{py3_test_envvars} %{python3} -m tests.compress_test
%{py3_test_envvars} %{python3} -m tests.compressor_test
%{py3_test_envvars} %{python3} -m tests.decompress_test
%{py3_test_envvars} %{python3} -m tests.decompressor_test

%files
%{_bindir}/brotli
%{_mandir}/man1/brotli.1*

%files -n libbrotli
%license LICENSE
%{_libdir}/libbrotlicommon.so.1*
%{_libdir}/libbrotlidec.so.1*
%{_libdir}/libbrotlienc.so.1*

%files -n python3-brotli -f %{pyproject_files}

%files devel
%{_includedir}/brotli
%{_libdir}/libbrotlicommon.so
%{_libdir}/libbrotlidec.so
%{_libdir}/libbrotlienc.so
%{_libdir}/pkgconfig/libbrotlicommon.pc
%{_libdir}/pkgconfig/libbrotlidec.pc
%{_libdir}/pkgconfig/libbrotlienc.pc
%{_mandir}/man3/constants.h.3brotli*
%{_mandir}/man3/decode.h.3brotli*
%{_mandir}/man3/encode.h.3brotli*
%{_mandir}/man3/types.h.3brotli*

%changelog
* Mon Dec 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.2.0-1
- Update to 1.2.0 (close RHBZ#2401888)
- Stop trying to support EPEL7, which is end-of-life
- Port to pyproject-rpm-macros (close RHBZ#2377212)
- Test the Python extension

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.1.0-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.1.0-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.1.0-7
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.1.0-4
- Rebuilt for Python 3.13

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 15 2023 Jonathan Wright <jonathan@almalinux.org> - 1.1.0-1
- Update to 1.1.1 rhbz#2233368

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.0.9-12
- Rebuilt for Python 3.12

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 03 2022 Jonathan Wright <jonathan@almalinux.org> - 1.0.9-10
- Fix EL7 builds

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.9-8
- Rebuilt for Python 3.11

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.0.9-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 01 2020 Travis Kendrick <pouar@pouar.net> - 1.0.9-3
- Apparently %%autosetup calls %%patch on its own

* Thu Oct 01 2020 Travis Kendrick <pouar@pouar.net> - 1.0.9-2
- Fix pc file (#1884364)

* Wed Sep 30 2020 Travis Kendrick <pouar@pouar.net> - 1.0.9-1
- Update to 1.0.9 (#1872932)

* Wed Aug 12 2020 Carl George <carl@george.computer> - 1.0.7-14
- Update cmake invocation rhbz#1863298

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-11
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec  7 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.7-9
- Splil out the libs to a separate package

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-7
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Apr 20 2019 Orion Poplawski <orion@nwra.com> - 1.0.7-5
- Build with devtoolset-7 on EPEL7 to fix aarch64 builds

* Thu Mar 28 2019 Carl George <carl@george.computer> - 1.0.7-4
- EPEL compatibility

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 09 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-2
- Remove last python2 bits

* Wed Nov 28 2018 Travis Kendrick pouar@pouar.net> - 1.0.7-1
- Update to 1.0.7

* Wed Nov 28 2018 Travis Kendrick pouar@pouar.net> - 1.0.5-2
- remove Python 2 support https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 13 2018 Travis Kendrick pouar@pouar.net> - 1.0.5-1
- update to 1.0.5

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.4-3
- Rebuilt for Python 3.7

* Wed Apr 18 2018 Travis Kendrick pouar@pouar.net> - 1.0.4-2
- update to 1.0.4

* Sat Mar 03 2018 Travis Kendrick <pouar@pouar.net> - 1.0.3-1
- update to 1.0.3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-2
- Switch to %%ldconfig_scriptlets

* Fri Sep 22 2017 Travis Kendrick <pouar@pouar.net> - 1.0.1-1
- update to 1.0.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-4
- add man pages

* Sun May 14 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-3
- wrong directory for ctest
- LICENSE not needed in -devel
- fix "spurious-executable-perm"
- rpmbuild does the cleaning for us, so 'rm -rf %%{buildroot}' isn't needed

* Sat May 13 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-2
- include libraries and development files

* Sat May 06 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-1
- Initial build

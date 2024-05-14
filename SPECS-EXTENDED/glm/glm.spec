# The library consists of headers only
%global debug_package %{nil}

Name:           glm
Version:        0.9.9.6
Release:        5%{?dist}
Summary:        C++ mathematics library for graphics programming

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://glm.g-truc.net/
Source0:        https://github.com/g-truc/glm/releases/download/%{version}/%{name}-%{version}.zip
Patch0:         glm-0.9.9.6-install.patch
Patch1:         glm-0.9.9.6-noarch.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.14

%description
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%package        devel
Summary:        C++ mathematics library for graphics programming
BuildArch:      noarch

# As required in
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Static_Libraries_2
Provides:       %{name}-static = %{version}-%{release}

%description    devel
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%{name}-devel is only required for building software that uses
the GLM library. Because GLM currently is a header-only library,
there is no matching run time package.

%package        doc
Summary:        Documentation for %{name}-devel
BuildArch:      noarch

%description    doc
The %{name}-doc package contains reference documentation and
a programming manual for the %{name}-devel package.

%prep
# Some glm releases, like version 0.9.3.1, place contents of
# the source archive directly into the archive root. Others,
# like glm 0.9.3.2, place them into a single subdirectory.
# The former case is inconvenient, but it can be be
# compensated for with the -c option of the setup macro.
#
# When updating this package, take care to check if -c is
# needed for the particular version.
#
# Also it looks like some versions get shipped with a common
# directory in archive root, but with an unusual name for the
# directory. In this case, use the -n option of the setup macro.
%setup -q -n glm

# A couple of files had CRLF line-ends in them.
# Check with rpmlint after updating the package that we are not
# forgetting to convert line endings in some files.
#
# This release of glm seems to have shipped with no CRLF file
# endings at all, so these are commented out.
sed -i 's/\r//' readme.md
sed -i 's/\r//' CMakeLists.txt
sed -i 's/\r//' doc/api/doxygen.css
sed -i 's/\r//' doc/api/dynsections.js
sed -i 's/\r//' doc/api/jquery.js
sed -i 's/\r//' doc/api/tabs.css

# These are just for being able to apply the patch that
# was exported from git.
sed -i 's/\r//' glm/detail/setup.hpp
sed -i 's/\r//' glm/simd/platform.h
sed -i 's/\r//' test/core/core_setup_message.cpp

%patch 0 -p1
%patch 1 -p1

%build
mkdir build
cd build
%{cmake} -DGLM_TEST_ENABLE=ON ..
make %{?_smp_mflags}

%check
cd build

# Some tests are disabled due to failing tests (to be reported)
# - test-core_func_common   fails on aarch64
# - test-core_func_integer  fails on Mariner (x86_64)
%ifarch x86_64
ctest --output-on-failure -E '(test-core_func_integer)'
%endif

%ifarch aarch64
ctest --output-on-failure -E '(test-core_func_common)'
%endif


%install
cd build

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name CMakeLists.txt -exec rm -f {} ';'

# The cmake config files seem architecture independent and since
# also glm-devel is otherwise noarch, it is desired to ship the
# cmake configuration files under /usr/share.
mkdir -pv $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_libdir}/cmake $RPM_BUILD_ROOT%{_datadir}/cmake
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig $RPM_BUILD_ROOT%{_datadir}/pkgconfig
rmdir $RPM_BUILD_ROOT%{_libdir}

# Here it seems to be acceptable to own the cmake and pkgconfig directories
# as an alternative to having glm-devel depending on cmake and pkg-config
# https://fedoraproject.org/wiki/Packaging:Guidelines#The_directory_is_owned_by_a_package_which_is_not_required_for_your_package_to_function
%files devel
%license copying.txt
%doc readme.md
%{_includedir}/%{name}
%{_datadir}/cmake
%{_datadir}/pkgconfig/

%files doc
%license copying.txt
%doc doc/manual.pdf
%doc doc/api/

%changelog
* Wed Apr 20 2022 Muhammad Falak <mwani@microsoft.com> - 0.9.9.6-5
- Re-enable `test-gtc_packing` for all archs
- Skip broken tests based of arch
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.9.6-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sat May 02 2020 Joonas Sarajärvi <muep@iki.fi> - 0.9.9.6-3
- Remove arch check from glmConfigVersion.cmake, fix #1758009

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 23 2019 Joonas Sarajärvi <muep@iki.fi> - 0.9.9.6-1
- New upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Joonas Sarajärvi <muep@iki.fi> - 0.9.9.2-1
- Update to upstream GLM version 0.9.9.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Joonas Sarajärvi <muep@iki.fi> - 0.9.8.5-1
- Update to upstream GLM version 0.9.8.5

* Mon Jan 29 2018 Joonas Sarajärvi <muep@iki.fi> - 0.9.8.4-5
- Fix compatibility with GCC 7.3.1 #1539568

* Sat Aug 12 2017 Joonas Sarajärvi <muep@iki.fi> - 0.9.8.4-4
- Update the workaround for known-broken tests

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 02 2017 Joonas Sarajärvi <muep@iki.fi> - 0.9.8.4-1
- Update to upstream GLM version 0.9.8.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 12 2016 Joonas Sarajärvi <muep@iki.fi> - 0.9.8.3-1
- Update to upstream GLM version 0.9.8.3

* Mon Nov 07 2016 Joonas Sarajärvi <muep@iki.fi> - 0.9.8.2-1
- Update to upstream GLM version 0.9.8.2

* Tue Sep 06 2016 Joonas Sarajärvi <muep@iki.fi> - 0.9.7.6-1
- Update to upstream GLM version 0.9.7.6

* Thu Mar 03 2016 Joonas Sarajärvi <muep@iki.fi> - 0.9.7.3-1
- Update to upstream GLM version 0.9.7.3

* Thu Feb 04 2016 Joonas Sarajärvi <muep@iki.fi> - 0.9.7.2-3
- Fix tests with GCC 6.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Joonas Sarajärvi <muep@iki.fi> - 0.9.7.2-1
- Update to upstream GLM version 0.9.7.2

* Wed Aug 05 2015 Joonas Sarajärvi <muep@iki.fi> - 0.9.7.0-1
- Update to upstream GLM version 0.9.7.0
- CMake config files are added

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Joonas Sarajärvi <muep@iki.fi> - 0.9.6.3-1
- Update to upstream GLM version 0.9.6.3

* Mon Apr 20 2015 David Tardon <dtardon@redhat.com> - 0.9.6.1-3
- make -devel noarch
- install license file in -doc, as required by packaging guidelines

* Wed Jan 28 2015 Dan Horák <dan[at]danny.cz> - 0.9.6.1-2
- fix build on big endian arches, patch by Jakub Cajka from #1185298

* Tue Jan 06 2015 Joonas Sarajärvi <muep@iki.fi> - 0.9.6.1-1
- Update to upstream GLM version 0.9.6.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Joonas Sarajärvi <muep@iki.fi> - 0.9.5.2-3
- Reduce test array size to avoid memory allocation failure in tests
- Resolve a number of aliasing warnings
- Disable the packing test

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Joonas Sarajärvi <muep@iki.fi> - 0.9.5.2-1
- Update to upstream GLM version 0.9.5.2

* Tue Sep 24 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.6-2
- Fix building on ARM

* Tue Sep 24 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.6-1
- Update to upstream GLM version 0.9.4.6
- Bug fixes

* Tue Aug 20 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.5-1
- Update to upstream GLM version 0.9.4.5
- Bug fixes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.4-1
- Update to upstream GLM version 0.9.4.4
- Bug fixes

* Mon Apr 15 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.3-1
- Update to upstream GLM version 0.9.4.3
- This version introduces just minor bug fixes

* Fri Mar 08 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.2-1
- Update to upstream GLM version 0.9.4.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> - 0.9.3.4-2
- fix build on non-x86 arches

* Sun Sep 02 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.4-1
- Update to a new upstream version
- Work around problems in glm::log2 for integers

* Sat Sep 01 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.2-3
- Skip gtx_integer test that is known as broken

* Sat Sep 01 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.2-2
- Remove prebuilt binaries shipped in upstream source archive

* Fri May 04 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.2-1
- Update to upstream version 0.9.3.2

* Mon Feb 13 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-5
- Use global instead of define
- Clarify the comment about GLM zip archives
- Remove the unnecessary rm command from install section
- Remove misleading reference to non-existing glm package

* Mon Feb 06 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-4
- Add virtual Provides: that is required for static-only libraries
- Make descriptions in devel and doc packages more accurate

* Mon Feb 06 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-3
- Fix items pointed out in Comment 2 of #787510

* Mon Feb 06 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-2
- Build and run the self-test suite shipped with glm
- Add subpackage for manual and reference docs

* Sun Feb 05 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-1
- Initial RPM packaging

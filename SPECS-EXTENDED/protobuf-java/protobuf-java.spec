%global original_name protobuf

Summary:        Protocol Buffers - Google's data interchange format
Name:           %{original_name}-java
Version:        3.11.2
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/protocolbuffers/protobuf
Source:         https://github.com/protocolbuffers/protobuf/archive/v%{version}/%{original_name}-%{version}-all.tar.gz
# For tests (using exactly the same version as the release)
Source1:        https://github.com/google/googletest/archive/5ec7f0c4a113e2f18ac2c6cc7df51ad6afc24081.zip#/googletest-5ec7f0c4a113e2f18ac2c6cc7df51ad6afc24081.zip

BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.gson:gson)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel

%description
Java runtime libraries for the protobuf.

Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package -n %{original_name}-javalite
Summary:        Java Protocol Buffers lite runtime library
BuildArch:      noarch

%description -n %{original_name}-javalite
This package contains Java Protocol Buffers lite runtime library.

%package -n %{original_name}-java-util
Summary:        Utilities for Protocol Buffers
BuildArch:      noarch

%description -n %{original_name}-java-util
Utilities to work with protos. It contains JSON support
as well as utilities to work with proto3 well-known types.

%package -n %{original_name}-javadoc
Summary:        Javadoc for %{original_name}-java
BuildArch:      noarch

%description -n %{original_name}-javadoc
This package contains the API documentation for %{original_name}-java.

%package -n %{original_name}-parent
Summary:        Protocol Buffer Parent POM
BuildArch:      noarch

%description -n %{original_name}-parent
Protocol Buffer Parent POM.

%package -n %{original_name}-bom
Summary:        Protocol Buffer BOM POM
BuildArch:      noarch

%description -n %{original_name}-bom
Protocol Buffer BOM POM.

%prep
%setup -q -n %{original_name}-%{version} -a 1
%autopatch -p1
mv googletest-5ec7f0c4a113e2f18ac2c6cc7df51ad6afc24081/* third_party/googletest/
find -name \*.cc -o -name \*.h | xargs chmod -x

%pom_remove_dep org.easymock:easymockclassextension java/pom.xml java/core/pom.xml java/lite/pom.xml java/util/pom.xml
%pom_remove_dep com.google.truth:truth java/pom.xml java/core/pom.xml java/lite/pom.xml java/util/pom.xml
%pom_remove_dep com.google.errorprone:error_prone_annotations java/util/pom.xml
%pom_remove_dep com.google.guava:guava-testlib java/pom.xml java/util/pom.xml
# These use easymockclassextension
rm java/core/src/test/java/com/google/protobuf/ServiceTest.java
# These use truth or error_prone_annotations or guava-testlib
rm java/core/src/test/java/com/google/protobuf/LiteralByteStringTest.java
rm java/core/src/test/java/com/google/protobuf/BoundedByteStringTest.java
rm java/core/src/test/java/com/google/protobuf/RopeByteStringTest.java
rm java/core/src/test/java/com/google/protobuf/RopeByteStringSubstringTest.java
rm -r java/util/src/test/java/com/google/protobuf/util
rm -r java/util/src/main/java/com/google/protobuf/util

# Make OSGi dependency on sun.misc package optional
%pom_xpath_inject "pom:configuration/pom:instructions" "<Import-Package>sun.misc;resolution:=optional,*</Import-Package>" java/core

# Backward compatibility symlink
%mvn_file :protobuf-java:jar: %{original_name}/%{original_name}-java %{original_name}

# This test is incredibly slow on arm
# https://github.com/google/protobuf/issues/2389
%ifarch %{arm} s390x
mv java/core/src/test/java/com/google/protobuf/IsValidUtf8Test.java \
   java/core/src/test/java/com/google/protobuf/IsValidUtf8Test.java.slow
mv java/core/src/test/java/com/google/protobuf/DecodeUtf8Test.java \
   java/core/src/test/java/com/google/protobuf/DecodeUtf8Test.java.slow
%endif

rm -f src/solaris/libstdc++.la

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%configure

%make_build

%ifarch s390x %{arm}
export MAVEN_OPTS=-Xmx1024m
%endif
%mvn_build -s -- -f java/pom.xml

%check
# Java tests fail on s390x
%ifarch s390x
fail=0
%else
fail=1
%endif
make %{?_smp_mflags} check || exit $fail


%install
%mvn_install

%files -f .mfiles-protobuf-java
%doc examples/AddPerson.java examples/ListPeople.java
%doc java/README.md
%license LICENSE

%files -n %{original_name}-java-util -f .mfiles-protobuf-java-util

%files -n %{original_name}-javadoc -f .mfiles-javadoc
%license LICENSE

%files -n %{original_name}-parent -f .mfiles-protobuf-parent
%license LICENSE

%files -n %{original_name}-bom -f .mfiles-protobuf-bom
%license LICENSE

%files -n %{original_name}-javalite -f .mfiles-protobuf-javalite
%license LICENSE

%changelog
* Mon Oct 04 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.11.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing all but Java components as the rest is provided through a separate spec.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Adrian Reber <adrian@lisas.de> - 3.11.2-1
- Update to 3.11.2

* Tue Nov 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-9
- Drop python2-protobuf (#1765879)

* Sat Oct 26 2019 Orion Poplawski <orion@nwra.com> - 3.6.1-8
- Drop obsolete BR on python-google-apputils

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 8 2019 Orion Poplawski <orion@nwra.com> - 3.6.1-4
- Update emacs packaging to comply with guidelines

* Wed Feb 27 2019 Orion Poplawski <orion@nwra.com> - 3.6.1-3
- Update googletest to 1.8.1 to re-enable tests

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 23 2018 Felix Kaechele <heffer@fedoraproject.org> - 3.6.1-1
- update to 3.6.1
- obsolete javanano subpackage; discontinued upstream

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-8
- Rebuild for new binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-6
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.5.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-4
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-2
- Switch to %%ldconfig_scriptlets

* Thu Nov 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-1
- Update to 3.5.0

* Mon Nov 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Mat Booth <mat.booth@redhat.com> - 3.3.1-2
- Make OSGi dependency on sun.misc package optional. This package is not
  available in all execution environments and will not be available in Java 9.

* Mon Jun 12 2017 Orion Poplawski <orion@cora.nwra.com> - 3.3.1-1
- Update to 3.3.1

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Orion Poplawski <orion@cora.nwra.com> - 3.2.0-1
- Update to 3.2.0 final

* Mon Jan 23 2017 Orion Poplawski <orion@cora.nwra.com> - 3.2.0-0.1.rc2
- Update to 3.2.0rc2

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-6
- Rebuild for Python 3.6

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-5
- Disable slow test on arm

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-4
- Ship python 3 module

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-3
- Fix jar file compat symlink

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-2
- Add needed python requirement

* Fri Nov 04 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-2
- Make various sub-packages noarch

* Fri Nov 04 2016 gil cattaneo <puntogil@libero.it> 3.1.0-2
- enable javanano
- minor changes to adapt to current guidelines

* Fri Nov 04 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-1
- Update to 3.1.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-3
- Tests no longer segfaulting on arm

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 6 2015 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-1
- Update to 2.6.1
- New URL
- Cleanup spec
- Add patch to fix emacs compilation with emacs 24.4
- Drop java-fixes patch, use pom macros instead
- Add BR on python-google-apputils and mvn(org.easymock:easymock)
- Run make check
- Make -static require -devel (bug #1067475)

* Thu Mar 26 2015 Kalev Lember <kalevlember@gmail.com> - 2.6.0-4
- Rebuilt for GCC 5 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.6.0-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Dec 17 2014 Peter Lemenkov <lemenkov@gmail.com> - 2.6.0-2
- Added missing Requires zlib-devel to protobuf-devel (see rhbz #1173343). See
  also rhbz #732087.

* Sun Oct 19 2014 Conrad Meyer <cemeyer@uw.edu> - 2.6.0-1
- Bump to upstream release 2.6.0 (rh# 1154474).
- Rebase 'java fixes' patch on 2.6.0 pom.xml.
- Drop patch #3 (fall back to generic GCC atomics if no specialized atomics
  exist, e.g. AArch64 GCC); this has been upstreamed.

* Sun Oct 19 2014 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-11
- protobuf-emacs requires emacs(bin), not emacs (rh# 1154456)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-9
- Update to current Java packaging guidelines

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5.0-7
- Use Requires: java-headless rebuild (#1067528)

* Thu Dec 12 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-6
- BR python-setuptools-devel -> python-setuptools

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Dan Horák <dan[at]danny.cz> - 2.5.0-4
- export the new generic atomics header (rh #926374)

* Mon May 6 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5.0-3
- Add support for generic gcc atomic operations (rh #926374)

* Sat Apr 27 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-2
- Remove changelog history from before 2010
- This spec already runs autoreconf -fi during %%build, but bump build for
  rhbz #926374

* Sat Mar 9 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-1
- Bump to latest upstream (#883822)
- Rebase gtest, maven patches on 2.5.0

* Tue Feb 26 2013 Conrad Meyer <cemeyer@uw.edu> - 2.4.1-12
- Nuke BR on maven-doxia, maven-doxia-sitetools (#915620)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.4.1-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jan 20 2013 Conrad Meyer <konrad@tylerc.org> - 2.4.1-9
- Fix packaging bug, -emacs-el subpackage should depend on -emacs subpackage of
  the same version (%%version), not the emacs version number...

* Thu Jan 17 2013 Tim Niemueller <tim@niemueller.de> - 2.4.1-8
- Added sub-package for Emacs editing mode

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Dan Horák <dan[at]danny.cz> - 2.4.1-6
- disable test-suite until g++ 4.7 issues are resolved

* Mon Mar 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4.1-5
- Update to latest java packaging guidelines

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.4.1-2
- Adding zlib-devel as BR (rhbz: #732087)

* Thu Jun 09 2011 BJ Dierkes <wdierkes@rackspace.com> - 2.4.1-1
- Latest sources from upstream.
- Rewrote Patch2 as protobuf-2.4.1-java-fixes.patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.0-6
- Fix java subpackage bugs #669345 and #669346
- Use new maven plugin names
- Use mavenpomdir macro for pom installation

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.0-5
- generalize hardcoded reference to 2.6 in python subpackage %%files manifest

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 James Laska <jlaska@redhat.com> - 2.3.0-3
- Correct use of %%bcond macros

* Wed Jul 14 2010 James Laska <jlaska@redhat.com> - 2.3.0-2
- Enable python and java sub-packages

* Tue May 4 2010 Conrad Meyer <konrad@tylerc.org> - 2.3.0-1
- bump to 2.3.0

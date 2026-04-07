## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global shver 4
%global maven_group_id tw.edu.ntu.csie
%global pom_file_version 3.35
%global octpkg %{name}
%global release_date 2025-12-21
%global cpp_std c++17
%global giturl https://github.com/cjlin1/libsvm

%if %{defined rhel}
%bcond java 0
%else
%ifarch %{java_arches}
%bcond java 1
%else
%bcond java 0
%endif
%endif

%bcond octave %[!0%{?rhel}]
%bcond python %[!0%{?rhel}]

Name:           libsvm
Version:        3.37
Release:        %autorelease
Summary:        A Library for Support Vector Machines

%global upver   %(tr -d . <<< %{version})

License:        BSD-3-Clause
URL:            https://www.csie.ntu.edu.tw/~cjlin/libsvm/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/v%{upver}/%{name}-%{upver}.tar.gz
Source1:        https://www.csie.ntu.edu.tw/~cjlin/libsvm/log
Source2:        https://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf
Source3:        libsvm-svm-toy-qt.desktop
Source4:        LibSVM-svm-toy-48.png
# Java interface files
Source5:        https://repo1.maven.org/maven2/tw/edu/ntu/csie/%{name}/%{pom_file_version}/%{name}-%{pom_file_version}.pom
# Octave interface files
Source6:        libsvm.INDEX
Source7:        libsvm.CITATION
Source8:        libsvm.DESCRIPTION
Patch:          %{name}.packageMain.patch
Patch:          %{name}.javaDir.patch
Patch:          %{name}.toolsDir.patch
Patch:          %{name}.svm-toy-qt5.patch

%description
LIBSVM is integrated software for support vector classification (C-SVC,
nu-SVC), regression (epsilon-SVR, nu-SVR) and distribution estimation
(one-class SVM).  It supports multi-class classification.

%package devel
Summary:        Development files for libsvm in C, C++ and Java
BuildRequires:  gcc-c++
BuildRequires:  make
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Header and object files for libsvm in C, C++ and Java.  Install this package
if you want to develop programs with libsvm.

%if %{with python}
%package -n     python3-%{name}
Summary:        Python3 tools and interfaces for libsvm
BuildRequires:  python3-devel
#gnuplot is required by easy.py
Requires:       gnuplot
Recommends:     %{py3_dist scipy}

%description -n python3-%{name}
Python3 tools and interfaces for libsvm.  Install this package if you want to
develop programs with libsvm in Python3.
%endif

%if %{with java}
%package        java
Summary:        Java tools and interfaces for libsvm
BuildRequires:  java-devel
BuildRequires:  javapackages-tools
BuildRequires:  maven-local
BuildArch:      noarch
Requires:       javapackages-tools
Requires:       %{name} = %{version}-%{release}

%description    java
Java tools and interfaces for libsvm.  Install this package if you want to
develop programs with libsvm in Java.

%package        javadoc
Summary:        Javadoc for libsvm
BuildRequires:  java-devel
BuildRequires:  javapackages-tools
BuildArch:      noarch
Requires:       %{name}-java = %{version}-%{release}

%description    javadoc
Javadoc for libsvm
%endif

%if %{with octave}
%package -n     octave-%{name}
Summary:        Octave interface to libsvm
BuildRequires:  octave-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       octave

%description -n octave-%{name}
Octave interface for libsvm.
%endif

%package        svm-toy-qt
Summary:        QT version of svm-toy (libsvm demonstration program)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig
BuildRequires:  qt5-qtbase-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    svm-toy-qt
svm-toy is a libsvm demonstration program which has a qt-GUI to display the
derived separating hyperplane.

%prep
%autosetup -p0 -n %{name}-%{upver}

%conf
cp -p %{SOURCE1} ChangeLog
cp -p %{SOURCE2} %{SOURCE3} .
cp -p %{SOURCE4} %{name}-svm-toy-qt-48.png

%if %{with java}
cp -p %{SOURCE5} pom.xml

# org.sonatype.oss.oss-parent is deprecated and slated for removal from Fedora
%pom_remove_parent

# Update the POM file, which is stuck on version 3.35
%pom_xpath_set '/pom:project/pom:version' %{version}

%mvn_file %{maven_group_id}:%{name} %{maven_group_id}/%{name}
%endif

# Fix line endings
sed -i.orig 's/\r//' FAQ.html
touch -r FAQ.html.orig FAQ.html
rm FAQ.html.orig

%if %{with python}
# Fix shebangs
%py3_shebang_fix tools
# Remove useless shebangs
for p in python/libsvm/{commonutil,svm,svmutil}.py; do
    sed -i.orig '1,+1d' $p
    touch -r $p.orig $p
    rm $p.orig
done
%endif

%if %{with python}
%generate_buildrequires
cd python
%pyproject_buildrequires
%endif

%build
# Build the library
make all RPM_CFLAGS='%{build_cflags}' LIBDIR='%{_libdir}' CPP_STD='%{cpp_std}'

%if %{with java}
# Build the Java interface
%mvn_artifact pom.xml java/%{name}.jar
make -C java all javadoc
%endif

%if %{with octave}
# Build the octave interface
cd matlab
octave -H -q --no-window-system --no-site-file << EOF
make
EOF
cd -
%endif

%if %{with python}
# Build the python interface
cd python
%pyproject_wheel
cd -
%endif

%install
%make_install LIBDIR='%{_libdir}' LIBSVM_VER='%{version}' CPP_STD='%{cpp_std}'
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
cp -p %{name}-svm-toy-qt-48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
mkdir -p %{buildroot}%{_datadir}/applications
cp -p %{name}-svm-toy-qt.desktop %{buildroot}%{_datadir}/applications

ln -s %{name}.so.%{shver} %{buildroot}%{_libdir}/%{name}.so

%if %{with python}
# Python
cd python
%pyproject_install
%pyproject_save_files -l libsvm
cd -
cd tools
for p in *.py; do
    install -p -m 755 $p %{buildroot}%{_bindir}/svm-$p
done
cd -
%endif

%if %{with java}
# Java
make -C java install JAVA_TARGET_DIR='%{buildroot}%{_javadir}'
mkdir -p  %{buildroot}%{_javadocdir}/%{name}
cp -p -R java/docs/* %{buildroot}%{_javadocdir}/%{name}

%mvn_install
%endif

%if %{with octave}
# Octave
# FIXME: the *.mex files are arch-specific, so they should go into octpkglibdir
# like the *.oct files do.  But octave refuses to load them from there.  It will
# only load them if they are in octpkgdir.  I don't know why.
mkdir -p %{buildroot}%{octpkgdir}/packinfo
cp -p matlab/*.mex %{buildroot}%{octpkgdir}
cp -p COPYRIGHT %{buildroot}%{octpkgdir}/packinfo/COPYING
cp -p %{SOURCE6} %{buildroot}%{octpkgdir}/packinfo/INDEX
cp -p %{SOURCE7} %{buildroot}%{octpkgdir}/packinfo/CITATION
sed 's/@VERSION@/%{version}/;s/@DATE@/%{release_date}/' %{SOURCE8} \
    > %{buildroot}%{octpkgdir}/packinfo/DESCRIPTION
cat > %{buildroot}%{octpkgdir}/packinfo/on_uninstall.m << EOF
function on_uninstall (desc)
  error ('Can not uninstall %%s installed by the redhat package manager', desc.name);
endfunction
EOF
%endif

# Desktop files
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}-svm-toy-qt.desktop

# Rename READMEs to avoid name collisions
mv python/README python/README-Python
mv tools/README tools/README-Tools
cp -p README java/README-Java

%if %{with octave}
%post -n octave-%{name}
%octave_cmd pkg rebuild

%preun -n octave-%{name}
%octave_pkg_preun

%postun -n octave-%{name}
%octave_cmd pkg rebuild
%endif

%files
%doc COPYRIGHT FAQ.html ChangeLog guide.pdf
%{_bindir}/svm-predict
%{_bindir}/svm-scale
%{_bindir}/svm-train
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/examples
%{_libdir}/%{name}.so.4

%files devel
%doc README
%{_includedir}/%{name}/
%{_libdir}/%{name}.so

%if %{with octave}
%files -n octave-%{name}
%{octpkgdir}/
%endif

%if %{with python}
%files -n python3-%{name} -f %{pyproject_files}
%doc python/README-Python tools/README-Tools
%{_bindir}/svm-*.py
%endif

%if %{with java}
%files java -f .mfiles
%doc java/README-Java
%{_javadir}/%{name}.jar

%files javadoc
%{_javadocdir}/%{name}/
%endif

%files svm-toy-qt
%doc README
%{_bindir}/svm-toy-qt
%{_datadir}/icons/hicolor/48x48/apps/%{name}-svm-toy-qt-48.png
%{_datadir}/applications/*%{name}-svm-toy-qt.desktop

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.37-2
- Latest state for libsvm

* Mon Dec 29 2025 Jerry James <loganjerry@gmail.com> - 3.37-1
- Version 3.37
- Recommend scipy

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.36-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.36-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Aug 07 2025 Orion Poplawski <orion@nwra.com> - 3.36-5
- Fix up rpmdev-bumpspec release breakage

* Thu Aug 07 2025 Orion Poplawski <orion@nwra.com> - 3.36-4
- Rebuild for Octave 10.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.36-2
- Rebuilt for Python 3.14

* Mon May 12 2025 Jerry James <loganjerry@gmail.com> - 3.36-1
- Version 3.36

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Jerry James <loganjerry@gmail.com> - 3.35-2
- Move configuration steps to %%conf

* Tue Sep 03 2024 Jerry James <loganjerry@gmail.com> - 3.35-1
- Version 3.35

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Jerry James <loganjerry@gmail.com> - 3.33-1
- Version 3.33
- Minor spec file simplifications and cleanups

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 3.32-5
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 3.32-1
- Version 3.32
- Drop upstreamed matlab patch

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 3.31-2
- Rebuilt for Python 3.12

* Tue Feb 28 2023 Jerry James <loganjerry@gmail.com> - 3.31-1
- Version 3.31

* Mon Feb 27 2023 Jerry James <loganjerry@gmail.com> - 3.30-2
- Dynamically generate python BuildRequires

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 3.30-1
- Version 3.3
- Convert License tag to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul  5 2022 Jerry James <loganjerry@gmail.com> - 3.25-7
- Remove Java support on i686 (rhbz#2104073)

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.25-6
- Rebuilt for Python 3.11

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.25-5
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.25-2
- Rebuilt for Python 3.10

* Wed Apr 14 2021 Jerry James <loganjerry@gmail.com> - 3.25-1
- Version 3.25
- Drop support for RHEL 6
- Build for JDK 1.8 instead of 1.7
- Python subpackage is archful again
- Python subpackage requires scipy
- Add missing dependency on octave to the octave subpackage
- Miscellaneous spec file cleanups

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 3.24-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.24-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Jerry James <loganjerry@gmail.com> - 3.24-1
- Upstream update to 3.24
- Make Java and Python subpackages be noarch
- Add octave subpackage
- Miscellaneous spec file cleanups

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.23-7
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.23-4
- Remove Python 2 subpackage (#1655696)

* Tue Aug 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.23-3
- Fix Provides/Obsoletes for old python subpackage

* Thu Jul 26 2018 Ding-Yi Chen <dchen@redhat.com> - 3.23-2
- Add -javadoc subpackage
- Use macro rhel instead of el_version
- qt5 in EL should be qt5-qtbase

* Thu Jul 19 2018 Ding-Yi Chen <dchen@redhat.com> - 3.23-1
- Upstream update to 3.23
  + add more digits of predicted file, model file, scaled data and data
    from matlab libsvmwrite: to .17g
  + svm-toy-gtk is no longer supported
  + Dependency qt is updated to qt5
- probability output:
  + if 2 classes, directly output the predited probabilities
    rather than run the iterative algorithms for multi-class situations
- java:
  + libsvm.jar generated by java 1.7 rather than 1.5
  + change the use of "_" in svm.java, which won't be allowed in later java
- python:
  + split to python2 and python3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.21-6
- Python 2 binary package renamed to python2-libsvm
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 07 2016 Than Ngo <than@redhat.com> - 3.21-2
- bz#1392340, enable java part on ppc64

* Wed Jul 20 2016 Ding-Yi Chen <dchen@redhat.com> - 3.21-1
- Upstream update to 3.21
- Fixes Bug 1277450 - libsvm(-java) remove versioned jars from {_javadir}

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.20-4
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 20 2015 Ding-Yi Chen <dchen@redhat.com> - 3.20-3
- Fix for RHEL6

* Tue Jan 20 2015 Ding-Yi Chen <dchen@redhat.com> - 3.20-2
- Upstream update to 3.20

* Fri Dec 19 2014 Jerry James <loganjerry@gmail.com> - 3.18-7
- Install maven POM and depmaps (bz 1175898)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Richard Hughes <richard@hughsie.com> - 3.18-5
- Do not use vendor prefixes on Fedora

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Ding-Yi Chen <dchen@redhat.com> - 3.18-3
- EPEL5 desktop files need vendor.

* Mon Apr 28 2014 Ding-Yi Chen <dchen@redhat.com> - 3.18-2
- Fixed Bug 1090844 - libsvm-java has unresolved dependencies on epel6 testing

* Tue Apr 22 2014 Ding-Yi Chen <dchen@redhat.com> - 3.18-1
- Upstream update to 3.18
- svm.cpp and svm-scale.c: check return values of fscanf
- matlab interface: Makefile no longer handles octave
  because make.m should be used

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.17-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Jon Ciesla <limburgher@gmail.com> - 3.17-2
- Drop desktop vendor tag.

* Sat Apr 13 2013 Ding-Yi Chen <dchen@redhat.com> - 3.17-1
- Upstream update from 3.13 to 3.17
  svm.c and svm.h:
    add sv_indices in model structure, so users can know which training instances are SVs
    two library funs svm_get_sv_indices and svm_get_nr_sv are added
    max_iter warning moved to stderr so -q won't disable it
  svm-train.c:
    usage modified to stress that multiclass is supported
  svm-predict.c:
    add -q for svm-predict
  svm-scale.c:
    issue a warning if feature indices do not start from 1
    issue a warning for inconsistency between scaling-factor file and input file
  tools:
    subset.py is written to be much faster
  fix the bug of not freeing sv_indices
  tools/grid.py:
    -null option: allow the search on C or g only
    -resume option: resume tasks from an earlier run
     can be called as a python module
  python interface:
    local package searched first
  libsvm options can be str or list
  param.show() becomes print(param)
  tools/:
    easy.py fails in 3.15. Fix it by modifying grid.py
  svm.cpp:
    if class labels are 1 and -1, ensure labels[0] = 1 and labels[1] = -1
    initialize model->sv_indices as null in svm_load_model
    if nr_fold > # data, change nr_fold to be # data and ro leave-one-out cv
  matlab interface:
    handle the problem where output variables are not specified

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 04 2012 Ding-Yi Chen <dchen@redhat.com> - 3.12-1
- Upstream update:
  svm-toy: support loading/saving of regression data
  python interface: handle the issue of the "0th" feature if using lists
  tools/grid.py: not redrawing contour if c,g, cv doesn't change
  add setlocale when saving and loading model so not affected by users' locale

* Thu Jan 12 2012 Ding-Yi Chen <dchen@redhat.com> - 3.11-3
- Fixed Bug 646154 - libsvm-python's pth is not set correctly

* Fri Jun 17 2011 Ding-Yi Chen <dchen@redhat.com> - 3.11-1
- Upstream update:
  + Set max number of iterations in the main loop of solvers
  + matlab:
    new make.m for unix/mac/windows and for matlab/octave
  + matlab and python:
    fix a problem that decision values returned by svmpredict is empty if number of classes = 1

* Fri Jun 17 2011 Ding-Yi Chen <dchen@redhat.com> - 3.1-2
- Fix the build error on EL-5

* Tue Jun 14 2011 Ding-Yi Chen <dchen@redhat.com> - 3.1-1
- svm tools is now installed in /usr/bin as svm-*.py
  i.e. tools/easy.py is linked as svm-easy.py.
- Upstream update:
  + MATLAB interface:
  + Merge matlab interface to core libsvm
  + Using mexPrintf() when calling info() in MATLAB interface.
  + Both 32- and 64-bit windows binary files are provided
  + Java:
    Math.random is replaced by Random in java interface
  + Python interface:
    subroutines to get SVs
    relative path to load *.dll and *.so
  + svm.cpp:
    null pointer check before release memory in svm_free_model_content()
    svm_destroy_model() no longer supported.
  + svm-train.c and svm-predict.c
    Better format check in reading data labels
  + svm-toy:
    fix the svm_toy dialog path
  + tools:
    Using new string formatting/encoding in tools/*.py
    clearer png output, fix grid.py legend

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Ding-Yi Chen <dchen@redhat.com> - 3.0-2
- Fixed [Bug 661404] New: Wrong symbolic link libsvm.so

* Mon Nov 08 2010 Ding-Yi Chen <dchen@redhat.com> - 3.0-1
- Fixed the spelling errors of svm-toy-gtk and svm-toy-qt
- Upstream update:
  * Move model structure to svm.h
  * Two functions for freeing a model (content or the whole model)
  * QD from Qfloat to double (better precision because SSE on 64-bit machines less accurate than i387 on 32-bit
  * exit status for checkdata.py
  * old python interface (swig) is removed

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.91-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 07 2010 Ding-Yi Chen <dchen@redhat.com> - 2.91-1
- Fixed Bug 564887 - FTBFS libsvm-2.90-3.fc13
- Upstream update:
  * completely new python interface using ctype
  * new way to set the print_string function
  * Java: able to load model from a BufferedReader directly
  * fix grid.py so -log2c can be run under python 2.6 or after

* Thu Nov 05 2009 Ding-Yi Chen <dchen@redhat.com> - 2.90-2
- Obsoletes libsvm-java for ppc and ppc64.

* Wed Nov 04 2009 Ding-Yi Chen <dchen@redhat.com> - 2.90-1
- Upstream update to 2.9, change to 2.90 for conveniently update.
  + tools/*.py can be run under python 3.0
  + svm_set_quiet() in python interface to disable outputs
  + check gamma < 0
  + internal functions to be static

* Fri Sep 18 2009 Ding-Yi Chen <dchen@redhat.com> - 2.89-4
- Fixed [Bug 524108] put libsvm.jar into _javadir
  + Move livsvm.jar to _javadir
  + Move test_applet.html to _datadir/doc/libsvm-<version>
- Buildrequire changed to java-devel>=1.5.0, jpackage-utils
- Require changed to java>=1.5.0, jpackage-utils

* Wed Sep 16 2009 Ding-Yi Chen <dchen@redhat.com> - 2.89-3
- Fix the building for EL-5
  Note that libsvm-java on ppc and ppc64 for EL-5 is excluded,
  as java-1.6.0-openjdk-devel for them do not exist yet.
- Change the Java buildrequires from java-sdk to java-1.6.0-openjdk-devel
- Fix [Bug 521194] Python: 'import libsvm' doesn't work.
   By adding __init__.py to libsvm_python_dir

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 03 2009 Ding-Yi Chen <dchen@redhat.com> - 2.89-1
- Upstream Update to 2.89:
  + reduce input/loading time of svm-train/svm-predict by half
  + pointer function so users can specify their own outputs
  + remove info_flush()
  + a extern variable libsvm_version
  + svm-train -q option (disable outputs)
  + svm-scale: warning if more nonzero produced
  + easy.py: popel.communiate() to avoid some deadlock (if lots of
    outputs when #classes is large)

* Mon Nov 10 2008 Ding-Yi Chen <dchen@redhat.com> - 2.88-2
- Fix java BuildRequire and Build
- javadoc have been removed because ppc and ppc64 do not have a
  suitable package to build javadoc in F-8, nor does javadoc
  provide much useful information.


* Wed Nov 05 2008 Ding-Yi Chen <dchen@redhat.com> - 2.88-0
- Note:
  + SO version now follows upstream, i.e. SHVER=1, as upstream start to build shared library now.
    Be aware that previously SO version of libsvm.so is libsvm.so.2.86, which looks higher than
    the current SO version libsvm.so.1.
  + Replaced java-1.5.0-gcj-devel with  java-1.6.0-openjdk-devel.
  + java sub-package now have javadoc.
- Upstream update
  + From 2.87: 2008/10/13
    * svm-toy/qt updated to qt4 from qt3
    * fix a bug in svm-scale.c
    * max feature index of -r file is considered
    * Makefile: add make lib; add -Wconversion and -fPIC in Makefile
    * Add "rb" in load_model of svm.cpp
    * Simplify do_shrinking of svm.cpp
    * Change the order of loops in reconstrict_gradient of svm.cpp
    * save the number of kernel evaluations
    * Add python/setup.py
  + From 2.88: 2008/10/30
    * better gradient reconstructions
    * issue a warning when -h 0 may be faster

* Tue Apr 29 2008 Ding-Yi Chen <dchen@redhat.com> - 2.86-13
- Fix svm-toy-qt clear button does not clear.
  (from Hsiang-Fu Yu in National Taiwan University)


* Thu Apr 3 2008 Ding-Yi Chen <dchen@redhat.com> - 2.86-12
- Correct changelog date

* Thu Apr 3 2008 Ding-Yi Chen <dchen@redhat.com> - 2.86-11
- Fix the Qt path problem

* Wed Apr 2 2008 Ding-Yi Chen <dchen@redhat.com> - 2.86-4
- Support both Qt3 for F8 and earlier, and Qt4 for F9

* Tue Apr 1 2008 Ding-Yi Chen <dchen@redhat.com> - 2.86-0
- Upstream update to 2.86
  - svm-scale for java
  - version number in svm.h and svm.m4
  - rename svmtrain.exe to svm-train.exe
  - python: while 1 --> while True, Popen -> call
  - show best parameters on the contour of grid.py
- LIBSVM_VER_MAJOR and LIBSVM_VER_MINOR are defined in libsvm.spec instead in

* Tue Mar 11 2008 Ding-Yi Chen <dchen@redhat.com> - 2.85-6
- Fix build error.

* Mon Mar 10 2008 Ding-Yi Chen <dchen@redhat.com> - 2.85-5
- [Bug 436392]: Fix by copy from right place.
-  Add desktop files and icons for svm-toy-gtk and svm-toy-qt

* Mon Feb 11 2008 Ding-Yi Chen <dchen@redhat.com> - 2.85-4
- Move gnuplot from BuildRequires to Requires

* Thu Feb 07 2008 Ding-Yi Chen <dchen@redhat.com> - 2.85-3
- Fix linker name (libsvm.so)
- Linked to dynamic libraries

* Tue Feb 05 2008 Ding-Yi Chen <dchen@redhat.com> - 2.85-2
- Fix svm-toy-qt build error

* Tue Feb 05 2008 Ding-Yi Chen <dchen@redhat.com> - 2.85-1
- Fix svm-toy-gtk build error

* Mon Feb 04 2008 Ding-Yi Chen <dchen@redhat.com> - 2.85-0
- Upgrade to 2.85
- Include guide.pdf in main package
- Change the dependent from eclipse-ecj to java-1.5.0-gcj
- Add svm-toy-gtk
- Add svm-toy-qt

* Thu Dec 20 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-9
- [Bug 254091] Comment 19
- Fix python/Makefile

* Thu Dec 13 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-8
- Fix improper sed.
- Change ldconfig to /sbin/ldconfig
- Add gnuplot dependency for libsvm-python, as tools/easy.py needs it.

* Mon Dec 03 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-7
- [Bug 254091] Review Request: libsvm - A Library for Support Vector Machines (Comment #12)

* Wed Sep 26 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-6
- Add defattr to each subpackage
- Move libsvm.so to libsvm

* Mon Sep 24 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-5
- Split out libsvm-java
- Add libsvm.so

* Thu Aug 30 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-4
- Refined description.
- Fix the /tmp/python.ver problem

* Mon Aug 27 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-3
- Fix dependency problem

* Mon Aug 27 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-2
- Fix mock error
- Support Python 2.4 and Python 2.5

* Mon Aug 27 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-1
- Fix rpmlint error
- Move python related files to libsvm-python

* Fri Aug 17 2007 Ding-Yi Chen <dchen@redhat.com> - 2.84-0
- initial packaging

## END: Generated by rpmautospec

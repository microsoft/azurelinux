## START: Set by rpmautospec
## (rpmautospec version 0.6.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 13;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# TODO: Algorithms are available for the following, not yet packaged:
# - Ada
# - C#
# - Go
# - JavaScript
# - Pascal
# - Rust

%global giturl  https://github.com/snowballstem/snowball

Name:           snowball
Version:        2.2.0
Release:        %autorelease
Summary:        Snowball compiler and stemming algorithms

License:        BSD-3-Clause
URL:            https://snowballstem.org/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/v%{version}/%{name}-%{version}.tar.gz
# Test data for the compiler
Source1:        https://github.com/snowballstem/snowball-data/archive/refs/heads/master.zip
# Build a shared library instead of a static library
Patch:          %{name}-sharedlib.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  %{py3_dist docutils}
BuildRequires:  %{py3_dist pygments}

# Java dependencies
%ifarch %{java_arches}
BuildRequires:  java-devel
BuildRequires:  javapackages-tools
%endif

# Python dependencies
BuildRequires:  python3-devel

%global desc %{expand:Snowball is a small string processing language for creating stemming
algorithms for use in Information Retrieval, plus a collection of
stemming algorithms implemented using it.

Snowball was originally designed and built by Martin Porter.  Martin
retired from development in 2014 and Snowball is now maintained as a
community project.  Martin originally chose the name Snowball as a
tribute to SNOBOL, the excellent string handling language from the
1960s.  It now also serves as a metaphor for how the project grows by
gathering contributions over time.}

%global langlist %{expand:Algorithms are available for the following languages:
- Arabic
- Armenian
- Basque
- Catalan
- Danish
- Dutch
- English (Standard, Porter)
- Finnish
- French
- German
- Greek
- Hindi
- Hungarian
- Indonesian
- Irish
- Italian
- Lithuanian
- Nepali
- Norwegian
- Portuguese
- Romanian
- Russian
- Serbian
- Spanish
- Swedish
- Tamil
- Turkish
- Yiddish}

%description
%desc

The Snowball compiler translates a Snowball program into source code in
another language - currently Ada, ISO C, C#, Go, Java, Javascript,
Object Pascal, Python and Rust are supported.

What is Stemming?

Stemming maps different forms of the same word to a common "stem" - for
example, the English stemmer maps connection, connections, connective,
connected, and connecting to connect.  So a search for connected would
also find documents which only have the other forms.

This stem form is often a word itself, but this is not always the case
as this is not a requirement for text search systems, which are the
intended field of use.  We also aim to conflate words with the same
meaning, rather than all words with a common linguistic root (so awe and
awful don't have the same stem), and over-stemming is more problematic
than under-stemming so we tend not to stem in cases that are hard to
resolve.  If you want to always reduce words to a root form and/or get a
root form which is itself a word then Snowball's stemming algorithms
likely aren't the right answer.

%package     -n libstemmer
Summary:        Stemming algorithms written in C

%description -n libstemmer
Stemming algorithms written in C.

%desc

%langlist

%package     -n libstemmer-devel
Summary:        Developer files for libstemmer
Requires:       libstemmer%{?_isa} = %{version}-%{release}

%description -n libstemmer-devel
Header files and shared library links for libstemmer.

%ifarch %{java_arches}
%package     -n snowball-java
Summary:        Stemming algorithms written in Java
BuildArch:      noarch

%description -n snowball-java
Stemming algorithms written in Java.

%desc

%langlist
%endif

%package     -n python3-snowballstemmer
Summary:        Stemming algorithms written in Python 3
BuildArch:      noarch

%description -n python3-snowballstemmer
Stemming algorithms written in Python 3.

%desc

%langlist

%prep
%autosetup -p1 -b 1

# Fix an RST error
sed -i 's/\(libstemmer_c-\)\*/\1\\*/' doc/libstemmer_c_README

%generate_buildrequires
cd python
rm -f modules.txt README.rst src
ln -s ../libstemmer/modules.txt .
ln -s ../README.rst .
ln -s . src
%pyproject_buildrequires

%build
# Build the compiler and C library
sed -i 's|^\(CFLAGS=\).*|\1%{build_cflags}|' GNUmakefile
%make_build

%ifarch %{java_arches}
# Build the Java algorithms
%make_build dist_libstemmer_java
cd dist
tar xf libstemmer_java-%{version}.tar.*
cd -
cd dist/libstemmer_java-%{version}
mkdir classes
javac -d classes java/org/tartarus/snowball/{,ext/}*.java
jar -c -f snowball.jar -C classes org/
cd -
%endif

# Build the python algorithms
%make_build dist_libstemmer_python
cd dist
tar xf snowballstemmer-%{version}.tar.*
cd -
cd dist/snowballstemmer-%{version}
%pyproject_wheel
cd -

# Convert the RST docs to HTML for readability
rst2html --no-datestamp README.rst README.html
rst2html --no-datestamp doc/libstemmer_c_README libstemmer/README.html
rst2html --no-datestamp doc/libstemmer_java_README java/README.html
rst2html --no-datestamp doc/libstemmer_python_README python/README.html

%install
# Install the snowball compiler
mkdir -p %{buildroot}%{_bindir}
cp -p snowball stemwords %{buildroot}%{_bindir}

# Install the C library
mkdir -p %{buildroot}%{_libdir}
cp -p libstemmer.so.0.0.0 %{buildroot}%{_libdir}
ln -s libstemmer.so.0.0.0 %{buildroot}%{_libdir}/libstemmer.so.0
ln -s libstemmer.so.0 %{buildroot}%{_libdir}/libstemmer.so

# Install the C headers
mkdir -p %{buildroot}%{_includedir}
cp -p include/*.h %{buildroot}%{_includedir}

%ifarch %{java_arches}
# Install the Java algorithms
cd dist/libstemmer_java-%{version}
mkdir -p %{buildroot}%{_javadir}
cp -p snowball.jar %{buildroot}%{_javadir}
cd -
%endif

# Install the python algorithms
cd dist/snowballstemmer-%{version}
%pyproject_install
%pyproject_save_files snowballstemmer
cd -

%check
# Check the compiler
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
mv ../snowball-data-master ../snowball-data
make check
%ifarch %{java_arches}
make check_java
%endif
make check_python

%files
%doc NEWS README.html
%license COPYING
%{_bindir}/snowball
%{_bindir}/stemwords

%files -n libstemmer
%doc libstemmer/README.html
%license COPYING
%{_libdir}/libstemmer.so.0*

%files -n libstemmer-devel
%doc examples/stemwords.c
%{_includedir}/libstemmer.h
%{_libdir}/libstemmer.so

%ifarch %{java_arches}
%files -n snowball-java
%doc java/README.html
%license COPYING
%{_javadir}/snowball.jar
%endif

%files -n python3-snowballstemmer -f %{pyproject_files}
%doc python/README.html
%license COPYING

%changelog
## START: Generated by rpmautospec
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jerry James <loganjerry@gmail.com> - 2.2.0-12
- Add VCS field

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.2.0-11
- Rebuilt for Python 3.13

* Mon Feb 12 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.2.0-8
- Handle %generate_buildrequires differences between dnf and dnf5

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.2.0-6
- Rebuilt for Python 3.12

* Mon Feb 27 2023 Jerry James <loganjerry@gmail.com> - 2.2.0-5
- Dynamically generate python BuildRequires

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 26 2022 Jerry James <loganjerry@gmail.com> - 2.2.0-4
- Add BR on javapackages-tools for Java arches
- Run the Java and python tests

* Wed Sep 21 2022 Jerry James <loganjerry@gmail.com> - 2.2.0-3
- Initial RPM, from the libstemmer and python-snowballstemmer packages

## END: Generated by rpmautospec

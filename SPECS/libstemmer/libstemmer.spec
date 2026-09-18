%global snowball_data_commit 381b447563f9bef87b218ebbedde3159afdc3032

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libstemmer
Version:        3.0.1
Release:        1%{?dist}
Summary:        C stemming algorithm library
URL:            https://snowballstem.org/
License:        BSD-3-Clause

Source0:        https://github.com/snowballstem/snowball/archive/refs/tags/v%{version}.tar.gz#/snowball-%{version}.tar.gz
# Test data for the compiler.
Source1:        https://github.com/snowballstem/snowball-data/archive/%{snowball_data_commit}.zip#/snowball-data-%{version}.zip

Patch0:         snowball-sharedlib.patch

BuildRequires:  gcc
BuildRequires:  perl
BuildRequires:  make
BuildRequires:  unzip

%description
Snowball stemming algorithms for use in Information Retrieval Snowball 
provides access to efficient algorithms for calculating a "stemmed" 
form of a word.  This is a form with most of the common morphological 
endings removed; hopefully representing a common linguistic base form.  
This is most useful in building search engines and information 
retrieval software; for example, a search with stemming enabled should 
be able to find a document containing "cycling" given the query 
"cycles".

Snowball provides algorithms for several (mainly European) languages. 
It also provides access to the classic Porter stemming algorithm for 
English: although this has been superseded by an improved algorithm, 
the original algorithm may be of interest to information retrieval 
researchers wishing to reproduce results of earlier experiments.


%package devel
Summary:	C stemming algorithm library developer files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files of libstemmer.

Snowball stemming algorithms for use in Information Retrieval Snowball 
provides access to efficient algorithms for calculating a "stemmed" 
form of a word.  This is a form with most of the common morphological 
endings removed; hopefully representing a common linguistic base form.  
This is most useful in building search engines and information 
retrieval software; for example, a search with stemming enabled should 
be able to find a document containing "cycling" given the query 
"cycles".

Snowball provides algorithms for several (mainly European) languages. 
It also provides access to the classic Porter stemming algorithm for 
English: although this has been superseded by an improved algorithm, 
the original algorithm may be of interest to information retrieval 
researchers wishing to reproduce results of earlier experiments.


%prep
%autosetup -n snowball-%{version}
# Extract and rename the test data archive so %check can find it at ../snowball-data
cd ..
unzip %{SOURCE1}
mv snowball-data-%{snowball_data_commit} snowball-data
cd snowball-%{version}

%build
make libstemmer.so %{?_smp_mflags} CFLAGS="%{optflags} -fPIC -Iinclude" LDFLAGS="$RPM_LD_FLAGS"

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install -p -D -m 755	libstemmer.so.0.0.0	%{buildroot}%{_libdir}/
ln -s libstemmer.so.0.0.0	%{buildroot}%{_libdir}/libstemmer.so.0
ln -s libstemmer.so.0.0.0	%{buildroot}%{_libdir}/libstemmer.so
install -p -D -m 644	include/*	%{buildroot}%{_includedir}/

%ldconfig_scriptlets

%check
# Check the compiler
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
make check

%files
%license COPYING
%doc README.rst
%{_libdir}/libstemmer.so.*

%files devel
%{_libdir}/libstemmer.so
%{_includedir}/*

%changelog
* Tue Jun 30 2026 Lynsey Rydberg <lyrydber@microsoft.com> - 3.0.1-1
- Update to upstream version 3.0.1 using the snowballstem/snowball source.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-14.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-13.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-12.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-11.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Marek Skalický <mskalick@redhat.com> - 0-10.585svn
- Use LDFLAGS for building

* Tue Feb 27 2018 Marek Skalický <mskalick@redhat.com> - 0-9.585svn
- Add missing BuildRequires: gcc/gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-8.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-7.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-6.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-5.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-4.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-3.585svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 6 2015 Marek Skalicky <mskalick@redhat.com> - 0-2.585svn
- Removed undefined-non-weak-symbol warnings

* Tue Dec 2 2014 Marek Skalicky <mskalick@redhat.com> - 0-1.585svn
- Initial packaging

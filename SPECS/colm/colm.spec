Name:           colm
# note that ragel (ragel.spec) depends on a very specific version of colm
# => ragel version must be upgraded when upgrading colm
Version:        0.14.7
Release:        1%{?dist}
Summary:        Programming language designed for the analysis of computer languages
# aapl/ and some headers from src/ are the LGPLv2+
License:        MIT AND LGPLv2+
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.colm.net/open-source/colm/
Source0:        https://github.com/adrian-thurston/colm/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         Colm-NoStatic.patch

BuildRequires:  asciidoc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

# Unfortunately, upstream doesn't exist and not possible to find version
Provides:       bundled(aapl)

%description
Colm is a programming language designed for the analysis and transformation
of computer languages. Colm is influenced primarily by TXL. It is
in the family of program transformation languages.

%package devel
Summary:        Development libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1
# Do not pollute with docs
sed -i -e "/dist_doc_DATA/d" Makefile.am

%build
./autogen.sh
./configure --prefix=%{buildroot}/usr --disable-static
make %{?_smp_mflags}

%install
make install
# do not install/remove .la files and doc files
rm -rf %{buildroot}%{_datadir}
find %{buildroot}%{_libdir} -type f -name '*.la' -print -delete
install -p -m 0644 -D %{name}.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/%{name}.vim
install -p -m 0644 -D ./src/cgil/*.lm %{buildroot}%{_datadir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README
%{_bindir}/*
%{_libdir}/lib%{name}-%{version}.so
%{_libdir}/libfsm-%{version}.so
%dir %{_datadir}/vim
%dir %{_datadir}/vim/vimfiles
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/%{name}.vim

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/libfsm.so
%{_includedir}/
%{_datadir}/*.lm

%changelog
* Wed Jan 19 2022 Nicolas Guibourge <nicolasg@microsft.com> - 0.14.7-1
- Ugradte to 0.14.7

* Wed Oct 27 2021 Muhammad Falak <mwani@microsft.com> - 0.13.0.7-4
- Remove epoch

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.13.0.7-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jul 28 2019 Christian Glombek <lorbus@fedoraproject.org> - 0.13.0.7-1
- Updated to version 0.13.0.7

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Christian Glombek <lorbus@fedoraproject.org> - 0.13.0.6-1
- Updated to version 0.13.0.6

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Jason Taylor <jtfas90@gmail.com> - 0.13.0.5-1
- Upstream bugfix release
- Correction to spec license add MIT license
- Added asciidoc BuildRequires and docdir files

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.13.0.4-1
- Initial package

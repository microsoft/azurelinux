Summary:        A fast, simple LZW file compressor
Name:           ncompress
Version:        5.0
Release:        1%{?dist}
License:        Unlicense
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/vapier/ncompress
#Source0:       https://github.com/vapier/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make

%description

This is (N)compress. It is an improved version of compress 4.1.

Compress is a fast, simple LZW file compressor. Compress does not have the highest compression rate,
but it is one of the fastest programs to compress data. Compress is the defacto standard in the UNIX
community for compressing files. (N)compress 4.2 introduced a special, fast compression hash algorithm.
This algorithm uses more memory than the old hash table. If you don't want the faster hash table algorithm
et 'Memory free for compress' below 800000. Starting with compress 3.0, the output format changed in a
backwards incompatible way. This is not a big deal as compress 3.0 was first released in Jan 1985, while
the first release of compress was available less than a year prior. There shouldn't be any need to produce
files that only older versions of compress would accept. Newer versions of compress are still able to 
handle the output of older versions though -- i.e. compress 3.0+ is able to decompress files produced
by compress 2.0 and older.

%prep
%autosetup

%build
%make_build

%install
make PREFIX=%{_prefix} DESTDIR=%{buildroot} install_core

# %%check
# As of v5.0, this package does not have a test section

%files
%defattr(-,root,root)
%license UNLICENSE LZW.INFO
%{_bindir}/compress
%{_bindir}/uncompress
%{_mandir}/man1/*

%changelog
* Mon May 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 5.0-1
- Original version for CBL-Mariner

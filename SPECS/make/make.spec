Summary:	Program for compiling packages
Name:		make
Version:	4.2.1
Release:        4%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/make
Group:		Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.bz2
%define sha1 make=7d9d11eb36cfb752da1fb11bb3e521d2a3cc8830

%description
The Make package contains a program for compiling packages.

%prep
%setup -q
%build
#work around an error caused by glibc-2.27
sed -i '211,217 d; 219,229 d; 232 d' glob/glob.c

./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%find_lang %{name}

%check
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_includedir}/gnumake.h
%{_mandir}/*/*

%changelog
* Sat May 09 00:21:04 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.2.1-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.2.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 4.2.1-2
- Fix compilation issue against glibc-2.27
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.2.1-1
- Update package version
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 4.1-4
- Modified check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1-3
- GA - Bump release of all rpms
* Tue May 10 2016 Kumar Kaushik <kaushikk@vmware.com>  4.1-2
- Fix for segfaults in chroot env.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  4.1-1
- Update version.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.0-1
- Initial build. First version

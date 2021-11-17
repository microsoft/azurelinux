Summary:        A macro processor
Name:           m4
Version:        1.4.18
Release:        5%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/m4
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://ftp.gnu.org/gnu/m4/%{name}-%{version}.tar.gz
Patch0:         04-fix-sigstksz.patch
Patch1:         m4-1.4.18-glibc-change-work-around.patch

%description
The M4 package contains a macro processor

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%check
sed -i -e '41s/ENOENT/& || errno == EINVAL/' tests/test-readlink.h
make  %{?_smp_mflags}  check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Thu Oct 21 2021 Andrew Phelps <anphel@microsoft.com> 1.4.18-5
- Add patches for glibc 2.34
- License verified
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.4.18-4
- Added %%license line automatically
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.4.18-3
- Initial CBL-Mariner import from Photon (license: Apache2).
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4.18-2
- Fix compilation issue against glibc-2.28
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 1.4.18-1
- Update package version
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 1.4.17-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.17-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.17-1
- Initial build. First version

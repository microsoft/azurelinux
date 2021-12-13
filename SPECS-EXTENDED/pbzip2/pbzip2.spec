Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		pbzip2
Version:	1.1.13
Release:	3%{?dist}
Summary:	Parallel implementation of bzip2
URL:		https://launchpad.net/pbzip2
License:	BSD
BuildRequires:	gcc-c++
BuildRequires:	bzip2-devel
Source0:	https://launchpad.net/pbzip2/1.1/%{version}/+download/pbzip2-%{version}.tar.gz
Patch0:		%{name}-1.1.12-buildflags.patch

%description
PBZIP2 is a parallel implementation of the bzip2 block-sorting file
compressor that uses pthreads and achieves near-linear speedup on SMP
machines.  The output of this version is fully compatible with bzip2
v1.0.2 or newer (ie: anything compressed with pbzip2 can be 
decompressed with bzip2).


%prep
%autosetup -p1
f=AUTHORS; iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 && mv $f.utf8 $f


%build
%set_build_flags
%make_build


%install
install -D -m755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
ln -sf ./%{name} %{buildroot}%{_bindir}/pbunzip2
ln -sf ./%{name} %{buildroot}%{_bindir}/pbzcat



%files
%doc AUTHORS ChangeLog README
%license COPYING
%{_bindir}/%{name}
%{_bindir}/pbunzip2
%{_bindir}/pbzcat
%{_mandir}/man1/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.13-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Filipe Rosset <rosset.filipe@gmail.com> - 1.1.13-1
- update to 1.1.13 + spec cleanup and modernization fixes rhbz#1297158

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 14 2015 Adam Tkac <vonsch@gmail.com> - 1.1.12-1
- update to 1.1.12

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.1.6-7
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  1 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.1.6-1
- Update to 1.1.6.
- Build with %%{?__global_ldflags} and %%{?_smp_mflags}.
- Fix some rpmlint warnings.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Apr 17 2010 Jeff Gilchrist <pbzip2@compression.ca> - 1.1.1-1
- Release 1.1.1

* Sat Mar 13 2010 Jeff Gilchrist <pbzip2@compression.ca> - 1.1.0-1
- Release 1.1.0

* Fri Jan 8 2009 Jeff Gilchrist <pbzip2@compression.ca> - 1.0.5-1
- Release 1.0.5

* Fri Dec 21 2008 Jeff Gilchrist <pbzip2@compression.ca> - 1.0.4-1
- Release 1.0.4

* Tue Oct 31 2008 Jeff Gilchrist <pbzip2@compression.ca> - 1.0.3-1
- Release 1.0.3
- Added support for SUSE RPM build
- Added symlink for pbzcat

* Thu Jul 26 2007 Jeff Gilchrist <pbzip2@compression.ca> - 1.0.2-2
- Fixed symbolic link for pbunzip2 file

* Tue Jul 25 2007 Jeff Gilchrist <pbzip2@compression.ca> - 1.0.2-1
- Release 1.0.2

* Tue Mar 20 2007 Jeff Gilchrist <pbzip2@compression.ca> - 1.0.1-1
- Release 1.0.1

* Wed Mar 14 2007 Jeff Gilchrist <pbzip2@compression.ca> - 1.0-1
- Release 1.0

* Tue Sep 12 2006 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.6-4
- Rebuild for Fedora Extras 6

* Tue May 23 2006 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.6-3
- Added support for $RPM_OPT_FLAGS thanks to Ville Skytta

* Tue Feb 28 2006 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.6-2
- Rebuild for Fedora Extras 5

* Sun Feb 5 2006 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.6-1
- Release 0.9.6

* Sat Dec 31 2005 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.5-1
- Release 0.9.5

* Tue Aug 30 2005 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.4-1
- Updated RPM spec with suggestions from Oliver Falk

* Fri Jul 29 2005 Bryan Stillwell <bryan@bokeoa.com> - 0.9.3-1
- Release 0.9.3
- Removed non-packaging changelog info
- Added dist macro to release field
- Clean buildroot at the beginning of the install section
- Modified buildroot tag to match with Fedora PackagingGuidelines
- Shortened Requires and BuildRequires list
- Changed description to match with the Debian package

* Sat Mar 12 2005 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.2-1
- Release 0.9.2

* Sat Jan 29 2005 Jeff Gilchrist <pbzip2@compression.ca> - 0.9.1-1
- Release 0.9.1

* Sun Jan 24 2005 Jeff Gilchrist <pbzip2@compression.ca> - 0.9-1
- Release 0.9

* Sun Jan 9 2005 Jeff Gilchrist <pbzip2@compression.ca> - 0.8.3-1
- Release 0.8.3

* Mon Nov 30 2004 Jeff Gilchrist <pbzip2@compression.ca> - 0.8.2-1
- Release 0.8.2

* Sat Nov 27 2004 Jeff Gilchrist <pbzip2@compression.ca> - 0.8.1-1
- Release 0.8.1

* Thu Oct 28 2004 Bryan Stillwell <bryan@bokeoa.com> - 0.8-1
- Initial packaging

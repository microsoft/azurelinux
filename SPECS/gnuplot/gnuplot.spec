Summary:        Gnuplot is a portable command-line driven graphing utility.
Name:           gnuplot
Version:        5.4.8
Release:        1%{?dist}
License:        Gnuplot
URL:            http://www.gnuplot.info/
Group:          Applications
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

%description
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. The source code is copyrighted but freely distributed (i.e., you don't have to pay for it). It was originally created to allow scientists and students to visualize mathematical functions and data interactively, but has grown to support many non-interactive uses such as web scripting. It is also used as a plotting engine by third-party applications like Octave. Gnuplot has been supported and under active development since 1986.

%prep
%setup -q

%build
%configure \
    --disable-static \
    --enable-shared
make

%check
make check

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license Copyright
%{_bindir}/*
%{_datadir}/*


%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.4.8-1
- Auto-upgrade to 5.4.8 - Azure Linux 3.0 - package upgrades

* Tue Feb 15 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.4.3-1
- Update source to 5.4.3

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 5.2.4-5
- Remove unused `%%define sha1` lines
- License verified (corrected from Freeware to Gnuplot)

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.2.4-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 5.2.4-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Nov 25 2018 Ashwin H <ashwinh@vmware.com> - 5.2.4-2
- Fix %%check

* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> - 5.2.4-1
- Update version to 5.2.4

* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> - 5.0.6-1
- Update version to 5.0.6

* Tue Nov 29 2016 Xiaolin Li <xiaolinl@vmware.com> - 5.0.5-1
- Add gnuplot 5.0.5 package.

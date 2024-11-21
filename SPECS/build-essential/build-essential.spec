Summary:        Metapackage to install all build tools
Name:           build-essential
Version:        3.0
Release:        1%{?dist}
License:        GPLv2
Requires:       autoconf
Requires:       automake
Requires:       binutils
Requires:       bison
Requires:       diffutils
Requires:       file
Requires:       gawk
Requires:       gcc
Requires:       glibc-devel
Requires:       gzip
Requires:       installkernel
Requires:       kernel-headers
Requires:       libtool
Requires:       make
Requires:       patch
Requires:       pkgconf
Requires:       tar

%description
Metapackage to install all build tools

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
* Thu Dec 21 2023 Muhammad Falak <mwani@microsoft.com> - 3.0-1
- Bump version to 3.0
- Add file, gzip, pkgconf & tar

* Wed Mar 30 2022 Chris Co <chrco@microsoft.com> - 0.1-5
- Add installkernel
- License verified

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.1-4
- Renaming linux-api-headers to kernel-headers.
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Dec 07 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> - 0.1-3
- Add patch and bison

* Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> - 0.1-2
- Added diffutils

* Fri Aug 5 2016 Dheeraj Shetty <dheerajs@vmware.com> - 0.1-1
- Initial

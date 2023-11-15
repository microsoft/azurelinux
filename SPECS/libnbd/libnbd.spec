# The source directory.
%global source_directory 1.12-stable
Summary:        NBD client library in userspace
Name:           libnbd
Version:        1.12.1
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.com/nbdkit/libnbd
Source0:        https://libguestfs.org/download/libnbd/%{source_directory}/%{name}-%{version}.tar.gz
Patch0:         CVE-2023-5215.patch
# For the core library.
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  /usr/bin/pod2man
BuildRequires:  gnutls-devel
BuildRequires:  libxml2-devel

# For nbdfuse.
BuildRequires:  fuse3, fuse3-devel

# For the Python 3 bindings.
BuildRequires:  python3-devel

# For the OCaml bindings.
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc

# Only for building the examples.
BuildRequires:  glib2-devel

# For bash-completion.
BuildRequires:  bash-completion

%if %{with_check}
BuildRequires:  coreutils
BuildRequires:  gcc-c++
BuildRequires:  gnutls-utils
BuildRequires:  iproute
BuildRequires:  jq
BuildRequires:  nbd
BuildRequires:  qemu-img
BuildRequires:  util-linux
%endif

%description
NBD — Network Block Device — is a protocol for accessing Block Devices
(hard disks and disk-like things) over a Network.

This is the NBD client library in userspace, a simple library for
writing NBD clients.

The key features are:

 * Synchronous and asynchronous APIs, both for ease of use and for
   writing non-blocking, multithreaded clients.

 * High performance.

 * Minimal dependencies for the basic library.

 * Well-documented, stable API.

 * Bindings in several programming languages.

%package        devel
Summary:        Development headers for %{name}
License:        LGPLv2+ and BSD
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development headers for %{name}.

%package -n     ocaml-%{name}
Summary:        OCaml language bindings for %{name}
Requires:       %{name} = %{version}-%{release}

%description -n ocaml-%{name}
This package contains OCaml language bindings for %{name}.

%package -n     ocaml-%{name}-devel
Summary:        OCaml language development package for %{name}
License:        LGPLv2+ and BSD
Requires:       ocaml-%{name} = %{version}-%{release}

%description -n ocaml-%{name}-devel
This package contains OCaml language development package for
%{name}.  Install this if you want to compile OCaml software which
uses %{name}.

%package -n     python3-%{name}
Summary:        Python 3 bindings for %{name}
Requires:       %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

# The Python module happens to be called lib*.so.  Don't scan it and
# have a bogus "Provides: libnbdmod.*".
%global __provides_exclude_from ^%{python3_sitearch}/lib.*\\.so

%description -n python3-%{name}
python3-%{name} contains Python 3 bindings for %{name}.

%package -n     nbdfuse
Summary:        FUSE support for %{name}
License:        LGPLv2+ and BSD
Requires:       %{name} = %{version}-%{release}
Recommends:     fuse3

%description -n nbdfuse
This package contains FUSE support for %{name}.

%package        bash-completion
Summary:       Bash tab-completion for %{name}
BuildArch:     noarch
Requires:      bash-completion >= 2.0
Requires:      %{name} = %{version}-%{release}

%description bash-completion
Install this package if you want intelligent bash tab-completion
for %{name}.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --with-tls-priority=@LIBNBD,SYSTEM \
    PYTHON=%{__python3} \
    --enable-python \
    --enable-ocaml \
    --enable-fuse \
    --disable-golang
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.la' -print -delete

# Delete the golang man page since we're not distributing the bindings.
rm %{buildroot}%{_mandir}/man3/libnbd-golang.3*

%check
function skip_test ()
{
    for f in "$@"; do
        rm -f "$f"
        echo 'exit 77' > "$f"
        chmod +x "$f"
    done
}

# All fuse tests fail in Koji with:
# fusermount: entry for fuse/test-*.d not found in /etc/mtab
# for unknown reasons but probably related to the Koji environment.
skip_test fuse/test-*.sh

# IPv6 loopback connections fail in Koji.
make -C tests connect-tcp6 ||:
skip_test tests/connect-tcp6

%make_build check || {
    for f in $(find -name test-suite.log); do
        echo
        echo "==== $f ===="
        cat $f
    done
    exit 1
  }


%files
%doc README
%license COPYING.LIB
%{_bindir}/nbdcopy
%{_bindir}/nbdinfo
%{_libdir}/libnbd.so.*
%{_mandir}/man1/nbdcopy.1*
%{_mandir}/man1/nbdinfo.1*

%files devel
%doc TODO examples/*.c
%license examples/LICENSE-FOR-EXAMPLES
%{_includedir}/libnbd.h
%{_libdir}/libnbd.so
%{_libdir}/pkgconfig/libnbd.pc
%{_mandir}/man3/libnbd.3*
%{_mandir}/man1/libnbd-release-notes-1.*.1*
%{_mandir}/man3/libnbd-security.3*
%{_mandir}/man3/nbd_*.3*

%files -n ocaml-%{name}
%{_libdir}/ocaml/nbd
%exclude %{_libdir}/ocaml/nbd/*.a
%exclude %{_libdir}/ocaml/nbd/*.cmxa
%exclude %{_libdir}/ocaml/nbd/*.cmx
%exclude %{_libdir}/ocaml/nbd/*.mli
%{_libdir}/ocaml/stublibs/dllmlnbd.so
%{_libdir}/ocaml/stublibs/dllmlnbd.so.owner

%files -n ocaml-%{name}-devel
%doc ocaml/examples/*.ml
%license ocaml/examples/LICENSE-FOR-EXAMPLES
%{_libdir}/ocaml/nbd/*.a
%{_libdir}/ocaml/nbd/*.cmxa
%{_libdir}/ocaml/nbd/*.cmx
%{_libdir}/ocaml/nbd/*.mli
%{_mandir}/man3/libnbd-ocaml.3*
%{_mandir}/man3/NBD.3*
%{_mandir}/man3/NBD.*.3*

%files -n python3-%{name}
%{python3_sitearch}/libnbdmod*.so
%{python3_sitearch}/nbd.py
%{python3_sitearch}/nbdsh.py
%{python3_sitearch}/__pycache__/nbd*.py*
%{_bindir}/nbdsh
%{_mandir}/man1/nbdsh.1*

%files -n nbdfuse
%{_bindir}/nbdfuse
%{_mandir}/man1/nbdfuse.1*

%files bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/nbdcopy
%{_datadir}/bash-completion/completions/nbdfuse
%{_datadir}/bash-completion/completions/nbdinfo
%{_datadir}/bash-completion/completions/nbdsh


%changelog
* Thu Oct 19 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 1.12.1-3
- Add patch to fix CVE-2023-5215

* Fri Jul 15 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.12.1-2
- Promote to Mariner base repo
- Lint spec

* Fri Mar 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.1-1
- Updating to version 1.12.1 using Fedora 36 spec (license: MIT) for guidance.

* Fri Jan 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.6-3
- Removing in-spec verification of source tarballs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.6-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Mar 31 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-1
- New upstream development version 1.3.6.
- Golang bindings are contained in this release but not distributed.

* Wed Mar 11 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.5-2
- Fix bogus runtime Requires of new bash-completion package.

* Tue Mar 10 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.5-1
- New upstream development version 1.3.5.
- Add new bash-completion subpackage.

* Sat Feb 29 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.4-1
- New upstream development version 1.3.4.

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2.2
- Bump release and rebuild.

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2
- OCaml 4.10.0 final.

* Wed Feb 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-1
- New upstream development version 1.3.3.

* Thu Jan 30 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.2-1
- New upstream development version 1.3.2.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-4
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-3
- OCaml 4.10.0+beta1 rebuild.

* Thu Dec 12 2019 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-2
- Rebuild for OCaml 4.09.0.

* Tue Dec 03 2019 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- New upstream development version 1.3.1.

* Wed Nov 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-2
- Use gpgverify macro instead of explicit gpgv2 command.

* Thu Nov 14 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-1
- New stable release 1.2.0

* Sat Nov 09 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.9-1
- New upstream version 1.1.9.
- Add new nbdkit-release-notes-1.2(1) man page.

* Wed Nov 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.8-1
- New upstream version 1.1.8.

* Thu Oct 24 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-1
- New upstream version 1.1.7.

* Sat Oct 19 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-1
- New upstream version 1.1.6.

* Sat Oct 12 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-1
- New upstream version 1.1.5.
- New tool and subpackage nbdfuse.

* Wed Oct  9 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.4-1
- New upstream version 1.1.4.
- Contains fix for remote code execution vulnerability.
- Add new libnbd-security(3) man page.

* Tue Oct  1 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-1
- New upstream version 1.1.3.

* Tue Sep 17 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- New upstream version 1.1.2.
- Remove patches which are upstream.
- Contains fix for NBD Protocol Downgrade Attack (CVE-2019-14842).

* Thu Sep 12 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-2
- Add upstream patch to fix nbdsh (for nbdkit tests).

* Sun Sep 08 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-1
- New development version 1.1.1.

* Wed Aug 28 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-1
- New upstream version 1.0.0.

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.9-2
- Rebuilt for Python 3.8

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 0.9.9-1
- New upstream version 0.9.9.

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-4
- Fix nbdkit dependencies so we're actually running the tests.
- Add glib2-devel BR so we build the glib main loop example.
- Add upstream patch to fix test error:
  nbd_connect_unix: getlogin: No such device or address
- Fix test failure on 32 bit.

* Tue Aug 20 2019 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-3
- Bump and rebuild to fix releng brokenness.
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/2LIDI33G3IEIPYSCCIP6WWKNHY7XZJGQ/

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.8-2
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-1
- New upstream version 0.9.8.
- Package the new nbd_*(3) man pages.

* Mon Aug  5 2019 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-1
- New upstream version 0.9.7.
- Add libnbd-ocaml(3) man page.

* Sat Aug  3 2019 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-2
- Add all upstream patches since 0.9.6 was released.
- Package the ocaml bindings into a subpackage.

* Tue Jul 30 2019 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-1
- New upstream verison 0.9.6.

* Fri Jul 26 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.9-1
- New upstream version 0.1.9.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.8-1
- New upstream version 0.1.8.

* Tue Jul 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.7-1
- New upstream version 0.1.7.

* Wed Jul  3 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.6-1
- New upstream version 0.1.6.

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.5-1
- New upstream version 0.1.5.

* Sun Jun 09 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.4-1
- New upstream version 0.1.4.

* Sun Jun  2 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.2-2
- Enable libxml2 for NBD URI support.

* Thu May 30 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.2-1
- New upstream version 0.1.2.

* Tue May 28 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1.1-1
- Fix license in man pages and examples.
- Add nbdsh(1) man page.
- Include the signature and keyring even if validation is disabled.
- Update devel subpackage license.
- Fix old FSF address in Python tests.
- Filter Python provides.
- Remove executable permission on the tar.gz.sig file.
- Initial release.

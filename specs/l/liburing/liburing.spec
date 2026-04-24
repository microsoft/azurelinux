# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: liburing
Version: 2.12
Release: 2%{?dist}
Summary: Linux-native io_uring I/O access library
License: (GPL-2.0-only WITH Linux-syscall-note OR MIT) AND (LGPL-2.0-or-later OR MIT)
Source0: https://brick.kernel.dk/snaps/%{name}-%{version}.tar.gz
Source1: https://brick.kernel.dk/snaps/%{name}-%{version}.tar.gz.asc
URL: https://git.kernel.dk/cgit/liburing/
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make

%description
Provides native async IO for the Linux kernel, in a fast and efficient
manner, for both buffered and O_DIRECT.

%package devel
Summary: Development files for Linux-native io_uring I/O access library
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package provides header files to include and libraries to link with
for the Linux-native io_uring.

%prep
%autosetup -p1

%build
%set_build_flags
./configure --prefix=%{_prefix} --libdir=/%{_libdir} --libdevdir=/%{_libdir} --mandir=%{_mandir} --includedir=%{_includedir} --use-libc

%make_build

%install
%make_install

%files
%{_libdir}/liburing.so.*
%{_libdir}/liburing-ffi.so.*
%license COPYING

%files devel
%{_includedir}/liburing/
%{_includedir}/liburing.h
%{_libdir}/liburing.so
%{_libdir}/liburing-ffi.so
%exclude %{_libdir}/liburing.a
%exclude %{_libdir}/liburing-ffi.a
%{_libdir}/pkgconfig/*
%{_mandir}/man2/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Tue Sep 16 2025 Davide Cavalca <dcavalca@fedoraproject.org> - 2.12-1
- Update to liburing 2.12 (RHBZ#2369233)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 04 2025 Stefan Hajnoczi <stefanha@redhat.com> - 2.9-1
- Update to liburing 2.9 (RHBZ#2343530)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 30 2024 Richard W.M. Jones <rjones@redhat.com> - 2.8-1
- Update to liburing 2.8 (RHBZ#2317177)
- Remove explicit %%attr on library

* Thu Aug 22 2024 Richard W.M. Jones <rjones@redhat.com> - 2.7-1
- Update to liburing 2.7 (RHBZ#2307229)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 07 2024 Richard W.M. Jones <rjones@redhat.com> - 2.6-1
- Update to liburing 2.6 (RHBZ#2213893)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 23 2023 Stefan Hajnoczi <stefanha@redhat.com> - 2.5-1
- Update to liburing 2.5.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 20 2023 Stefan Hajnoczi <stefanha@redhat.com> - 2.4-2
- Fix i686 build failure due to nolibc conflict with stack protector.

* Tue Jun 20 2023 Stefan Hajnoczi <stefanha@redhat.com> - 2.4-1
- Update to liburing 2.4.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 9 2022 Stefan Hajnoczi <stefanha@redhat.com> - 2.3-1
- Update to liburing 2.3.

* Mon Aug 22 2022 Richard W.M. Jones <rjones@redhat.com> - 2.2-1
- Update to liburing 2.2.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 13 2021 Stefan Hajnoczi <stefanha@redhat.com> - 2.0-1
- Update to liburing 2.0. This release is source-compatible with 0.7 but
  applications must be recompiled since <liburing.h> struct sizes have changed.
- Add man3 and man7 documentation

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 19 2020 Davide Cavalca <dcavalca@fb.com> - 0.7-3
- Drop exclude for armv7hl as it's no longer necessary

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Stefan Hajnoczi <stefanha@redhat.com> - 0.7-1
- Add io_uring_cq_eventfd_toggle() helper for new IORING_CQ_EVENTFD_DISABLED flag
- Add IORING_OP_TEE
- Documentation fixes and improvements

* Thu May 7 2020 Stefan Hajnoczi <stefanha@redhat.com> - 0.6-1
- add io_uring_prep_splice()
- add io_uring_prep_provide_buffers()
- add io_uring_prep_remove_buffers()
- add io_uring_register_eventfd_async()
- reinstate io_uring_unregister_eventfd() (it was accidentally removed in 0.4)

* Thu Mar 19 2020 Stefan Hajnoczi <stefanha@redhat.com> - 0.5-1
- Update license to GPL-2.0 OR MIT
- Add io_uring_prep_epoll_ctl()
- Add io_uring_get_probe(), io_uring_get_probe_ring()
- Add io_uring_register_probe()
- Add io_uring_{register,unregister}_personality()
- Add io_uring_prep_{recv,send}()
- Add io_uring_prep_openat2()
- Add io_uring_ring_dontfork()
- Add io_uring_prep_read() and io_uring_prep_write()
- Documentation fixes and improvements

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 7 2020 Stefan Hajnoczi <stefanha@redhat.com> - 0.3-1
- Add IORING_OP_STATX
- Add IORING_OP_OPENAT/IORING_OP_CLOSE helpers
- Add prep helpers for IORING_OP_FILES_UPDATE and IORING_OP_FALLOCATE
- Add io_uring_prep_connect() helper
- Add io_uring_wait_cqe_nr()
- Add IORING_OP_ASYNC_CANCEL and prep helper

* Thu Oct 31 2019 Jeff Moyer <jmoyer@redhat.com> - 0.2-1
- Add io_uring_cq_ready()
- Add io_uring_peek_batch_cqe()
- Add io_uring_prep_accept()
- Add io_uring_prep_{recv,send}msg()
- Add io_uring_prep_timeout_remove()
- Add io_uring_queue_init_params()
- Add io_uring_register_files_update()
- Add io_uring_sq_space_left()
- Add io_uring_wait_cqe_timeout()
- Add io_uring_wait_cqes()
- Add io_uring_wait_cqes_timeout()

* Tue Jan 8 2019 Jens Axboe <axboe@kernel.dk> - 0.1
- Initial version

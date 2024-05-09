Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Spanish man pages from the Linux Documentation Project
Name: man-pages-es
Version: 1.55
Release: 34%{?dist}
# FIXME: a more complete audit of the various licenses should really be done
# These man pages come under various copyrights.
# All are freely distributable when the nroff source is included.
License: GPL+ and GPLv2+ and LDP and IEEE
URL: https://ditec.um.es/~piernas/manpages-es/
%global extra_name %{name}-extra
%global extra_ver 0.8a
%global extra_pkg_name %{extra_name}-%{extra_ver}
%global es_man_dir %{_mandir}/es
Source0: https://ditec.um.es/~piernas/manpages-es/%{name}-%{version}.tar.bz2
Source1: https://ditec.um.es/~piernas/manpages-es/%{extra_pkg_name}.tar.gz

BuildArch: noarch
Summary(es): Páginas de manual en español

Requires: man-pages-reader
Supplements: (man-pages and langpacks-es)




%description
This package contains the translation into Spanish of the English
man-pages package. It is a beta release, so you can still find a lot
of bugs.  Contributions are welcome. For any doubt or suggestion about
this release, send an e-mail to Juan Piernas Canovas <piernas at
ditec.um.es>. In order to collaborate with the project, please visit
https://es.tldp.org.

%description -l es
Este archivo contiene la traducción al español del paquete man-pages
en inglés. Es una versión beta, por lo que todavía puede encontrar
bastantes errores. Cualquier contribución será bienvenida. Para
cualquier duda o sugerencia sobre esta versión, envíe un correo a Juan
Piernas Cánovas (piernas en ditec.um.es). Si desea colaborar en el
proyecto, por favor, visite https://es.tldp.org.


%package extra
Summary: Extra manual pages - Spanish versions
Requires: %{name} = %{version}-%{release}
Summary(es): Páginas de manual extras en castellano.

%description extra
This package contains the eighth release of the Linux extra man pages
in Spanish. Note it is an alpha release, so you can find a lot of bugs.
These man pages are from several packages and applications. See PAQUETES
file for more information about packages.

%description extra -l es
Esta paquete contiene la octava versión de páginas de manual extras
en español para Linux. Note que es una versión alfa, por lo que puede
encontrar bastantes errores. Estas páginas proceden de distintos paquetes y
aplicaciones. Consulte el fichero PAQUETES para conocer dichos paquetes.


%prep
%setup -q -a 1

for i in README LEEME.extra PAQUETES PROYECTO; do
    iconv -f ISO8859-15 -t UTF-8 %{extra_pkg_name}/$i -o %{extra_pkg_name}/$i.utf8
    mv  %{extra_pkg_name}/$i.utf8 %{extra_pkg_name}/$i
done
mv %{extra_pkg_name}/README %{extra_pkg_name}/README.extra

# Bug 388391
rm -f %{extra_pkg_name}/man1/mc.1
rm -f %{extra_pkg_name}/man1/newgrp.1
# Bug 226124
for i in man3/dlopen.3 man5/acct.5 man5/host.conf.5 man5/resolver.5 man8/ld.so.8; do
    iconv -f UTF-8 -t UTF-8 $i -o $i.utf8
    mv $i.utf8 $i
    rm -f %{extra_pkg_name}/$i
done

for i in man-pages-1.55.Announce man7/iso_8859-7.7; do
    iconv -f ISO8859-15 -t UTF-8 $i -o $i.utf8
    mv $i.utf8 $i
done

for j in 1 1x 2 3 4 5 6 7 8 9; do
    for i in `find %{extra_pkg_name} -type f -name \*.$j`; do
        iconv -f ISO8859-15 -t UTF-8 $i -o $i.utf8
        mv $i.utf8 $i
    done
done

# Remove non-free man-pages
rm ./man2/sysinfo.2
rm ./man2/getitimer.2

%build

%install
make install MANDIR=$RPM_BUILD_ROOT%{es_man_dir}
make -C %{extra_pkg_name} MANDIR=$RPM_BUILD_ROOT%{es_man_dir}
rm -f $RPM_BUILD_ROOT%{es_man_dir}/LEEME.extra
rm -f $RPM_BUILD_ROOT%{es_man_dir}/PAQUETES
rm -f $RPM_BUILD_ROOT%{es_man_dir}/PROYECTO
#[Bug 427684] man-pages fileconflict
#- Fix the conflict with vipw.8 (in shadow-utils)
rm -f $RPM_BUILD_ROOT%{es_man_dir}/man8/vipw.8
#[Bug 487941]File conflict between man-pages-es-extra and shadow-utils
rm -f $RPM_BUILD_ROOT%{es_man_dir}/man8/vigr.8

%files
%doc LEEME man-pages-1.55.Announce README CHANGES-1.28-1.55 CAMBIOS-1.28-1.55
%{es_man_dir}/man1/chgrp.1.gz
%{es_man_dir}/man1/chmod.1.gz
%{es_man_dir}/man1/chown.1.gz
%{es_man_dir}/man1/cp.1.gz
%{es_man_dir}/man1/dd.1.gz
%{es_man_dir}/man1/df.1.gz
%{es_man_dir}/man1/diff.1.gz
%{es_man_dir}/man1/dir.1.gz
%{es_man_dir}/man1/dircolors.1.gz
%{es_man_dir}/man1/du.1.gz
%{es_man_dir}/man1/install.1.gz
%{es_man_dir}/man1/intro.1.gz
%{es_man_dir}/man1/ldd.1.gz
%{es_man_dir}/man1/LEAME.gz
%{es_man_dir}/man1/ln.1.gz
%{es_man_dir}/man1/ls.1.gz
%{es_man_dir}/man1/mkdir.1.gz
%{es_man_dir}/man1/mkfifo.1.gz
%{es_man_dir}/man1/mknod.1.gz
%{es_man_dir}/man1/mv.1.gz
%{es_man_dir}/man1/rm.1.gz
%{es_man_dir}/man1/rmdir.1.gz
%{es_man_dir}/man1/time.1.gz
%{es_man_dir}/man1/touch.1.gz
%{es_man_dir}/man1/vdir.1.gz
%{es_man_dir}/man2/accept.2.gz
%{es_man_dir}/man2/access.2.gz
%{es_man_dir}/man2/acct.2.gz
%{es_man_dir}/man2/adjtimex.2.gz
%{es_man_dir}/man2/afs_syscall.2.gz
%{es_man_dir}/man2/alarm.2.gz
%{es_man_dir}/man2/alloc_hugepages.2.gz
%{es_man_dir}/man2/arch_prctl.2.gz
%{es_man_dir}/man2/bdflush.2.gz
%{es_man_dir}/man2/bind.2.gz
%{es_man_dir}/man2/break.2.gz
%{es_man_dir}/man2/brk.2.gz
%{es_man_dir}/man2/cacheflush.2.gz
%{es_man_dir}/man2/capget.2.gz
%{es_man_dir}/man2/capset.2.gz
%{es_man_dir}/man2/chdir.2.gz
%{es_man_dir}/man2/chmod.2.gz
%{es_man_dir}/man2/chown.2.gz
%{es_man_dir}/man2/chroot.2.gz
%{es_man_dir}/man2/clone.2.gz
%{es_man_dir}/man2/close.2.gz
%{es_man_dir}/man2/connect.2.gz
%{es_man_dir}/man2/creat.2.gz
%{es_man_dir}/man2/dup.2.gz
%{es_man_dir}/man2/dup2.2.gz
%{es_man_dir}/man2/execve.2.gz
%{es_man_dir}/man2/_exit.2.gz
%{es_man_dir}/man2/exit.2.gz
%{es_man_dir}/man2/_Exit.2.gz
%{es_man_dir}/man2/fchdir.2.gz
%{es_man_dir}/man2/fchmod.2.gz
%{es_man_dir}/man2/fchown.2.gz
%{es_man_dir}/man2/fcntl.2.gz
%{es_man_dir}/man2/fdatasync.2.gz
%{es_man_dir}/man2/flock.2.gz
%{es_man_dir}/man2/fork.2.gz
%{es_man_dir}/man2/free_hugepages.2.gz
%{es_man_dir}/man2/fstat.2.gz
%{es_man_dir}/man2/fstatfs.2.gz
%{es_man_dir}/man2/fsync.2.gz
%{es_man_dir}/man2/ftruncate.2.gz
%{es_man_dir}/man2/futex.2.gz
%{es_man_dir}/man2/getcontext.2.gz
%{es_man_dir}/man2/getdents.2.gz
%{es_man_dir}/man2/getdomainname.2.gz
%{es_man_dir}/man2/getdtablesize.2.gz
%{es_man_dir}/man2/getegid.2.gz
%{es_man_dir}/man2/geteuid.2.gz
%{es_man_dir}/man2/getgid.2.gz
%{es_man_dir}/man2/getgroups.2.gz
%{es_man_dir}/man2/gethostid.2.gz
%{es_man_dir}/man2/gethostname.2.gz
%{es_man_dir}/man2/getpagesize.2.gz
%{es_man_dir}/man2/getpeername.2.gz
%{es_man_dir}/man2/getpgid.2.gz
%{es_man_dir}/man2/getpgrp.2.gz
%{es_man_dir}/man2/getpid.2.gz
%{es_man_dir}/man2/getppid.2.gz
%{es_man_dir}/man2/getpriority.2.gz
%{es_man_dir}/man2/getresgid.2.gz
%{es_man_dir}/man2/getresuid.2.gz
%{es_man_dir}/man2/getrlimit.2.gz
%{es_man_dir}/man2/getrusage.2.gz
%{es_man_dir}/man2/getsid.2.gz
%{es_man_dir}/man2/getsockname.2.gz
%{es_man_dir}/man2/getsockopt.2.gz
%{es_man_dir}/man2/gettid.2.gz
%{es_man_dir}/man2/gettimeofday.2.gz
%{es_man_dir}/man2/getuid.2.gz
%{es_man_dir}/man2/gtty.2.gz
%{es_man_dir}/man2/idle.2.gz
%{es_man_dir}/man2/inb.2.gz
%{es_man_dir}/man2/inb_p.2.gz
%{es_man_dir}/man2/inl.2.gz
%{es_man_dir}/man2/inl_p.2.gz
%{es_man_dir}/man2/insb.2.gz
%{es_man_dir}/man2/insl.2.gz
%{es_man_dir}/man2/insw.2.gz
%{es_man_dir}/man2/intro.2.gz
%{es_man_dir}/man2/inw.2.gz
%{es_man_dir}/man2/inw_p.2.gz
%{es_man_dir}/man2/ioctl.2.gz
%{es_man_dir}/man2/ioctl_list.2.gz
%{es_man_dir}/man2/ioperm.2.gz
%{es_man_dir}/man2/iopl.2.gz
%{es_man_dir}/man2/ipc.2.gz
%{es_man_dir}/man2/kill.2.gz
%{es_man_dir}/man2/killpg.2.gz
%{es_man_dir}/man2/lchown.2.gz
%{es_man_dir}/man2/link.2.gz
%{es_man_dir}/man2/listen.2.gz
%{es_man_dir}/man2/_llseek.2.gz
%{es_man_dir}/man2/llseek.2.gz
%{es_man_dir}/man2/lock.2.gz
%{es_man_dir}/man2/lseek.2.gz
%{es_man_dir}/man2/lstat.2.gz
%{es_man_dir}/man2/madvise.2.gz
%{es_man_dir}/man2/mincore.2.gz
%{es_man_dir}/man2/mkdir.2.gz
%{es_man_dir}/man2/mknod.2.gz
%{es_man_dir}/man2/mlock.2.gz
%{es_man_dir}/man2/mlockall.2.gz
%{es_man_dir}/man2/mmap.2.gz
%{es_man_dir}/man2/mmap2.2.gz
%{es_man_dir}/man2/modify_ldt.2.gz
%{es_man_dir}/man2/mount.2.gz
%{es_man_dir}/man2/mprotect.2.gz
%{es_man_dir}/man2/mpx.2.gz
%{es_man_dir}/man2/mremap.2.gz
%{es_man_dir}/man2/msgctl.2.gz
%{es_man_dir}/man2/msgget.2.gz
%{es_man_dir}/man2/msgop.2.gz
%{es_man_dir}/man2/msgrcv.2.gz
%{es_man_dir}/man2/msgsnd.2.gz
%{es_man_dir}/man2/msync.2.gz
%{es_man_dir}/man2/munlock.2.gz
%{es_man_dir}/man2/munlockall.2.gz
%{es_man_dir}/man2/munmap.2.gz
%{es_man_dir}/man2/nanosleep.2.gz
%{es_man_dir}/man2/_newselect.2.gz
%{es_man_dir}/man2/nfsservctl.2.gz
%{es_man_dir}/man2/nice.2.gz
%{es_man_dir}/man2/obsolete.2.gz
%{es_man_dir}/man2/oldfstat.2.gz
%{es_man_dir}/man2/oldlstat.2.gz
%{es_man_dir}/man2/oldolduname.2.gz
%{es_man_dir}/man2/oldstat.2.gz
%{es_man_dir}/man2/olduname.2.gz
%{es_man_dir}/man2/open.2.gz
%{es_man_dir}/man2/outb.2.gz
%{es_man_dir}/man2/outb_p.2.gz
%{es_man_dir}/man2/outl.2.gz
%{es_man_dir}/man2/outl_p.2.gz
%{es_man_dir}/man2/outsb.2.gz
%{es_man_dir}/man2/outsl.2.gz
%{es_man_dir}/man2/outsw.2.gz
%{es_man_dir}/man2/outw.2.gz
%{es_man_dir}/man2/outw_p.2.gz
%{es_man_dir}/man2/pause.2.gz
%{es_man_dir}/man2/personality.2.gz
%{es_man_dir}/man2/pipe.2.gz
%{es_man_dir}/man2/pivot_root.2.gz
%{es_man_dir}/man2/poll.2.gz
%{es_man_dir}/man2/prctl.2.gz
%{es_man_dir}/man2/pread.2.gz
%{es_man_dir}/man2/prof.2.gz
%{es_man_dir}/man2/pselect.2.gz
%{es_man_dir}/man2/ptrace.2.gz
%{es_man_dir}/man2/pwrite.2.gz
%{es_man_dir}/man2/quotactl.2.gz
%{es_man_dir}/man2/read.2.gz
%{es_man_dir}/man2/readdir.2.gz
%{es_man_dir}/man2/readlink.2.gz
%{es_man_dir}/man2/readv.2.gz
%{es_man_dir}/man2/reboot.2.gz
%{es_man_dir}/man2/recv.2.gz
%{es_man_dir}/man2/recvfrom.2.gz
%{es_man_dir}/man2/recvmsg.2.gz
%{es_man_dir}/man2/rename.2.gz
%{es_man_dir}/man2/rmdir.2.gz
%{es_man_dir}/man2/sbrk.2.gz
%{es_man_dir}/man2/sched_getaffinity.2.gz
%{es_man_dir}/man2/sched_getparam.2.gz
%{es_man_dir}/man2/sched_get_priority_max.2.gz
%{es_man_dir}/man2/sched_get_priority_min.2.gz
%{es_man_dir}/man2/sched_getscheduler.2.gz
%{es_man_dir}/man2/sched_rr_get_interval.2.gz
%{es_man_dir}/man2/sched_setaffinity.2.gz
%{es_man_dir}/man2/sched_setparam.2.gz
%{es_man_dir}/man2/sched_setscheduler.2.gz
%{es_man_dir}/man2/sched_yield.2.gz
%{es_man_dir}/man2/select.2.gz
%{es_man_dir}/man2/select_tut.2.gz
%{es_man_dir}/man2/semctl.2.gz
%{es_man_dir}/man2/semget.2.gz
%{es_man_dir}/man2/semop.2.gz
%{es_man_dir}/man2/send.2.gz
%{es_man_dir}/man2/sendfile.2.gz
%{es_man_dir}/man2/sendmsg.2.gz
%{es_man_dir}/man2/sendto.2.gz
%{es_man_dir}/man2/setcontext.2.gz
%{es_man_dir}/man2/setdomainname.2.gz
%{es_man_dir}/man2/setegid.2.gz
%{es_man_dir}/man2/seteuid.2.gz
%{es_man_dir}/man2/setfsgid.2.gz
%{es_man_dir}/man2/setfsuid.2.gz
%{es_man_dir}/man2/setgid.2.gz
%{es_man_dir}/man2/setgroups.2.gz
%{es_man_dir}/man2/sethostid.2.gz
%{es_man_dir}/man2/sethostname.2.gz
%{es_man_dir}/man2/setitimer.2.gz
%{es_man_dir}/man2/setpgid.2.gz
%{es_man_dir}/man2/setpgrp.2.gz
%{es_man_dir}/man2/setpriority.2.gz
%{es_man_dir}/man2/setregid.2.gz
%{es_man_dir}/man2/setresgid.2.gz
%{es_man_dir}/man2/setresuid.2.gz
%{es_man_dir}/man2/setreuid.2.gz
%{es_man_dir}/man2/setrlimit.2.gz
%{es_man_dir}/man2/setsid.2.gz
%{es_man_dir}/man2/setsockopt.2.gz
%{es_man_dir}/man2/settimeofday.2.gz
%{es_man_dir}/man2/setuid.2.gz
%{es_man_dir}/man2/setup.2.gz
%{es_man_dir}/man2/sgetmask.2.gz
%{es_man_dir}/man2/shmat.2.gz
%{es_man_dir}/man2/shmctl.2.gz
%{es_man_dir}/man2/shmdt.2.gz
%{es_man_dir}/man2/shmget.2.gz
%{es_man_dir}/man2/shmop.2.gz
%{es_man_dir}/man2/shutdown.2.gz
%{es_man_dir}/man2/sigaction.2.gz
%{es_man_dir}/man2/sigaltstack.2.gz
%{es_man_dir}/man2/sigblock.2.gz
%{es_man_dir}/man2/siggetmask.2.gz
%{es_man_dir}/man2/sigmask.2.gz
%{es_man_dir}/man2/signal.2.gz
%{es_man_dir}/man2/sigpause.2.gz
%{es_man_dir}/man2/sigpending.2.gz
%{es_man_dir}/man2/sigprocmask.2.gz
%{es_man_dir}/man2/sigqueue.2.gz
%{es_man_dir}/man2/sigreturn.2.gz
%{es_man_dir}/man2/sigsetmask.2.gz
%{es_man_dir}/man2/sigsuspend.2.gz
%{es_man_dir}/man2/sigtimedwait.2.gz
%{es_man_dir}/man2/sigvec.2.gz
%{es_man_dir}/man2/sigwaitinfo.2.gz
%{es_man_dir}/man2/socket.2.gz
%{es_man_dir}/man2/socketcall.2.gz
%{es_man_dir}/man2/socketpair.2.gz
%{es_man_dir}/man2/ssetmask.2.gz
%{es_man_dir}/man2/stat.2.gz
%{es_man_dir}/man2/statfs.2.gz
%{es_man_dir}/man2/stime.2.gz
%{es_man_dir}/man2/stty.2.gz
%{es_man_dir}/man2/swapoff.2.gz
%{es_man_dir}/man2/swapon.2.gz
%{es_man_dir}/man2/symlink.2.gz
%{es_man_dir}/man2/sync.2.gz
%{es_man_dir}/man2/syscall.2.gz
%{es_man_dir}/man2/syscalls.2.gz
%{es_man_dir}/man2/_sysctl.2.gz
%{es_man_dir}/man2/sysctl.2.gz
%{es_man_dir}/man2/sysfs.2.gz
%{es_man_dir}/man2/syslog.2.gz
%{es_man_dir}/man2/time.2.gz
%{es_man_dir}/man2/times.2.gz
%{es_man_dir}/man2/tkill.2.gz
%{es_man_dir}/man2/truncate.2.gz
%{es_man_dir}/man2/umask.2.gz
%{es_man_dir}/man2/umount.2.gz
%{es_man_dir}/man2/umount2.2.gz
%{es_man_dir}/man2/uname.2.gz
%{es_man_dir}/man2/undocumented.2.gz
%{es_man_dir}/man2/unimplemented.2.gz
%{es_man_dir}/man2/unlink.2.gz
%{es_man_dir}/man2/uselib.2.gz
%{es_man_dir}/man2/ustat.2.gz
%{es_man_dir}/man2/utime.2.gz
%{es_man_dir}/man2/utimes.2.gz
%{es_man_dir}/man2/vfork.2.gz
%{es_man_dir}/man2/vhangup.2.gz
%{es_man_dir}/man2/vm86.2.gz
%{es_man_dir}/man2/wait.2.gz
%{es_man_dir}/man2/wait3.2.gz
%{es_man_dir}/man2/wait4.2.gz
%{es_man_dir}/man2/waitpid.2.gz
%{es_man_dir}/man2/write.2.gz
%{es_man_dir}/man2/writev.2.gz
%{es_man_dir}/man3/a64l.3.gz
%{es_man_dir}/man3/abort.3.gz
%{es_man_dir}/man3/abs.3.gz
%{es_man_dir}/man3/acos.3.gz
%{es_man_dir}/man3/acosh.3.gz
%{es_man_dir}/man3/addmntent.3.gz
%{es_man_dir}/man3/alloca.3.gz
%{es_man_dir}/man3/alphasort.3.gz
%{es_man_dir}/man3/argz_add.3.gz
%{es_man_dir}/man3/argz_add_sep.3.gz
%{es_man_dir}/man3/argz_append.3.gz
%{es_man_dir}/man3/argz_count.3.gz
%{es_man_dir}/man3/argz_create.3.gz
%{es_man_dir}/man3/argz_create_sep.3.gz
%{es_man_dir}/man3/argz_delete.3.gz
%{es_man_dir}/man3/argz_extract.3.gz
%{es_man_dir}/man3/argz_insert.3.gz
%{es_man_dir}/man3/argz_next.3.gz
%{es_man_dir}/man3/argz_replace.3.gz
%{es_man_dir}/man3/argz_stringify.3.gz
%{es_man_dir}/man3/asctime.3.gz
%{es_man_dir}/man3/asin.3.gz
%{es_man_dir}/man3/asinh.3.gz
%{es_man_dir}/man3/asprintf.3.gz
%{es_man_dir}/man3/assert.3.gz
%{es_man_dir}/man3/assert_perror.3.gz
%{es_man_dir}/man3/atan2.3.gz
%{es_man_dir}/man3/atan.3.gz
%{es_man_dir}/man3/atanh.3.gz
%{es_man_dir}/man3/atexit.3.gz
%{es_man_dir}/man3/atof.3.gz
%{es_man_dir}/man3/atoi.3.gz
%{es_man_dir}/man3/atol.3.gz
%{es_man_dir}/man3/atoll.3.gz
%{es_man_dir}/man3/atoq.3.gz
%{es_man_dir}/man3/auth_destroy.3.gz
%{es_man_dir}/man3/authnone_create.3.gz
%{es_man_dir}/man3/authunix_create.3.gz
%{es_man_dir}/man3/authunix_create_default.3.gz
%{es_man_dir}/man3/basename.3.gz
%{es_man_dir}/man3/bcmp.3.gz
%{es_man_dir}/man3/bcopy.3.gz
%{es_man_dir}/man3/bindresvport.3.gz
%{es_man_dir}/man3/bsearch.3.gz
%{es_man_dir}/man3/bstring.3.gz
%{es_man_dir}/man3/btowc.3.gz
%{es_man_dir}/man3/btree.3.gz
%{es_man_dir}/man3/byteorder.3.gz
%{es_man_dir}/man3/bzero.3.gz
%{es_man_dir}/man3/calloc.3.gz
%{es_man_dir}/man3/callrpc.3.gz
%{es_man_dir}/man3/catclose.3.gz
%{es_man_dir}/man3/catgets.3.gz
%{es_man_dir}/man3/catopen.3.gz
%{es_man_dir}/man3/cbrt.3.gz
%{es_man_dir}/man3/ceil.3.gz
%{es_man_dir}/man3/ceilf.3.gz
%{es_man_dir}/man3/ceill.3.gz
%{es_man_dir}/man3/cfgetispeed.3.gz
%{es_man_dir}/man3/cfgetospeed.3.gz
%{es_man_dir}/man3/cfmakeraw.3.gz
%{es_man_dir}/man3/cfsetispeed.3.gz
%{es_man_dir}/man3/cfsetospeed.3.gz
%{es_man_dir}/man3/clearenv.3.gz
%{es_man_dir}/man3/clearerr.3.gz
%{es_man_dir}/man3/clearerr_unlocked.3.gz
%{es_man_dir}/man3/clnt_broadcast.3.gz
%{es_man_dir}/man3/clnt_call.3.gz
%{es_man_dir}/man3/clnt_control.3.gz
%{es_man_dir}/man3/clnt_create.3.gz
%{es_man_dir}/man3/clnt_destroy.3.gz
%{es_man_dir}/man3/clnt_freeres.3.gz
%{es_man_dir}/man3/clnt_geterr.3.gz
%{es_man_dir}/man3/clnt_pcreateerror.3.gz
%{es_man_dir}/man3/clnt_perrno.3.gz
%{es_man_dir}/man3/clnt_perror.3.gz
%{es_man_dir}/man3/clntraw_create.3.gz
%{es_man_dir}/man3/clnt_spcreateerror.3.gz
%{es_man_dir}/man3/clnt_sperrno.3.gz
%{es_man_dir}/man3/clnt_sperror.3.gz
%{es_man_dir}/man3/clnttcp_create.3.gz
%{es_man_dir}/man3/clntudp_bufcreate.3.gz
%{es_man_dir}/man3/clntudp_create.3.gz
%{es_man_dir}/man3/clock.3.gz
%{es_man_dir}/man3/closedir.3.gz
%{es_man_dir}/man3/closelog.3.gz
%{es_man_dir}/man3/cmsg.3.gz
%{es_man_dir}/man3/CMSG_ALIGN.3.gz
%{es_man_dir}/man3/CMSG_FIRSTHDR.3.gz
%{es_man_dir}/man3/CMSG_NXTHDR.3.gz
%{es_man_dir}/man3/CMSG_SPACE.3.gz
%{es_man_dir}/man3/confstr.3.gz
%{es_man_dir}/man3/copysign.3.gz
%{es_man_dir}/man3/copysignf.3.gz
%{es_man_dir}/man3/copysignl.3.gz
%{es_man_dir}/man3/cos.3.gz
%{es_man_dir}/man3/cosh.3.gz
%{es_man_dir}/man3/crypt.3.gz
%{es_man_dir}/man3/ctermid.3.gz
%{es_man_dir}/man3/ctime.3.gz
%{es_man_dir}/man3/cuserid.3.gz
%{es_man_dir}/man3/daemon.3.gz
%{es_man_dir}/man3/db.3.gz
%{es_man_dir}/man3/dbopen.3.gz
%{es_man_dir}/man3/difftime.3.gz
%{es_man_dir}/man3/dirfd.3.gz
%{es_man_dir}/man3/dirname.3.gz
%{es_man_dir}/man3/div.3.gz
%{es_man_dir}/man3/dlclose.3.gz
%{es_man_dir}/man3/dlerror.3.gz
%{es_man_dir}/man3/dlopen.3.gz
%{es_man_dir}/man3/dlsym.3.gz
%{es_man_dir}/man3/dn_comp.3.gz
%{es_man_dir}/man3/dn_expand.3.gz
%{es_man_dir}/man3/dprintf.3.gz
%{es_man_dir}/man3/drand48.3.gz
%{es_man_dir}/man3/drem.3.gz
%{es_man_dir}/man3/dysize.3.gz
%{es_man_dir}/man3/ecvt.3.gz
%{es_man_dir}/man3/ecvt_r.3.gz
%{es_man_dir}/man3/encrypt.3.gz
%{es_man_dir}/man3/endfsent.3.gz
%{es_man_dir}/man3/endgrent.3.gz
%{es_man_dir}/man3/endhostent.3.gz
%{es_man_dir}/man3/endmntent.3.gz
%{es_man_dir}/man3/endnetent.3.gz
%{es_man_dir}/man3/endprotoent.3.gz
%{es_man_dir}/man3/endpwent.3.gz
%{es_man_dir}/man3/endrpcent.3.gz
%{es_man_dir}/man3/endservent.3.gz
%{es_man_dir}/man3/endttyent.3.gz
%{es_man_dir}/man3/endusershell.3.gz
%{es_man_dir}/man3/endutent.3.gz
%{es_man_dir}/man3/endutxent.3.gz
%{es_man_dir}/man3/envz_add.3.gz
%{es_man_dir}/man3/envz_entry.3.gz
%{es_man_dir}/man3/envz_get.3.gz
%{es_man_dir}/man3/envz_merge.3.gz
%{es_man_dir}/man3/envz_remove.3.gz
%{es_man_dir}/man3/envz_strip.3.gz
%{es_man_dir}/man3/erand48.3.gz
%{es_man_dir}/man3/erf.3.gz
%{es_man_dir}/man3/erfc.3.gz
%{es_man_dir}/man3/err.3.gz
%{es_man_dir}/man3/errno.3.gz
%{es_man_dir}/man3/errx.3.gz
%{es_man_dir}/man3/ether_aton.3.gz
%{es_man_dir}/man3/ether_aton_r.3.gz
%{es_man_dir}/man3/ether_hostton.3.gz
%{es_man_dir}/man3/ether_line.3.gz
%{es_man_dir}/man3/ether_ntoa.3.gz
%{es_man_dir}/man3/ether_ntoa_r.3.gz
%{es_man_dir}/man3/ether_ntohost.3.gz
%{es_man_dir}/man3/exec.3.gz
%{es_man_dir}/man3/execl.3.gz
%{es_man_dir}/man3/execle.3.gz
%{es_man_dir}/man3/execlp.3.gz
%{es_man_dir}/man3/execv.3.gz
%{es_man_dir}/man3/execvp.3.gz
%{es_man_dir}/man3/exit.3.gz
%{es_man_dir}/man3/exp.3.gz
%{es_man_dir}/man3/expm1.3.gz
%{es_man_dir}/man3/fabs.3.gz
%{es_man_dir}/man3/fabsf.3.gz
%{es_man_dir}/man3/fabsl.3.gz
%{es_man_dir}/man3/__fbufsize.3.gz
%{es_man_dir}/man3/fclose.3.gz
%{es_man_dir}/man3/fcloseall.3.gz
%{es_man_dir}/man3/fcvt.3.gz
%{es_man_dir}/man3/fcvt_r.3.gz
%{es_man_dir}/man3/fdopen.3.gz
%{es_man_dir}/man3/feclearexcept.3.gz
%{es_man_dir}/man3/fegetenv.3.gz
%{es_man_dir}/man3/fegetexceptflag.3.gz
%{es_man_dir}/man3/fegetround.3.gz
%{es_man_dir}/man3/feholdexcept.3.gz
%{es_man_dir}/man3/fenv.3.gz
%{es_man_dir}/man3/feof.3.gz
%{es_man_dir}/man3/feof_unlocked.3.gz
%{es_man_dir}/man3/feraiseexcept.3.gz
%{es_man_dir}/man3/ferror.3.gz
%{es_man_dir}/man3/ferror_unlocked.3.gz
%{es_man_dir}/man3/fesetenv.3.gz
%{es_man_dir}/man3/fesetexceptflag.3.gz
%{es_man_dir}/man3/fesetround.3.gz
%{es_man_dir}/man3/fetestexcept.3.gz
%{es_man_dir}/man3/feupdateenv.3.gz
%{es_man_dir}/man3/fflush.3.gz
%{es_man_dir}/man3/fflush_unlocked.3.gz
%{es_man_dir}/man3/ffs.3.gz
%{es_man_dir}/man3/fgetc.3.gz
%{es_man_dir}/man3/fgetc_unlocked.3.gz
%{es_man_dir}/man3/fgetgrent.3.gz
%{es_man_dir}/man3/fgetpos.3.gz
%{es_man_dir}/man3/fgetpwent.3.gz
%{es_man_dir}/man3/fgets.3.gz
%{es_man_dir}/man3/fgets_unlocked.3.gz
%{es_man_dir}/man3/fgetwc.3.gz
%{es_man_dir}/man3/fgetwc_unlocked.3.gz
%{es_man_dir}/man3/fgetws.3.gz
%{es_man_dir}/man3/fgetws_unlocked.3.gz
%{es_man_dir}/man3/fileno.3.gz
%{es_man_dir}/man3/fileno_unlocked.3.gz
%{es_man_dir}/man3/finite.3.gz
%{es_man_dir}/man3/__flbf.3.gz
%{es_man_dir}/man3/flockfile.3.gz
%{es_man_dir}/man3/floor.3.gz
%{es_man_dir}/man3/floorf.3.gz
%{es_man_dir}/man3/floorl.3.gz
%{es_man_dir}/man3/_flushlbf.3.gz
%{es_man_dir}/man3/fmod.3.gz
%{es_man_dir}/man3/fnmatch.3.gz
%{es_man_dir}/man3/fopen.3.gz
%{es_man_dir}/man3/forkpty.3.gz
%{es_man_dir}/man3/fpathconf.3.gz
%{es_man_dir}/man3/__fpending.3.gz
%{es_man_dir}/man3/fprintf.3.gz
%{es_man_dir}/man3/__fpurge.3.gz
%{es_man_dir}/man3/fpurge.3.gz
%{es_man_dir}/man3/fputc.3.gz
%{es_man_dir}/man3/fputc_unlocked.3.gz
%{es_man_dir}/man3/fputs.3.gz
%{es_man_dir}/man3/fputs_unlocked.3.gz
%{es_man_dir}/man3/fputwc.3.gz
%{es_man_dir}/man3/fputwc_unlocked.3.gz
%{es_man_dir}/man3/fputws.3.gz
%{es_man_dir}/man3/fputws_unlocked.3.gz
%{es_man_dir}/man3/fread.3.gz
%{es_man_dir}/man3/__freadable.3.gz
%{es_man_dir}/man3/__freading.3.gz
%{es_man_dir}/man3/fread_unlocked.3.gz
%{es_man_dir}/man3/free.3.gz
%{es_man_dir}/man3/freeaddrinfo.3.gz
%{es_man_dir}/man3/freehostent.3.gz
%{es_man_dir}/man3/freopen.3.gz
%{es_man_dir}/man3/frexp.3.gz
%{es_man_dir}/man3/fscanf.3.gz
%{es_man_dir}/man3/fseek.3.gz
%{es_man_dir}/man3/fseeko.3.gz
%{es_man_dir}/man3/__fsetlocking.3.gz
%{es_man_dir}/man3/fsetpos.3.gz
%{es_man_dir}/man3/ftell.3.gz
%{es_man_dir}/man3/ftello.3.gz
%{es_man_dir}/man3/ftime.3.gz
%{es_man_dir}/man3/ftok.3.gz
%{es_man_dir}/man3/ftrylockfile.3.gz
%{es_man_dir}/man3/fts.3.gz
%{es_man_dir}/man3/fts_children.3.gz
%{es_man_dir}/man3/fts_close.3.gz
%{es_man_dir}/man3/fts_open.3.gz
%{es_man_dir}/man3/fts_read.3.gz
%{es_man_dir}/man3/fts_set.3.gz
%{es_man_dir}/man3/ftw.3.gz
%{es_man_dir}/man3/funlockfile.3.gz
%{es_man_dir}/man3/fwide.3.gz
%{es_man_dir}/man3/fwprintf.3.gz
%{es_man_dir}/man3/__fwritable.3.gz
%{es_man_dir}/man3/fwrite.3.gz
%{es_man_dir}/man3/fwrite_unlocked.3.gz
%{es_man_dir}/man3/__fwriting.3.gz
%{es_man_dir}/man3/gai_strerror.3.gz
%{es_man_dir}/man3/gamma.3.gz
%{es_man_dir}/man3/gammaf.3.gz
%{es_man_dir}/man3/gammal.3.gz
%{es_man_dir}/man3/gcvt.3.gz
%{es_man_dir}/man3/getaddrinfo.3.gz
%{es_man_dir}/man3/getc.3.gz
%{es_man_dir}/man3/getchar.3.gz
%{es_man_dir}/man3/getchar_unlocked.3.gz
%{es_man_dir}/man3/getc_unlocked.3.gz
%{es_man_dir}/man3/get_current_dir_name.3.gz
%{es_man_dir}/man3/getcwd.3.gz
%{es_man_dir}/man3/getdate.3.gz
%{es_man_dir}/man3/getdate_r.3.gz
%{es_man_dir}/man3/getdelim.3.gz
%{es_man_dir}/man3/getdirentries.3.gz
%{es_man_dir}/man3/getenv.3.gz
%{es_man_dir}/man3/getfsent.3.gz
%{es_man_dir}/man3/getfsfile.3.gz
%{es_man_dir}/man3/getfsspec.3.gz
%{es_man_dir}/man3/getgrent.3.gz
%{es_man_dir}/man3/getgrgid.3.gz
%{es_man_dir}/man3/getgrnam.3.gz
%{es_man_dir}/man3/gethostbyaddr.3.gz
%{es_man_dir}/man3/gethostbyname2.3.gz
%{es_man_dir}/man3/gethostbyname2_r.3.gz
%{es_man_dir}/man3/gethostbyname.3.gz
%{es_man_dir}/man3/gethostbyname_r.3.gz
%{es_man_dir}/man3/getipnodebyaddr.3.gz
%{es_man_dir}/man3/getipnodebyname.3.gz
%{es_man_dir}/man3/getline.3.gz
%{es_man_dir}/man3/getloadavg.3.gz
%{es_man_dir}/man3/getlogin.3.gz
%{es_man_dir}/man3/getmntent.3.gz
%{es_man_dir}/man3/get_myaddress.3.gz
%{es_man_dir}/man3/getnameinfo.3.gz
%{es_man_dir}/man3/getnetbyaddr.3.gz
%{es_man_dir}/man3/getnetbyname.3.gz
%{es_man_dir}/man3/getnetent.3.gz
%{es_man_dir}/man3/getopt.3.gz
%{es_man_dir}/man3/getopt_long.3.gz
%{es_man_dir}/man3/getopt_long_only.3.gz
%{es_man_dir}/man3/getpass.3.gz
%{es_man_dir}/man3/getprotobyname.3.gz
%{es_man_dir}/man3/getprotobynumber.3.gz
%{es_man_dir}/man3/getprotoent.3.gz
%{es_man_dir}/man3/getpt.3.gz
%{es_man_dir}/man3/getpw.3.gz
%{es_man_dir}/man3/getpwent.3.gz
%{es_man_dir}/man3/getpwnam.3.gz
%{es_man_dir}/man3/getpwuid.3.gz
%{es_man_dir}/man3/getrpcbyname.3.gz
%{es_man_dir}/man3/getrpcbynumber.3.gz
%{es_man_dir}/man3/getrpcent.3.gz
%{es_man_dir}/man3/getrpcport.3.gz
%{es_man_dir}/man3/gets.3.gz
%{es_man_dir}/man3/getservbyname.3.gz
%{es_man_dir}/man3/getservbyport.3.gz
%{es_man_dir}/man3/getservent.3.gz
%{es_man_dir}/man3/getttyent.3.gz
%{es_man_dir}/man3/getttynam.3.gz
%{es_man_dir}/man3/getumask.3.gz
%{es_man_dir}/man3/getusershell.3.gz
%{es_man_dir}/man3/getutent.3.gz
%{es_man_dir}/man3/getutid.3.gz
%{es_man_dir}/man3/getutline.3.gz
%{es_man_dir}/man3/getutxent.3.gz
%{es_man_dir}/man3/getutxid.3.gz
%{es_man_dir}/man3/getutxline.3.gz
%{es_man_dir}/man3/getw.3.gz
%{es_man_dir}/man3/getwc.3.gz
%{es_man_dir}/man3/getwchar.3.gz
%{es_man_dir}/man3/getwchar_unlocked.3.gz
%{es_man_dir}/man3/getwc_unlocked.3.gz
%{es_man_dir}/man3/getwd.3.gz
%{es_man_dir}/man3/glob.3.gz
%{es_man_dir}/man3/globfree.3.gz
%{es_man_dir}/man3/gmtime.3.gz
%{es_man_dir}/man3/grantpt.3.gz
%{es_man_dir}/man3/gsignal.3.gz
%{es_man_dir}/man3/hash.3.gz
%{es_man_dir}/man3/hasmntopt.3.gz
%{es_man_dir}/man3/hcreate.3.gz
%{es_man_dir}/man3/hcreate_r.3.gz
%{es_man_dir}/man3/hdestroy.3.gz
%{es_man_dir}/man3/hdestroy_r.3.gz
%{es_man_dir}/man3/herror.3.gz
%{es_man_dir}/man3/hsearch.3.gz
%{es_man_dir}/man3/hsearch_r.3.gz
%{es_man_dir}/man3/hstrerror.3.gz
%{es_man_dir}/man3/htonl.3.gz
%{es_man_dir}/man3/htons.3.gz
%{es_man_dir}/man3/hypot.3.gz
%{es_man_dir}/man3/iconv.3.gz
%{es_man_dir}/man3/iconv_close.3.gz
%{es_man_dir}/man3/iconv_open.3.gz
%{es_man_dir}/man3/imaxabs.3.gz
%{es_man_dir}/man3/index.3.gz
%{es_man_dir}/man3/inet.3.gz
%{es_man_dir}/man3/inet_addr.3.gz
%{es_man_dir}/man3/inet_aton.3.gz
%{es_man_dir}/man3/inet_lnaof.3.gz
%{es_man_dir}/man3/inet_makeaddr.3.gz
%{es_man_dir}/man3/inet_netof.3.gz
%{es_man_dir}/man3/inet_network.3.gz
%{es_man_dir}/man3/inet_ntoa.3.gz
%{es_man_dir}/man3/inet_ntop.3.gz
%{es_man_dir}/man3/inet_pton.3.gz
%{es_man_dir}/man3/infnan.3.gz
%{es_man_dir}/man3/initgroups.3.gz
%{es_man_dir}/man3/initstate.3.gz
%{es_man_dir}/man3/insque.3.gz
%{es_man_dir}/man3/intro.3.gz
%{es_man_dir}/man3/iruserok.3.gz
%{es_man_dir}/man3/isalnum.3.gz
%{es_man_dir}/man3/isalpha.3.gz
%{es_man_dir}/man3/isascii.3.gz
%{es_man_dir}/man3/isatty.3.gz
%{es_man_dir}/man3/isblank.3.gz
%{es_man_dir}/man3/iscntrl.3.gz
%{es_man_dir}/man3/isdigit.3.gz
%{es_man_dir}/man3/isgraph.3.gz
%{es_man_dir}/man3/isinf.3.gz
%{es_man_dir}/man3/islower.3.gz
%{es_man_dir}/man3/isnan.3.gz
%{es_man_dir}/man3/isprint.3.gz
%{es_man_dir}/man3/ispunct.3.gz
%{es_man_dir}/man3/isspace.3.gz
%{es_man_dir}/man3/isupper.3.gz
%{es_man_dir}/man3/iswalnum.3.gz
%{es_man_dir}/man3/iswalpha.3.gz
%{es_man_dir}/man3/iswblank.3.gz
%{es_man_dir}/man3/iswcntrl.3.gz
%{es_man_dir}/man3/iswctype.3.gz
%{es_man_dir}/man3/iswdigit.3.gz
%{es_man_dir}/man3/iswgraph.3.gz
%{es_man_dir}/man3/iswlower.3.gz
%{es_man_dir}/man3/iswprint.3.gz
%{es_man_dir}/man3/iswpunct.3.gz
%{es_man_dir}/man3/iswspace.3.gz
%{es_man_dir}/man3/iswupper.3.gz
%{es_man_dir}/man3/iswxdigit.3.gz
%{es_man_dir}/man3/isxdigit.3.gz
%{es_man_dir}/man3/j0.3.gz
%{es_man_dir}/man3/j0f.3.gz
%{es_man_dir}/man3/j0l.3.gz
%{es_man_dir}/man3/j1.3.gz
%{es_man_dir}/man3/j1f.3.gz
%{es_man_dir}/man3/j1l.3.gz
%{es_man_dir}/man3/jn.3.gz
%{es_man_dir}/man3/jnf.3.gz
%{es_man_dir}/man3/jnl.3.gz
%{es_man_dir}/man3/jrand48.3.gz
%{es_man_dir}/man3/key_decryptsession.3.gz
%{es_man_dir}/man3/key_encryptsession.3.gz
%{es_man_dir}/man3/key_gendes.3.gz
%{es_man_dir}/man3/key_secretkey_is_set.3.gz
%{es_man_dir}/man3/key_setsecret.3.gz
%{es_man_dir}/man3/killpg.3.gz
%{es_man_dir}/man3/klogctl.3.gz
%{es_man_dir}/man3/l64a.3.gz
%{es_man_dir}/man3/labs.3.gz
%{es_man_dir}/man3/lcong48.3.gz
%{es_man_dir}/man3/ldexp.3.gz
%{es_man_dir}/man3/ldiv.3.gz
%{es_man_dir}/man3/lfind.3.gz
%{es_man_dir}/man3/lgamma.3.gz
%{es_man_dir}/man3/lgammaf.3.gz
%{es_man_dir}/man3/lgammaf_r.3.gz
%{es_man_dir}/man3/lgammal.3.gz
%{es_man_dir}/man3/lgammal_r.3.gz
%{es_man_dir}/man3/lgamma_r.3.gz
%{es_man_dir}/man3/llabs.3.gz
%{es_man_dir}/man3/lldiv.3.gz
%{es_man_dir}/man3/llrint.3.gz
%{es_man_dir}/man3/llrintf.3.gz
%{es_man_dir}/man3/llrintl.3.gz
%{es_man_dir}/man3/llround.3.gz
%{es_man_dir}/man3/llroundf.3.gz
%{es_man_dir}/man3/llroundl.3.gz
%{es_man_dir}/man3/localeconv.3.gz
%{es_man_dir}/man3/localtime.3.gz
%{es_man_dir}/man3/lockf.3.gz
%{es_man_dir}/man3/log10.3.gz
%{es_man_dir}/man3/log1p.3.gz
%{es_man_dir}/man3/log.3.gz
%{es_man_dir}/man3/login_tty.3.gz
%{es_man_dir}/man3/logwtmp.3.gz
%{es_man_dir}/man3/longjmp.3.gz
%{es_man_dir}/man3/lrand48.3.gz
%{es_man_dir}/man3/lrint.3.gz
%{es_man_dir}/man3/lrintf.3.gz
%{es_man_dir}/man3/lrintl.3.gz
%{es_man_dir}/man3/lround.3.gz
%{es_man_dir}/man3/lroundf.3.gz
%{es_man_dir}/man3/lroundl.3.gz
%{es_man_dir}/man3/lsearch.3.gz
%{es_man_dir}/man3/makecontext.3.gz
%{es_man_dir}/man3/malloc.3.gz
%{es_man_dir}/man3/__malloc_hook.3.gz
%{es_man_dir}/man3/malloc_hook.3.gz
%{es_man_dir}/man3/MB_CUR_MAX.3.gz
%{es_man_dir}/man3/mblen.3.gz
%{es_man_dir}/man3/MB_LEN_MAX.3.gz
%{es_man_dir}/man3/mbrlen.3.gz
%{es_man_dir}/man3/mbrtowc.3.gz
%{es_man_dir}/man3/mbsinit.3.gz
%{es_man_dir}/man3/mbsnrtowcs.3.gz
%{es_man_dir}/man3/mbsrtowcs.3.gz
%{es_man_dir}/man3/mbstowcs.3.gz
%{es_man_dir}/man3/mbtowc.3.gz
%{es_man_dir}/man3/memalign.3.gz
%{es_man_dir}/man3/memccpy.3.gz
%{es_man_dir}/man3/memchr.3.gz
%{es_man_dir}/man3/memcmp.3.gz
%{es_man_dir}/man3/memcpy.3.gz
%{es_man_dir}/man3/memfrob.3.gz
%{es_man_dir}/man3/memmem.3.gz
%{es_man_dir}/man3/memmove.3.gz
%{es_man_dir}/man3/memrchr.3.gz
%{es_man_dir}/man3/memset.3.gz
%{es_man_dir}/man3/mkdtemp.3.gz
%{es_man_dir}/man3/mkfifo.3.gz
%{es_man_dir}/man3/mkstemp.3.gz
%{es_man_dir}/man3/mktemp.3.gz
%{es_man_dir}/man3/mktime.3.gz
%{es_man_dir}/man3/modf.3.gz
%{es_man_dir}/man3/mpool.3.gz
%{es_man_dir}/man3/mrand48.3.gz
%{es_man_dir}/man3/mtrace.3.gz
%{es_man_dir}/man3/muntrace.3.gz
%{es_man_dir}/man3/nan.3.gz
%{es_man_dir}/man3/nanf.3.gz
%{es_man_dir}/man3/nanl.3.gz
%{es_man_dir}/man3/nearbyint.3.gz
%{es_man_dir}/man3/nearbyintf.3.gz
%{es_man_dir}/man3/nearbyintl.3.gz
%{es_man_dir}/man3/netlink.3.gz
%{es_man_dir}/man3/nextafter.3.gz
%{es_man_dir}/man3/nextafterf.3.gz
%{es_man_dir}/man3/nextafterl.3.gz
%{es_man_dir}/man3/nexttoward.3.gz
%{es_man_dir}/man3/nexttowardf.3.gz
%{es_man_dir}/man3/nexttowardl.3.gz
%{es_man_dir}/man3/nftw.3.gz
%{es_man_dir}/man3/nl_langinfo.3.gz
%{es_man_dir}/man3/nrand48.3.gz
%{es_man_dir}/man3/ntohl.3.gz
%{es_man_dir}/man3/ntohs.3.gz
%{es_man_dir}/man3/on_exit.3.gz
%{es_man_dir}/man3/opendir.3.gz
%{es_man_dir}/man3/openlog.3.gz
%{es_man_dir}/man3/openpty.3.gz
%{es_man_dir}/man3/pathconf.3.gz
%{es_man_dir}/man3/pclose.3.gz
%{es_man_dir}/man3/perror.3.gz
%{es_man_dir}/man3/pmap_getmaps.3.gz
%{es_man_dir}/man3/pmap_getport.3.gz
%{es_man_dir}/man3/pmap_rmtcall.3.gz
%{es_man_dir}/man3/pmap_set.3.gz
%{es_man_dir}/man3/pmap_unset.3.gz
%{es_man_dir}/man3/popen.3.gz
%{es_man_dir}/man3/posix_memalign.3.gz
%{es_man_dir}/man3/pow.3.gz
%{es_man_dir}/man3/printf.3.gz
%{es_man_dir}/man3/profil.3.gz
%{es_man_dir}/man3/psignal.3.gz
%{es_man_dir}/man3/ptsname.3.gz
%{es_man_dir}/man3/putc.3.gz
%{es_man_dir}/man3/putchar.3.gz
%{es_man_dir}/man3/putchar_unlocked.3.gz
%{es_man_dir}/man3/putc_unlocked.3.gz
%{es_man_dir}/man3/putenv.3.gz
%{es_man_dir}/man3/putpwent.3.gz
%{es_man_dir}/man3/puts.3.gz
%{es_man_dir}/man3/pututline.3.gz
%{es_man_dir}/man3/pututxline.3.gz
%{es_man_dir}/man3/putw.3.gz
%{es_man_dir}/man3/putwc.3.gz
%{es_man_dir}/man3/putwchar.3.gz
%{es_man_dir}/man3/putwchar_unlocked.3.gz
%{es_man_dir}/man3/putwc_unlocked.3.gz
%{es_man_dir}/man3/qecvt.3.gz
%{es_man_dir}/man3/qecvt_r.3.gz
%{es_man_dir}/man3/qfcvt.3.gz
%{es_man_dir}/man3/qfcvt_r.3.gz
%{es_man_dir}/man3/qgcvt.3.gz
%{es_man_dir}/man3/qsort.3.gz
%{es_man_dir}/man3/queue.3.gz
%{es_man_dir}/man3/raise.3.gz
%{es_man_dir}/man3/rand.3.gz
%{es_man_dir}/man3/random.3.gz
%{es_man_dir}/man3/rcmd.3.gz
%{es_man_dir}/man3/readdir.3.gz
%{es_man_dir}/man3/realloc.3.gz
%{es_man_dir}/man3/realpath.3.gz
%{es_man_dir}/man3/recno.3.gz
%{es_man_dir}/man3/re_comp.3.gz
%{es_man_dir}/man3/re_exec.3.gz
%{es_man_dir}/man3/regcomp.3.gz
%{es_man_dir}/man3/regerror.3.gz
%{es_man_dir}/man3/regex.3.gz
%{es_man_dir}/man3/regexec.3.gz
%{es_man_dir}/man3/regfree.3.gz
%{es_man_dir}/man3/registerrpc.3.gz
%{es_man_dir}/man3/remove.3.gz
%{es_man_dir}/man3/remque.3.gz
%{es_man_dir}/man3/res_init.3.gz
%{es_man_dir}/man3/res_mkquery.3.gz
%{es_man_dir}/man3/resolver.3.gz
%{es_man_dir}/man3/res_query.3.gz
%{es_man_dir}/man3/res_querydomain.3.gz
%{es_man_dir}/man3/res_search.3.gz
%{es_man_dir}/man3/res_send.3.gz
%{es_man_dir}/man3/rewind.3.gz
%{es_man_dir}/man3/rewinddir.3.gz
%{es_man_dir}/man3/rindex.3.gz
%{es_man_dir}/man3/rint.3.gz
%{es_man_dir}/man3/rintf.3.gz
%{es_man_dir}/man3/rintl.3.gz
%{es_man_dir}/man3/round.3.gz
%{es_man_dir}/man3/roundf.3.gz
%{es_man_dir}/man3/roundl.3.gz
%{es_man_dir}/man3/rpc.3.gz
%{es_man_dir}/man3/rresvport.3.gz
%{es_man_dir}/man3/rtnetlink.3.gz
%{es_man_dir}/man3/ruserok.3.gz
%{es_man_dir}/man3/scandir.3.gz
%{es_man_dir}/man3/scanf.3.gz
%{es_man_dir}/man3/seed48.3.gz
%{es_man_dir}/man3/seekdir.3.gz
%{es_man_dir}/man3/setbuf.3.gz
%{es_man_dir}/man3/setbuffer.3.gz
%{es_man_dir}/man3/setenv.3.gz
%{es_man_dir}/man3/__setfpucw.3.gz
%{es_man_dir}/man3/setfsent.3.gz
%{es_man_dir}/man3/setgrent.3.gz
%{es_man_dir}/man3/sethostent.3.gz
%{es_man_dir}/man3/setjmp.3.gz
%{es_man_dir}/man3/setkey.3.gz
%{es_man_dir}/man3/setlinebuf.3.gz
%{es_man_dir}/man3/setlocale.3.gz
%{es_man_dir}/man3/setlogmask.3.gz
%{es_man_dir}/man3/setmntent.3.gz
%{es_man_dir}/man3/setnetent.3.gz
%{es_man_dir}/man3/setprotoent.3.gz
%{es_man_dir}/man3/setpwent.3.gz
%{es_man_dir}/man3/setrpcent.3.gz
%{es_man_dir}/man3/setservent.3.gz
%{es_man_dir}/man3/setstate.3.gz
%{es_man_dir}/man3/setttyent.3.gz
%{es_man_dir}/man3/setusershell.3.gz
%{es_man_dir}/man3/setutent.3.gz
%{es_man_dir}/man3/setutxent.3.gz
%{es_man_dir}/man3/setvbuf.3.gz
%{es_man_dir}/man3/shm_open.3.gz
%{es_man_dir}/man3/sigaddset.3.gz
%{es_man_dir}/man3/sigdelset.3.gz
%{es_man_dir}/man3/sigemptyset.3.gz
%{es_man_dir}/man3/sigfillset.3.gz
%{es_man_dir}/man3/siginterrupt.3.gz
%{es_man_dir}/man3/sigismember.3.gz
%{es_man_dir}/man3/siglongjmp.3.gz
%{es_man_dir}/man3/signbit.3.gz
%{es_man_dir}/man3/sigsetjmp.3.gz
%{es_man_dir}/man3/sigsetops.3.gz
%{es_man_dir}/man3/sin.3.gz
%{es_man_dir}/man3/sinh.3.gz
%{es_man_dir}/man3/sleep.3.gz
%{es_man_dir}/man3/snprintf.3.gz
%{es_man_dir}/man3/sprintf.3.gz
%{es_man_dir}/man3/sqrt.3.gz
%{es_man_dir}/man3/srand.3.gz
%{es_man_dir}/man3/srand48.3.gz
%{es_man_dir}/man3/srandom.3.gz
%{es_man_dir}/man3/sscanf.3.gz
%{es_man_dir}/man3/ssignal.3.gz
%{es_man_dir}/man3/stdarg.3.gz
%{es_man_dir}/man3/stderr.3.gz
%{es_man_dir}/man3/stdin.3.gz
%{es_man_dir}/man3/stdio.3.gz
%{es_man_dir}/man3/stdio_ext.3.gz
%{es_man_dir}/man3/stdout.3.gz
%{es_man_dir}/man3/stpcpy.3.gz
%{es_man_dir}/man3/stpncpy.3.gz
%{es_man_dir}/man3/strcasecmp.3.gz
%{es_man_dir}/man3/strcat.3.gz
%{es_man_dir}/man3/strchr.3.gz
%{es_man_dir}/man3/strcmp.3.gz
%{es_man_dir}/man3/strcoll.3.gz
%{es_man_dir}/man3/strcpy.3.gz
%{es_man_dir}/man3/strcspn.3.gz
%{es_man_dir}/man3/strdup.3.gz
%{es_man_dir}/man3/strdupa.3.gz
%{es_man_dir}/man3/strerror.3.gz
%{es_man_dir}/man3/strerror_r.3.gz
%{es_man_dir}/man3/strfmon.3.gz
%{es_man_dir}/man3/strfry.3.gz
%{es_man_dir}/man3/strftime.3.gz
%{es_man_dir}/man3/string.3.gz
%{es_man_dir}/man3/strlen.3.gz
%{es_man_dir}/man3/strncasecmp.3.gz
%{es_man_dir}/man3/strncat.3.gz
%{es_man_dir}/man3/strncmp.3.gz
%{es_man_dir}/man3/strncpy.3.gz
%{es_man_dir}/man3/strndup.3.gz
%{es_man_dir}/man3/strndupa.3.gz
%{es_man_dir}/man3/strnlen.3.gz
%{es_man_dir}/man3/strpbrk.3.gz
%{es_man_dir}/man3/strptime.3.gz
%{es_man_dir}/man3/strrchr.3.gz
%{es_man_dir}/man3/strsep.3.gz
%{es_man_dir}/man3/strsignal.3.gz
%{es_man_dir}/man3/strspn.3.gz
%{es_man_dir}/man3/strstr.3.gz
%{es_man_dir}/man3/strtod.3.gz
%{es_man_dir}/man3/strtof.3.gz
%{es_man_dir}/man3/strtok.3.gz
%{es_man_dir}/man3/strtok_r.3.gz
%{es_man_dir}/man3/strtol.3.gz
%{es_man_dir}/man3/strtold.3.gz
%{es_man_dir}/man3/strtoll.3.gz
%{es_man_dir}/man3/strtoq.3.gz
%{es_man_dir}/man3/strtoul.3.gz
%{es_man_dir}/man3/strtoull.3.gz
%{es_man_dir}/man3/strtouq.3.gz
%{es_man_dir}/man3/strverscmp.3.gz
%{es_man_dir}/man3/strxfrm.3.gz
%{es_man_dir}/man3/svc_destroy.3.gz
%{es_man_dir}/man3/svcerr_auth.3.gz
%{es_man_dir}/man3/svcerr_decode.3.gz
%{es_man_dir}/man3/svcerr_noproc.3.gz
%{es_man_dir}/man3/svcerr_noprog.3.gz
%{es_man_dir}/man3/svcerr_progvers.3.gz
%{es_man_dir}/man3/svcerr_systemerr.3.gz
%{es_man_dir}/man3/svcerr_weakauth.3.gz
%{es_man_dir}/man3/svcfd_create.3.gz
%{es_man_dir}/man3/svc_freeargs.3.gz
%{es_man_dir}/man3/svc_getargs.3.gz
%{es_man_dir}/man3/svc_getcaller.3.gz
%{es_man_dir}/man3/svc_getreq.3.gz
%{es_man_dir}/man3/svc_getreqset.3.gz
%{es_man_dir}/man3/svcraw_create.3.gz
%{es_man_dir}/man3/svc_register.3.gz
%{es_man_dir}/man3/svc_run.3.gz
%{es_man_dir}/man3/svc_sendreply.3.gz
%{es_man_dir}/man3/svctcp_create.3.gz
%{es_man_dir}/man3/svcudp_bufcreate.3.gz
%{es_man_dir}/man3/svcudp_create.3.gz
%{es_man_dir}/man3/svc_unregister.3.gz
%{es_man_dir}/man3/swab.3.gz
%{es_man_dir}/man3/swapcontext.3.gz
%{es_man_dir}/man3/swprintf.3.gz
%{es_man_dir}/man3/sysconf.3.gz
%{es_man_dir}/man3/syslog.3.gz
%{es_man_dir}/man3/system.3.gz
%{es_man_dir}/man3/tan.3.gz
%{es_man_dir}/man3/tanh.3.gz
%{es_man_dir}/man3/tcdrain.3.gz
%{es_man_dir}/man3/tcflow.3.gz
%{es_man_dir}/man3/tcflush.3.gz
%{es_man_dir}/man3/tcgetattr.3.gz
%{es_man_dir}/man3/tcgetpgrp.3.gz
%{es_man_dir}/man3/tcgetsid.3.gz
%{es_man_dir}/man3/tcsendbreak.3.gz
%{es_man_dir}/man3/tcsetattr.3.gz
%{es_man_dir}/man3/tcsetpgrp.3.gz
%{es_man_dir}/man3/tdelete.3.gz
%{es_man_dir}/man3/telldir.3.gz
%{es_man_dir}/man3/tempnam.3.gz
%{es_man_dir}/man3/termios.3.gz
%{es_man_dir}/man3/tfind.3.gz
%{es_man_dir}/man3/tgamma.3.gz
%{es_man_dir}/man3/tgammaf.3.gz
%{es_man_dir}/man3/tgammal.3.gz
%{es_man_dir}/man3/timegm.3.gz
%{es_man_dir}/man3/timelocal.3.gz
%{es_man_dir}/man3/tmpfile.3.gz
%{es_man_dir}/man3/tmpnam.3.gz
%{es_man_dir}/man3/toascii.3.gz
%{es_man_dir}/man3/tolower.3.gz
%{es_man_dir}/man3/toupper.3.gz
%{es_man_dir}/man3/towctrans.3.gz
%{es_man_dir}/man3/towlower.3.gz
%{es_man_dir}/man3/towupper.3.gz
%{es_man_dir}/man3/trunc.3.gz
%{es_man_dir}/man3/truncf.3.gz
%{es_man_dir}/man3/truncl.3.gz
%{es_man_dir}/man3/tsearch.3.gz
%{es_man_dir}/man3/ttyname.3.gz
%{es_man_dir}/man3/ttyname_r.3.gz
%{es_man_dir}/man3/ttyslot.3.gz
%{es_man_dir}/man3/twalk.3.gz
%{es_man_dir}/man3/tzset.3.gz
%{es_man_dir}/man3/ulimit.3.gz
%{es_man_dir}/man3/undocumented.3.gz
%{es_man_dir}/man3/ungetc.3.gz
%{es_man_dir}/man3/ungetwc.3.gz
%{es_man_dir}/man3/unlocked_stdio.3.gz
%{es_man_dir}/man3/unlockpt.3.gz
%{es_man_dir}/man3/unsetenv.3.gz
%{es_man_dir}/man3/updwtmp.3.gz
%{es_man_dir}/man3/usleep.3.gz
%{es_man_dir}/man3/utmpname.3.gz
%{es_man_dir}/man3/va_arg.3.gz
%{es_man_dir}/man3/va_end.3.gz
%{es_man_dir}/man3/valloc.3.gz
%{es_man_dir}/man3/vasprintf.3.gz
%{es_man_dir}/man3/va_start.3.gz
%{es_man_dir}/man3/vdprintf.3.gz
%{es_man_dir}/man3/verr.3.gz
%{es_man_dir}/man3/verrx.3.gz
%{es_man_dir}/man3/versionsort.3.gz
%{es_man_dir}/man3/vfprintf.3.gz
%{es_man_dir}/man3/vfscanf.3.gz
%{es_man_dir}/man3/vfwprintf.3.gz
%{es_man_dir}/man3/vprintf.3.gz
%{es_man_dir}/man3/vscanf.3.gz
%{es_man_dir}/man3/vsnprintf.3.gz
%{es_man_dir}/man3/vsprintf.3.gz
%{es_man_dir}/man3/vsscanf.3.gz
%{es_man_dir}/man3/vswprintf.3.gz
%{es_man_dir}/man3/vsyslog.3.gz
%{es_man_dir}/man3/vwarn.3.gz
%{es_man_dir}/man3/vwarnx.3.gz
%{es_man_dir}/man3/vwprintf.3.gz
%{es_man_dir}/man3/warn.3.gz
%{es_man_dir}/man3/warnx.3.gz
%{es_man_dir}/man3/wcpcpy.3.gz
%{es_man_dir}/man3/wcpncpy.3.gz
%{es_man_dir}/man3/wcrtomb.3.gz
%{es_man_dir}/man3/wcscasecmp.3.gz
%{es_man_dir}/man3/wcscat.3.gz
%{es_man_dir}/man3/wcschr.3.gz
%{es_man_dir}/man3/wcscmp.3.gz
%{es_man_dir}/man3/wcscpy.3.gz
%{es_man_dir}/man3/wcscspn.3.gz
%{es_man_dir}/man3/wcsdup.3.gz
%{es_man_dir}/man3/wcslen.3.gz
%{es_man_dir}/man3/wcsncasecmp.3.gz
%{es_man_dir}/man3/wcsncat.3.gz
%{es_man_dir}/man3/wcsncmp.3.gz
%{es_man_dir}/man3/wcsncpy.3.gz
%{es_man_dir}/man3/wcsnlen.3.gz
%{es_man_dir}/man3/wcsnrtombs.3.gz
%{es_man_dir}/man3/wcspbrk.3.gz
%{es_man_dir}/man3/wcsrchr.3.gz
%{es_man_dir}/man3/wcsrtombs.3.gz
%{es_man_dir}/man3/wcsspn.3.gz
%{es_man_dir}/man3/wcsstr.3.gz
%{es_man_dir}/man3/wcstok.3.gz
%{es_man_dir}/man3/wcstombs.3.gz
%{es_man_dir}/man3/wcswidth.3.gz
%{es_man_dir}/man3/wctob.3.gz
%{es_man_dir}/man3/wctomb.3.gz
%{es_man_dir}/man3/wctrans.3.gz
%{es_man_dir}/man3/wctype.3.gz
%{es_man_dir}/man3/wcwidth.3.gz
%{es_man_dir}/man3/wmemchr.3.gz
%{es_man_dir}/man3/wmemcmp.3.gz
%{es_man_dir}/man3/wmemcpy.3.gz
%{es_man_dir}/man3/wmemmove.3.gz
%{es_man_dir}/man3/wmemset.3.gz
%{es_man_dir}/man3/wprintf.3.gz
%{es_man_dir}/man3/xdr.3.gz
%{es_man_dir}/man3/xdr_accepted_reply.3.gz
%{es_man_dir}/man3/xdr_array.3.gz
%{es_man_dir}/man3/xdr_authunix_parms.3.gz
%{es_man_dir}/man3/xdr_bool.3.gz
%{es_man_dir}/man3/xdr_bytes.3.gz
%{es_man_dir}/man3/xdr_callhdr.3.gz
%{es_man_dir}/man3/xdr_callmsg.3.gz
%{es_man_dir}/man3/xdr_char.3.gz
%{es_man_dir}/man3/xdr_destroy.3.gz
%{es_man_dir}/man3/xdr_double.3.gz
%{es_man_dir}/man3/xdr_enum.3.gz
%{es_man_dir}/man3/xdr_float.3.gz
%{es_man_dir}/man3/xdr_free.3.gz
%{es_man_dir}/man3/xdr_getpos.3.gz
%{es_man_dir}/man3/xdr_inline.3.gz
%{es_man_dir}/man3/xdr_int.3.gz
%{es_man_dir}/man3/xdr_long.3.gz
%{es_man_dir}/man3/xdrmem_create.3.gz
%{es_man_dir}/man3/xdr_opaque.3.gz
%{es_man_dir}/man3/xdr_opaque_auth.3.gz
%{es_man_dir}/man3/xdr_pmap.3.gz
%{es_man_dir}/man3/xdr_pmaplist.3.gz
%{es_man_dir}/man3/xdr_pointer.3.gz
%{es_man_dir}/man3/xdrrec_create.3.gz
%{es_man_dir}/man3/xdrrec_endofrecord.3.gz
%{es_man_dir}/man3/xdrrec_eof.3.gz
%{es_man_dir}/man3/xdrrec_skiprecord.3.gz
%{es_man_dir}/man3/xdr_reference.3.gz
%{es_man_dir}/man3/xdr_rejected_reply.3.gz
%{es_man_dir}/man3/xdr_replymsg.3.gz
%{es_man_dir}/man3/xdr_setpos.3.gz
%{es_man_dir}/man3/xdr_short.3.gz
%{es_man_dir}/man3/xdrstdio_create.3.gz
%{es_man_dir}/man3/xdr_string.3.gz
%{es_man_dir}/man3/xdr_u_char.3.gz
%{es_man_dir}/man3/xdr_u_int.3.gz
%{es_man_dir}/man3/xdr_u_long.3.gz
%{es_man_dir}/man3/xdr_union.3.gz
%{es_man_dir}/man3/xdr_u_short.3.gz
%{es_man_dir}/man3/xdr_vector.3.gz
%{es_man_dir}/man3/xdr_void.3.gz
%{es_man_dir}/man3/xdr_wrapstring.3.gz
%{es_man_dir}/man3/xprt_register.3.gz
%{es_man_dir}/man3/xprt_unregister.3.gz
%{es_man_dir}/man3/y0.3.gz
%{es_man_dir}/man3/y0f.3.gz
%{es_man_dir}/man3/y0l.3.gz
%{es_man_dir}/man3/y1.3.gz
%{es_man_dir}/man3/y1f.3.gz
%{es_man_dir}/man3/y1l.3.gz
%{es_man_dir}/man3/yn.3.gz
%{es_man_dir}/man3/ynf.3.gz
%{es_man_dir}/man3/ynl.3.gz
%{es_man_dir}/man4/console.4.gz
%{es_man_dir}/man4/console_codes.4.gz
%{es_man_dir}/man4/console_ioctl.4.gz
%{es_man_dir}/man4/dsp56k.4.gz
%{es_man_dir}/man4/fd.4.gz
%{es_man_dir}/man4/fifo.4.gz
%{es_man_dir}/man4/full.4.gz
%{es_man_dir}/man4/futex.4.gz
%{es_man_dir}/man4/hd.4.gz
%{es_man_dir}/man4/initrd.4.gz
%{es_man_dir}/man4/intro.4.gz
%{es_man_dir}/man4/kmem.4.gz
%{es_man_dir}/man4/lp.4.gz
%{es_man_dir}/man4/mem.4.gz
%{es_man_dir}/man4/mouse.4.gz
%{es_man_dir}/man4/null.4.gz
%{es_man_dir}/man4/port.4.gz
%{es_man_dir}/man4/ptmx.4.gz
%{es_man_dir}/man4/pts.4.gz
%{es_man_dir}/man4/ram.4.gz
%{es_man_dir}/man4/random.4.gz
%{es_man_dir}/man4/sd.4.gz
%{es_man_dir}/man4/st.4.gz
%{es_man_dir}/man4/tty.4.gz
%{es_man_dir}/man4/tty_ioctl.4.gz
%{es_man_dir}/man4/ttyS.4.gz
%{es_man_dir}/man4/urandom.4.gz
%{es_man_dir}/man4/vcs.4.gz
%{es_man_dir}/man4/vcsa.4.gz
%{es_man_dir}/man4/wavelan.4.gz
%{es_man_dir}/man4/zero.4.gz
%{es_man_dir}/man5/acct.5.gz
%{es_man_dir}/man5/charmap.5.gz
%{es_man_dir}/man5/dir_colors.5.gz
%{es_man_dir}/man5/environ.5.gz
%{es_man_dir}/man5/fs.5.gz
%{es_man_dir}/man5/ftpusers.5.gz
%{es_man_dir}/man5/group.5.gz
%{es_man_dir}/man5/host.conf.5.gz
%{es_man_dir}/man5/hosts.5.gz
%{es_man_dir}/man5/hosts.equiv.5.gz
%{es_man_dir}/man5/intro.5.gz
%{es_man_dir}/man5/ipc.5.gz
%{es_man_dir}/man5/issue.5.gz
%{es_man_dir}/man5/locale.5.gz
%{es_man_dir}/man5/motd.5.gz
%{es_man_dir}/man5/nologin.5.gz
%{es_man_dir}/man5/nscd.conf.5.gz
%{es_man_dir}/man5/nsswitch.conf.5.gz
%{es_man_dir}/man5/passwd.5.gz
%{es_man_dir}/man5/proc.5.gz
%{es_man_dir}/man5/protocols.5.gz
%{es_man_dir}/man5/resolv.conf.5.gz
%{es_man_dir}/man5/resolver.5.gz
%{es_man_dir}/man5/rpc.5.gz
%{es_man_dir}/man5/securetty.5.gz
%{es_man_dir}/man5/services.5.gz
%{es_man_dir}/man5/shells.5.gz
%{es_man_dir}/man5/slabinfo.5.gz
%{es_man_dir}/man5/termcap.5.gz
%{es_man_dir}/man5/ttytype.5.gz
%{es_man_dir}/man5/tzfile.5.gz
%{es_man_dir}/man5/utmp.5.gz
%{es_man_dir}/man5/wtmp.5.gz
%{es_man_dir}/man6/intro.6.gz
%{es_man_dir}/man7/arp.7.gz
%{es_man_dir}/man7/ascii.7.gz
%{es_man_dir}/man7/boot.7.gz
%{es_man_dir}/man7/bootparam.7.gz
%{es_man_dir}/man7/capabilities.7.gz
%{es_man_dir}/man7/charsets.7.gz
%{es_man_dir}/man7/ddp.7.gz
%{es_man_dir}/man7/glob.7.gz
%{es_man_dir}/man7/hier.7.gz
%{es_man_dir}/man7/icmp.7.gz
%{es_man_dir}/man7/intro.7.gz
%{es_man_dir}/man7/ip.7.gz
%{es_man_dir}/man7/ipv6.7.gz
%{es_man_dir}/man7/iso_8859_15.7.gz
%{es_man_dir}/man7/iso_8859-15.7.gz
%{es_man_dir}/man7/iso-8859-15.7.gz
%{es_man_dir}/man7/iso_8859_1.7.gz
%{es_man_dir}/man7/iso_8859-1.7.gz
%{es_man_dir}/man7/iso-8859-1.7.gz
%{es_man_dir}/man7/iso_8859_2.7.gz
%{es_man_dir}/man7/iso_8859-2.7.gz
%{es_man_dir}/man7/iso-8859-2.7.gz
%{es_man_dir}/man7/iso_8859_7.7.gz
%{es_man_dir}/man7/iso_8859-7.7.gz
%{es_man_dir}/man7/iso-8859-7.7.gz
%{es_man_dir}/man7/iso_8859_9.7.gz
%{es_man_dir}/man7/iso_8859-9.7.gz
%{es_man_dir}/man7/iso-8859-9.7.gz
%{es_man_dir}/man7/latin1.7.gz
%{es_man_dir}/man7/latin2.7.gz
%{es_man_dir}/man7/LDP.7.gz
%{es_man_dir}/man7/locale.7.gz
%{es_man_dir}/man7/mailaddr.7.gz
%{es_man_dir}/man7/man.7.gz
%{es_man_dir}/man7/mdoc.7.gz
%{es_man_dir}/man7/mdoc.samples.7.gz
%{es_man_dir}/man7/netdevice.7.gz
%{es_man_dir}/man7/netlink.7.gz
%{es_man_dir}/man7/packet.7.gz
%{es_man_dir}/man7/raw.7.gz
%{es_man_dir}/man7/regex.7.gz
%{es_man_dir}/man7/rtnetlink.7.gz
%{es_man_dir}/man7/signal.7.gz
%{es_man_dir}/man7/socket.7.gz
%{es_man_dir}/man7/suffixes.7.gz
%{es_man_dir}/man7/tcp.7.gz
%{es_man_dir}/man7/udp.7.gz
%{es_man_dir}/man7/unicode.7.gz
%{es_man_dir}/man7/units.7.gz
%{es_man_dir}/man7/unix.7.gz
%{es_man_dir}/man7/uri.7.gz
%{es_man_dir}/man7/url.7.gz
%{es_man_dir}/man7/utf-8.7.gz
%{es_man_dir}/man7/utf8.7.gz
%{es_man_dir}/man7/x25.7.gz
%{es_man_dir}/man8/intro.8.gz
%{es_man_dir}/man8/ldconfig.8.gz
%{es_man_dir}/man8/ld.so.8.gz
%{es_man_dir}/man8/nscd.8.gz
%{es_man_dir}/man8/sync.8.gz
%{es_man_dir}/man8/tzselect.8.gz
%{es_man_dir}/man8/zdump.8.gz
%{es_man_dir}/man8/zic.8.gz

%files extra
%doc %{extra_pkg_name}/LEEME.extra %{extra_pkg_name}/README.extra %{extra_pkg_name}/PAQUETES %{extra_pkg_name}/PROYECTO
%{es_man_dir}/man1/addr2line.1.gz
%{es_man_dir}/man1/ansi2knr.1.gz
%{es_man_dir}/man1/ar.1.gz
%{es_man_dir}/man1/arch.1.gz
%{es_man_dir}/man1/as.1.gz
%{es_man_dir}/man1/at.1.gz
%{es_man_dir}/man1/atq.1.gz
%{es_man_dir}/man1/atrm.1.gz
%{es_man_dir}/man1/awk.1.gz
%{es_man_dir}/man1/basename.1.gz
%{es_man_dir}/man1/bash.1.gz
%{es_man_dir}/man1/bashbug.1.gz
%{es_man_dir}/man1/batch.1.gz
%{es_man_dir}/man1/bc.1.gz
%{es_man_dir}/man1/builtins.1.gz
%{es_man_dir}/man1/bunzip2.1.gz
%{es_man_dir}/man1/bzcat.1.gz
%{es_man_dir}/man1/bzip2.1.gz
%{es_man_dir}/man1/cdp.1.gz
%{es_man_dir}/man1/c++filt.1.gz
%{es_man_dir}/man1/chroot.1.gz
%{es_man_dir}/man1/chvt.1.gz
%{es_man_dir}/man1/colrm.1.gz
%{es_man_dir}/man1/column.1.gz
%{es_man_dir}/man1/cpio.1.gz
%{es_man_dir}/man1/ddate.1.gz
%{es_man_dir}/man1/deallocvt.1.gz
%{es_man_dir}/man1/dirname.1.gz
%{es_man_dir}/man1/dnsdomainname.1.gz
%{es_man_dir}/man1/domainname.1.gz
%{es_man_dir}/man1/dumpkeys.1.gz
%{es_man_dir}/man1/echo.1.gz
%{es_man_dir}/man1/egrep.1.gz
%{es_man_dir}/man1/env.1.gz
%{es_man_dir}/man1/epsffit.1.gz
%{es_man_dir}/man1/expr.1.gz
%{es_man_dir}/man1/extractres.1.gz
%{es_man_dir}/man1/false.1.gz
%{es_man_dir}/man1/fgrep.1.gz
%{es_man_dir}/man1/file.1.gz
%{es_man_dir}/man1/find.1.gz
%{es_man_dir}/man1/fixdlsrps.1.gz
%{es_man_dir}/man1/fixfmps.1.gz
%{es_man_dir}/man1/fixmacps.1.gz
%{es_man_dir}/man1/fixpsditps.1.gz
%{es_man_dir}/man1/fixpspps.1.gz
%{es_man_dir}/man1/fixscribeps.1.gz
%{es_man_dir}/man1/fixtpps.1.gz
%{es_man_dir}/man1/fixwfwps.1.gz
%{es_man_dir}/man1/fixwpps.1.gz
%{es_man_dir}/man1/fixwwps.1.gz
%{es_man_dir}/man1/flex.1.gz
%{es_man_dir}/man1/flex++.1.gz
%{es_man_dir}/man1/formail.1.gz
%{es_man_dir}/man1/free.1.gz
%{es_man_dir}/man1/gawk.1.gz
%{es_man_dir}/man1/gdb.1.gz
%{es_man_dir}/man1/getafm.1.gz
%{es_man_dir}/man1/getopt.1.gz
%{es_man_dir}/man1/gprof.1.gz
%{es_man_dir}/man1/grep.1.gz
%{es_man_dir}/man1/groups.1.gz
%{es_man_dir}/man1/gunzip.1.gz
%{es_man_dir}/man1/gzexe.1.gz
%{es_man_dir}/man1/gzip.1.gz
%{es_man_dir}/man1/hostname.1.gz
%{es_man_dir}/man1/icewm.1x.gz
%{es_man_dir}/man1/id.1.gz
%{es_man_dir}/man1/igawk.1.gz
%{es_man_dir}/man1/includeres.1.gz
%{es_man_dir}/man1/kbd_mode.1.gz
%{es_man_dir}/man1/last.1.gz
%{es_man_dir}/man1/lastb.1.gz
%{es_man_dir}/man1/ld.1.gz
%{es_man_dir}/man1/lex.1.gz
%{es_man_dir}/man1/lockfile.1.gz
%{es_man_dir}/man1/login.1.gz
%{es_man_dir}/man1/logname.1.gz
%{es_man_dir}/man1/look.1.gz
%{es_man_dir}/man1/make.1.gz
%{es_man_dir}/man1/mattrib.1.gz
%{es_man_dir}/man1/mbadblocks.1.gz
%{es_man_dir}/man1/mcd.1.gz
%{es_man_dir}/man1/mcopy.1.gz
%{es_man_dir}/man1/mdel.1.gz
%{es_man_dir}/man1/mdeltree.1.gz
%{es_man_dir}/man1/mdir.1.gz
%{es_man_dir}/man1/mesg.1.gz
%{es_man_dir}/man1/mev.1.gz
%{es_man_dir}/man1/mformat.1.gz
%{es_man_dir}/man1/mmount.1.gz
%{es_man_dir}/man1/modprobe.1.gz
%{es_man_dir}/man1/more.1.gz
%{es_man_dir}/man1/mrd.1.gz
%{es_man_dir}/man1/mread.1.gz
%{es_man_dir}/man1/mren.1.gz
%{es_man_dir}/man1/mt.1.gz
%{es_man_dir}/man1/mtools.1.gz
%{es_man_dir}/man1/mtoolstest.1.gz
%{es_man_dir}/man1/mtype.1.gz
%{es_man_dir}/man1/mzip.1.gz
%{es_man_dir}/man1/namei.1.gz
%{es_man_dir}/man1/nice.1.gz
%{es_man_dir}/man1/nisdomainname.1.gz
%{es_man_dir}/man1/nlmconv.1.gz
%{es_man_dir}/man1/nm.1.gz
%{es_man_dir}/man1/nohup.1.gz
%{es_man_dir}/man1/objcopy.1.gz
%{es_man_dir}/man1/objdump.1.gz
%{es_man_dir}/man1/od.1.gz
%{es_man_dir}/man1/passwd.1.gz
%{es_man_dir}/man1/paste.1.gz
%{es_man_dir}/man1/pathchk.1.gz
%{es_man_dir}/man1/pico.1.gz
%{es_man_dir}/man1/pilot.1.gz
%{es_man_dir}/man1/pine.1.gz
%{es_man_dir}/man1/pr.1.gz
%{es_man_dir}/man1/printenv.1.gz
%{es_man_dir}/man1/printf.1.gz
%{es_man_dir}/man1/procmail.1.gz
%{es_man_dir}/man1/ps.1.gz
%{es_man_dir}/man1/psbook.1.gz
%{es_man_dir}/man1/psfaddtable.1.gz
%{es_man_dir}/man1/psfgettable.1.gz
%{es_man_dir}/man1/psfstriptable.1.gz
%{es_man_dir}/man1/psmerge.1.gz
%{es_man_dir}/man1/psnup.1.gz
%{es_man_dir}/man1/psresize.1.gz
%{es_man_dir}/man1/psselect.1.gz
%{es_man_dir}/man1/pstops.1.gz
%{es_man_dir}/man1/pwd.1.gz
%{es_man_dir}/man1/python.1.gz
%{es_man_dir}/man1/ranlib.1.gz
%{es_man_dir}/man1/readprofile.1.gz
%{es_man_dir}/man1/reset.1.gz
%{es_man_dir}/man1/rev.1.gz
%{es_man_dir}/man1/rpncalc.1.gz
%{es_man_dir}/man1/rpost.1.gz
%{es_man_dir}/man1/script.1.gz
%{es_man_dir}/man1/sessreg.1.gz
%{es_man_dir}/man1/setleds.1.gz
%{es_man_dir}/man1/setmetamode.1.gz
%{es_man_dir}/man1/setterm.1.gz
%{es_man_dir}/man1/showkey.1.gz
%{es_man_dir}/man1/size.1.gz
%{es_man_dir}/man1/skill.1.gz
%{es_man_dir}/man1/sleep.1.gz
%{es_man_dir}/man1/sln.1.gz
%{es_man_dir}/man1/snice.1.gz
%{es_man_dir}/man1/strings.1.gz
%{es_man_dir}/man1/strip.1.gz
%{es_man_dir}/man1/stty.1.gz
%{es_man_dir}/man1/su.1.gz
%{es_man_dir}/man1/suck.1.gz
%{es_man_dir}/man1/tar.1.gz
%{es_man_dir}/man1/tee.1.gz
%{es_man_dir}/man1/telnet.1.gz
%{es_man_dir}/man1/test.1.gz
%{es_man_dir}/man1/testhost.1.gz
%{es_man_dir}/man1/tload.1.gz
%{es_man_dir}/man1/top.1.gz
%{es_man_dir}/man1/true.1.gz
%{es_man_dir}/man1/tsort.1.gz
%{es_man_dir}/man1/tty.1.gz
%{es_man_dir}/man1/ul.1.gz
%{es_man_dir}/man1/uname.1.gz
%{es_man_dir}/man1/updatedb.1.gz
%{es_man_dir}/man1/uptime.1.gz
%{es_man_dir}/man1/users.1.gz
%{es_man_dir}/man1/w.1.gz
%{es_man_dir}/man1/wall.1.gz
%{es_man_dir}/man1/watch.1.gz
%{es_man_dir}/man1/whereis.1.gz
%{es_man_dir}/man1/who.1.gz
%{es_man_dir}/man1/whoami.1.gz
%{es_man_dir}/man1/write.1.gz
%{es_man_dir}/man1/xargs.1.gz
%{es_man_dir}/man1/yes.1.gz
%{es_man_dir}/man1/ypdomainname.1.gz
%{es_man_dir}/man1/zcat.1.gz
%{es_man_dir}/man1/zcmp.1.gz
%{es_man_dir}/man1/zdiff.1.gz
%{es_man_dir}/man1/zforce.1.gz
%{es_man_dir}/man1/zgrep.1.gz
%{es_man_dir}/man1/zmore.1.gz
%{es_man_dir}/man1/znew.1.gz
%{es_man_dir}/man2/create_module.2.gz
%{es_man_dir}/man2/delete_module.2.gz
%{es_man_dir}/man2/get_kernel_syms.2.gz
%{es_man_dir}/man2/init_module.2.gz
%{es_man_dir}/man2/query_module.2.gz
%{es_man_dir}/man3/dlclose.3.gz
%{es_man_dir}/man3/dlerror.3.gz
#%{es_man_dir}/man3/dlopen.3.gz
%{es_man_dir}/man3/dlsym.3.gz
%{es_man_dir}/man4/magic.4.gz
#%{es_man_dir}/man5/acct.5.gz
%{es_man_dir}/man5/at_allow.5.gz
%{es_man_dir}/man5/ethers.5.gz
%{es_man_dir}/man5/exports.5.gz
%{es_man_dir}/man5/fstab.5.gz
%{es_man_dir}/man5/get-news.conf.5.gz
#%{es_man_dir}/man5/host.conf.5.gz
%{es_man_dir}/man5/initscript.5.gz
%{es_man_dir}/man5/inittab.5.gz
%{es_man_dir}/man5/issue.net.5.gz
%{es_man_dir}/man5/locatedb.5.gz
%{es_man_dir}/man5/networks.5.gz
%{es_man_dir}/man5/nfs.5.gz
%{es_man_dir}/man5/procmailex.5.gz
%{es_man_dir}/man5/procmailrc.5.gz
%{es_man_dir}/man5/procmailsc.5.gz
%{es_man_dir}/man5/raidtab.5.gz
%{es_man_dir}/man5/resolv.conf.5.gz
#%{es_man_dir}/man5/resolver.5.gz
%{es_man_dir}/man6/banner.6.gz
%{es_man_dir}/man7/regex_debian.7.gz
%{es_man_dir}/man7/undocumented.7.gz
%{es_man_dir}/man8/agetty.8.gz
%{es_man_dir}/man8/arp.8.gz
%{es_man_dir}/man8/atd.8.gz
%{es_man_dir}/man8/atrun.8.gz
%{es_man_dir}/man8/bdflush.8.gz
%{es_man_dir}/man8/ckraid.8.gz
%{es_man_dir}/man8/ctrlaltdel.8.gz
%{es_man_dir}/man8/cytune.8.gz
%{es_man_dir}/man8/dip.8.gz
%{es_man_dir}/man8/diplogin.8.gz
%{es_man_dir}/man8/fastboot.8.gz
%{es_man_dir}/man8/fasthalt.8.gz
%{es_man_dir}/man8/fdisk.8.gz
%{es_man_dir}/man8/frag.8.gz
%{es_man_dir}/man8/fsck.minix.8.gz
%{es_man_dir}/man8/getkeycodes.8.gz
%{es_man_dir}/man8/get-news.8.gz
%{es_man_dir}/man8/gpm.8.gz
%{es_man_dir}/man8/halt.8.gz
%{es_man_dir}/man8/hwclock.8.gz
%{es_man_dir}/man8/ifconfig.8.gz
%{es_man_dir}/man8/inetd.8.gz
%{es_man_dir}/man8/init.8.gz
%{es_man_dir}/man8/ipchains.8.gz
%{es_man_dir}/man8/ipcrm.8.gz
%{es_man_dir}/man8/ipcs.8.gz
%{es_man_dir}/man8/ipfwadm.8.gz
%{es_man_dir}/man8/killall5.8.gz
#%{es_man_dir}/man8/ld.so.8.gz
%{es_man_dir}/man8/loadunimap.8.gz
%{es_man_dir}/man8/logrotate.8.gz
%{es_man_dir}/man8/mapscrn.8.gz
%{es_man_dir}/man8/mcserv.8.gz
%{es_man_dir}/man8/mkfs.8.gz
%{es_man_dir}/man8/mkfs.minix.8.gz
%{es_man_dir}/man8/mkpv.8.gz
%{es_man_dir}/man8/mkraid.8.gz
%{es_man_dir}/man8/mkswap.8.gz
%{es_man_dir}/man8/mount.8.gz
%{es_man_dir}/man8/netstat.8.gz
%{es_man_dir}/man8/pidof.8.gz
%{es_man_dir}/man8/ping.8.gz
%{es_man_dir}/man8/poweroff.8.gz
%{es_man_dir}/man8/psupdate.8.gz
%{es_man_dir}/man8/raidadd.8.gz
%{es_man_dir}/man8/raidrun.8.gz
%{es_man_dir}/man8/raidstart.8.gz
%{es_man_dir}/man8/raidstop.8.gz
%{es_man_dir}/man8/ramsize.8.gz
%{es_man_dir}/man8/rarp.8.gz
%{es_man_dir}/man8/rdev.8.gz
%{es_man_dir}/man8/reboot.8.gz
%{es_man_dir}/man8/renice.8.gz
%{es_man_dir}/man8/resizecons.8.gz
%{es_man_dir}/man8/rootflags.8.gz
%{es_man_dir}/man8/route.8.gz
%{es_man_dir}/man8/runlevel.8.gz
%{es_man_dir}/man8/setfdprm.8.gz
%{es_man_dir}/man8/setfont.8.gz
%{es_man_dir}/man8/setkeycodes.8.gz
%{es_man_dir}/man8/setsid.8.gz
%{es_man_dir}/man8/shutdown.8.gz
%{es_man_dir}/man8/simpleinit.8.gz
%{es_man_dir}/man8/sulogin.8.gz
%{es_man_dir}/man8/swapdev.8.gz
%{es_man_dir}/man8/swapoff.8.gz
%{es_man_dir}/man8/swapon.8.gz
%{es_man_dir}/man8/telinit.8.gz
%{es_man_dir}/man8/tunelp.8.gz
%{es_man_dir}/man8/umount.8.gz
%{es_man_dir}/man8/update.8.gz
%{es_man_dir}/man8/vidmode.8.gz
#%{es_man_dir}/man8/vigr.8.gz
%{es_man_dir}/man8/vmstat.8.gz


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.55-34
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 1.55-26
- remove non-free man-pages (bz1334282)

* Sat Feb 27 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.55-25
- Add Supplements: for https://fedoraproject.org/wiki/Packaging:Langpacks guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Jens Petersen <petersen@redhat.com> - 1.55-20
- revert license tags and add only GPL+ and GPLv2+ and LDP
  (a more detailed license audit of the manpages is really needed)

* Mon Nov 26 2012 Jens Petersen <petersen@redhat.com> - 1.55-19
- inherit the license tags of the man-pages package (#880076)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 04 2010 Ding-Yi Chen <dchen@redhat.com> - 1.55-15
- Bug 582909 - man-pages-es: Change requires tag from man to man-pages-reader

* Mon Feb 01 2010 Ding-Yi Chen <dchen@redhat.com> - 1.55-14
- Resolves: #559851

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Ding-Yi Chen <dchen@redhat.com> - 1.55-9
- Bug 510363 -  Unowned directories in man-pages-es-1.55-7.fc11

* Mon Mar 03 2009 Ding-Yi Chen <dchen@redhat.com> - 1.55-7
- Bug 487941 - File conflict between man-pages-es-extra and shadow-utils
  Removed es/man8/vigr.8.gz

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 08 2008 Ding-Yi Chen <dchen@redhat.com> - 1.55-5
- Bug 427684: man-pages fileconflict
- Fix the conflict with vipw.8 (in shadow-utils)

* Fri Dec 06 2007 Ding-Yi Chen <dchen@redhat.com> - 1.55-4
- [Bug 226124]  Merge Review: man-pages-es (comment 10)
- Fix improper SPEC file

* Wed Dec 06 2007 Ding-Yi Chen <dchen@redhat.com> - 1.55-3
- Change the Licence from "Freely redistributable without restriction" to IEEE

* Tue Dec 04 2007 Ding-Yi Chen <dchen@redhat.com> - 1.55-2
- [Bug 226124]  Merge Review: man-pages-es

* Mon Nov 19 2007 Ding-Yi Chen <dchen@redhat.com> - 1.55-1
- [Bug 388391] New: fileconflicts with other packages
- Remove mc.1.gz, as it conflicts with mc-4.6.1a-49.20070604cvs.fc8.i386.rpm
- Remove newgrp.1.gz, as it conflicts with shadow-utils-4.0.18.1-18.fc8.i386.rpm

* Wed Oct 31 2007 Ding-Yi Chen <dchen@redhat.com> - 1.55
- Update to 1.55
- Add Spanish summaries and descriptions

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.28-10.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 29 2004 Leon Ho <llch@redhat.com>
- rebuilt
              
* Sun Sep 26 2004 Rik van Riel <riel@redhat.com> 1.28-9
- fix the URL (bug #114895)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Phil Knirsch <pknirsch@redhat.com> 1.28-7
- Convert all manpages to utf-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.28-6
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.28-5
- rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 14 2001 Trond Eivind Glomsrø <teg@redhat.com> 1.28-1
- 1.28
- New URL

* Mon Aug 13 2001 Trond Eivind Glomsrø <teg@redhat.com> 0.6a-9
- Rebuild. Should fix #51679

* Thu Aug  2 2001 Trond Eivind Glomsrø <teg@redhat.com>
- Own %%{es_man_dir}

* Tue Apr  3 2001 Trond Eivind Glomsrø <teg@redhat.com>
- Fix some roff errors in man pages, delete console_codes.4 
  (has error, can't locate it)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 20 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Mon Jun 19 2000 Matt Wilson <msw@redhat.com>
- defattr root

* Sun Jun 12 2000 Trond Eivind Glomsrø <teg@redhat.com>
- use %%{_mandir} and %%{_tmppath}

* Mon May 15 2000 Trond Eivind Glomsrø <teg@redhat.com>
- first build

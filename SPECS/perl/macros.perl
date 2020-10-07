# Sensible Perl-specific RPM build macros.
#
# Note that these depend on the generic filtering system being in place in
# rpm core; but won't cause a build to fail if they're not present.
#
# Chris Weyl <cweyl@alumni.drew.edu> 2009
# Marcela Mašláňová <mmaslano@redhat.com> 2011

# This macro unsets several common vars used to control how Makefile.PL (et
# al) build and install packages.  We also set a couple to help some of the
# common systems be less interactive.  This was blatantly stolen from
# cpanminus, and helps building rpms locally when one makes extensive use of
# local::lib, etc.
#
# Usage, in %build, before "%{__perl} Makefile.PL ..."
#
#   %{?perl_ext_env_unset}

%perl_ext_env_unset %{expand:
unset PERL_MM_OPT MODULEBUILDRC PERL5INC
export PERL_AUTOINSTALL="--defaultdeps"
export PERL_MM_USE_DEFAULT=1
}

#############################################################################
# Perl specific macros, no longer part of rpm >= 4.15
%perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)
%perl_vendorlib  %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%perl_archlib    %(eval "`%{__perl} -V:installarchlib`"; echo $installarchlib)
%perl_privlib    %(eval "`%{__perl} -V:installprivlib`"; echo $installprivlib)

#############################################################################
# Filtering macro incantations

# keep track of what "revision" of the filtering we're at.  Each time we
# change the filter we should increment this.

%perl_default_filter_revision 3

# By default, for perl packages we want to filter all files in _docdir from 
# req/prov scanning.
# Filtering out any provides caused by private libs in vendorarch/archlib
# (vendor/core) is done by rpmbuild since Fedora 20
# <https://fedorahosted.org/fpc/ticket/353>.
#
# Note that this must be invoked in the spec file, preferably as 
# "%{?perl_default_filter}", before any %description block.

%perl_default_filter %{expand: \
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_docdir}
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}^%{_docdir}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\\\(VMS|^perl\\\\(Win32|^perl\\\\(DB\\\\)|^perl\\\\(UNIVERSAL\\\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\\\(VMS|^perl\\\\(Win32
}

#############################################################################
# Macros to assist with generating a "-tests" subpackage in a semi-automatic
# manner.
#
# The following macros are still in a highly experimental stage and users
# should be aware that the interface and behaviour may change. 
#
# PLEASE, PLEASE CONDITIONALIZE THESE MACROS IF YOU USE THEM.
#
# See http://gist.github.com/284409

# These macros should be invoked as above, right before the first %description
# section, and conditionalized.  e.g., for the common case where all our tests
# are located under t/, the correct usage is:
#
#   %{?perl_default_subpackage_tests}
#
# If custom files/directories need to be specified, this can be done as such:
#
#   %{?perl_subpackage_tests:%perl_subpackage_tests t/ one/ three.sql}
#
# etc, etc.

%perl_version   %(eval "`%{__perl} -V:version`"; echo $version)
%perl_testdir   %{_libexecdir}/perl5-tests
%cpan_dist_name %(eval echo %{name} | %{__sed} -e 's/^perl-//')

# easily mark something as required by -tests and BR to the main package
%tests_req() %{expand:\
BuildRequires: %*\
%%tests_subpackage_requires %*\
}

# fixup (and create if needed) the shbang lines in tests, so they work and
# rpmlint doesn't (correctly) have a fit
%fix_shbang_line() \
TMPHEAD=`mktemp`\
TMPBODY=`mktemp`\
for file in %* ; do \
    head -1 $file > $TMPHEAD\
    tail -n +2 $file > $TMPBODY\
    %{__perl} -pi -e '$f = /^#!/ ? "" : "#!%{__perl}$/"; $_="$f$_"' $TMPHEAD\
    cat $TMPHEAD $TMPBODY > $file\
done\
%{__perl} -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(qw{%*})"\
%{__rm} $TMPHEAD $TMPBODY\
%{nil}

# additional -tests subpackage requires, if any
%tests_subpackage_requires() %{expand: \
%global __tests_spkg_req %{?__tests_spkg_req} %* \
}

# additional -tests subpackage provides, if any
%tests_subpackage_provides() %{expand: \
%global __tests_spkg_prov %{?__tests_spkg_prov} %* \
}

#
# Runs after the body of %check completes.
#

%__perl_check_pre %{expand: \
%{?__spec_check_pre} \
pushd %{buildsubdir} \
%define perl_br_testdir %{buildroot}%{perl_testdir}/%{cpan_dist_name} \
%{__mkdir_p} %{perl_br_testdir} \
%{__tar} -cf - %{__perl_test_dirs} | ( cd %{perl_br_testdir} && %{__tar} -xf - ) \
find . -maxdepth 1 -type f -name '*META*' -exec %{__cp} -vp {} %{perl_br_testdir} ';' \
find %{perl_br_testdir} -type f -exec %{__chmod} -c -x {} ';' \
T_FILES=`find %{perl_br_testdir} -type f -name '*.t'` \
%fix_shbang_line $T_FILES \
%{__chmod} +x $T_FILES \
%{_fixperms} %{perl_br_testdir} \
popd \
}

#
# The actual invoked macro
#

%perl_subpackage_tests() %{expand: \
%global __perl_package 1\
%global __perl_test_dirs %* \
%global __spec_check_pre %{expand:%{__perl_check_pre}} \
%package tests\
Summary: Test suite for package %{name}\
Group: Development/Debug\
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}\
Requires: /usr/bin/prove \
%{?__tests_spkg_req:Requires: %__tests_spkg_req}\
%{?__tests_spkg_prov:Provides: %__tests_spkg_prov}\
AutoReqProv: 0 \
%description tests\
This package provides the test suite for package %{name}.\
%files tests\
%defattr(-,root,root,-)\
%{perl_testdir}\
}

# shortcut sugar
%perl_default_subpackage_tests %perl_subpackage_tests t/


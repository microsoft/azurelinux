Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: hunspell-no
Summary: Norwegian hunspell dictionaries
Version: 2.0.10
Release: 13%{?dist}

Source0: https://alioth-archive.debian.org/releases/spell-norwegian/spell-norwegian/%{version}/no_NO-pack2-%{version}.zip
Source1: %{name}-LICENSE.txt
URL: https://alioth-archive.debian.org/releases/spell-norwegian/spell-norwegian/
License: GPL+
BuildArch: noarch

Patch1:  rhbz959989.badsfxrules.patch

%description
Norwegian hunspell dictionaries.

%package -n hunspell-nb
Summary: Bokmaal hunspell dictionaries
Requires: hunspell
Supplements: (hunspell and langpacks-nb)

%description -n hunspell-nb
Bokmaal hunspell dictionaries.

%package -n hunspell-nn
Summary: Nynorsk hunspell dictionaries
Requires: hunspell
Supplements: (hunspell and langpacks-nn)

%description -n hunspell-nn
Nynorsk hunspell dictionaries.

%package -n hyphen-nb
Summary: Bokmaal hyphenation rules
Requires: hyphen
Supplements: (hyphen and langpacks-nb)

%description -n hyphen-nb
Bokmaal hyphenation rules.

%package -n hyphen-nn
Summary: Nynorsk hyphenation rules
Requires: hyphen
Supplements: (hyphen and langpacks-nn)

%description -n hyphen-nn
Nynorsk hyphenation rules

%package -n mythes-nb
Summary: Bokmaal thesaurus
Requires: mythes
Supplements: (mythes and langpacks-nb)

%description -n mythes-nb
Bokmaal thesaurus.

%package -n mythes-nn
Summary: Nynorsk thesaurus 
Requires: mythes
Supplements: (mythes and langpacks-nn)

%description -n mythes-nn
Nynorsk thesaurus.

%prep
%setup -q -c
unzip -q nb_NO.zip
unzip -q nn_NO.zip
unzip -q hyph_nb_NO.zip
unzip -q hyph_nn_NO.zip
unzip -q th_nb_NO_v2.zip
unzip -q th_nn_NO_v2.zip
%patch1 -p0 -b .rhbz959989

cp %{SOURCE1} ./LICENSE.txt

%build
for i in README_nb_NO.txt README_nn_NO.txt README_hyph_nb_NO.txt \
  README_hyph_nn_NO.txt README_th_nb_NO_v2.txt README_th_nn_NO_v2.txt; do
  if ! iconv -f utf-8 -t utf-8 -o /dev/null $i > /dev/null 2>&1; then
    iconv -f ISO-8859-1 -t UTF-8 $i > $i.new
    touch -r $i $i.new
    mv -f $i.new $i
  fi
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p nn_NO.aff nn_NO.dic nb_NO.aff nb_NO.dic $RPM_BUILD_ROOT/%{_datadir}/myspell
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_nn_NO.dic hyph_nb_NO.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_nb_NO_v2.dat th_nb_NO_v2.idx th_nn_NO_v2.dat th_nn_NO_v2.idx $RPM_BUILD_ROOT/%{_datadir}/mythes


%files -n hunspell-nb
%license LICENSE.txt
%doc README_nb_NO.txt
%{_datadir}/myspell/nb_NO.*

%files -n hunspell-nn
%license LICENSE.txt
%doc README_nn_NO.txt
%{_datadir}/myspell/nn_NO.*

%files -n hyphen-nb
%license LICENSE.txt
%doc README_hyph_nb_NO.txt
%{_datadir}/hyphen/hyph_nb_NO.*

%files -n hyphen-nn
%license LICENSE.txt
%doc README_hyph_nn_NO.txt
%{_datadir}/hyphen/hyph_nn_NO.*

%files -n mythes-nb
%license LICENSE.txt
%doc README_th_nb_NO_v2.txt
%{_datadir}/mythes/th_nb_NO_v2.*

%files -n mythes-nn
%license LICENSE.txt
%doc README_th_nb_NO_v2.txt
%{_datadir}/mythes/th_nn_NO_v2.*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.0.10-13
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.0.10-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 1:2.0.10-7
- Update Source tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1:2.0.10-3
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 15 2015 Caolán McNamara <caolanm@redhat.com> - 1:2.0.10
- Resolves: rhbz#1055112 return to 2.0.10 by popular demand

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013 Caolán McNamara <caolanm@redhat.com> - 2.1-4
- Resolves: rhbz#959989 incompatible stripping characters and condition

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 01 2012 Caolán McNamara <caolanm@redhat.com> - 2.1-1
- latest -version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 05 2010 Caolán McNamara <caolanm@redhat.com> - 2.0.10-8
- Resolves: rhbz#648740 revert this, and silence hunspell instead

* Tue Nov 02 2010 Caolán McNamara <caolanm@redhat.com> - 2.0.10-7
- Resolves: rhbz#648740 thousands of trailing empty rules spew

* Sun Apr 04 2010 Caolán McNamara <caolanm@redhat.com> - 2.0.10-6
- mythes now owns /usr/share/mythes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 2.0.10-4
- tidy spec

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 27 2008 Caolán McNamara <caolanm@redhat.com> - 2.0.10-2
- silly require

* Thu Nov 20 2008 Caolán McNamara <caolanm@redhat.com> - 2.0.10-1
- initial version

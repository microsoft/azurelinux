Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package publicsuffix
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2015 yaneti@declera.com
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           publicsuffix
Version:        20201026
Release:        2%{?dist}
Summary:        Cross-vendor public domain suffix database
License:        MPL-2.0
URL:            https://publicsuffix.org/
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  psl-make-dafsa
BuildArch:      noarch

%description
The Public Suffix List is a cross-vendor initiative to provide
an accurate list of domain name suffixes, maintained by the hard work
of Mozilla volunteers and by submissions from registries.
Software using the Public Suffix List will be able to determine where
cookies may and may not be set, protecting the user from being
tracked across sites.

%prep
%autosetup

%build
psl-make-dafsa \
    --input-format=psl \
    --output-format=binary \
    public_suffix_list.dat public_suffix_list.dafsa

%check
make %{?_smp_mflags} test-syntax

%install
install -m 644 -p -D public_suffix_list.dat \
  %{buildroot}/%{_datadir}/%{name}/public_suffix_list.dat
ln -s public_suffix_list.dat %{buildroot}/%{_datadir}/%{name}/effective_tld_names.dat
install -m 644 -p -D public_suffix_list.dafsa \
  %{buildroot}/%{_datadir}/%{name}/public_suffix_list.dafsa

%files
%license LICENSE
%{_datadir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20201026-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Oct 27 2020 andreas.stieger@gmx.de
- Update to version 20201026:
  * gTLD autopull: 2020-10-12
  * Remove algorithmia.com
  * Add azurestaticapps.net dns suffixes
  * Adds *.gateway.dev
  * Add cdn-edges.net
  * Sort Alphabet entries by TLD first and then by SLDD
  * Add service.one as a public suffix
  * Add tlon.network
  * Add iopsys.se
  * The list of Jelastic public domains was extended
  * Add wapblog's domain
  * added localzone.xyz
  * Adds translate.goog and tr-test.goog
  * Add bip.sh
  * Add .tm.dz
  * Add js.wpenginepowered.com
  * Updated comments with new URLs to the different lists of domains
* Sat Sep 12 2020 andreas.stieger@gmx.de
- Update to version 20200909:
  * Update gTLD list to 2020-09-09
  * Add pages.dev
  * Add gsj.bz
  * Added gitapp.si
  * Add small-web.org domain under Small Technology Foundation
  * Update to ICANN and private SLDs on CentralNic registry platform
  * The list of Jelastic public domains was extended
  * Add forte.id
  * Add Danger Science Group domains
  * Switch cloud.metacentrum.cz from suffix to wildcard notation
  * Added mcpe.me
  * Add omniwe.site
  * Add GOV.UK Pay test environment domain
* Fri Aug 14 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 20200810:
  * Add algorithmia.com (#1071)
  * Added Mythic Beasts (#1075)
  * gTLD autopull: 2020-08-07 (#1085)
  * add rdv.to domains for pcarrier.ca Software Inc. (#1039)
  * thingdust AG: added in-house domains of internal services (#1031)
  * Add mcdir.ru and vps.mcdir.ru (#1051)
  * Add na4u.ru to list (#998)
  * gTLD autopull: 2020-07-29 (#1079)
  * gTLD autopull: 2020-07-28 (#1077)
  * add impertrix.com and impertrixcdn.com (#1060)
  * gTLD autopull: 2020-07-18 (#1069)
  * Add 12 sub zones to .br [20200714 update] (#1068)
* Thu Jul 16 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 20200715:
  * Add cn.vu (#987)
  * Add opensocial.site (#1056)
  * Add wpenginepowered.com (#1064)
  * The list of Jelastic public domains was extended. Addition to #1023 (#1063)
  * Update platform.sh (#1061)
  * add pages.wiardweb.com (#1035)
  * Update public_suffix_list.dat (#1036)
  * gTLD autopull: 2020-06-27 (#1059)
  * Removal of education.tas.edu.au (#977)
  * gTLD autopull: 2020-06-24 (#1057)
  * gTLD autopull: 2020-06-20 (#1055)
* Fri Jun 19 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 20200616:
  * Fix broken links in nic.lk (#1053)
  * Remove fastpanel.direct for FASTVPS EESTI OU (#1024)
  * Add gitpage.si to private domains section (#1013)
  * add hostyhosting.io (#1046)
  * Add wien.funkfeuer.at to private section (#1041)
  * Update public_suffix_list.dat (#1029)
  * Update public_suffix_list.dat (#1050)
  * Add plesk.page and pleskns.com suffix to private section (#1048)
  * gTLD autopull: 2020-06-11 (#1049)
  * gTLD autopull: 2020-06-05 (#1047)
  * gTLD autopull: 2020-05-28 (#1045)
  * gTLD autopull: 2020-05-27 (#1044)
  * add g.vbrplsbx.io domain (#994)
  * Jelastic public domains are added (#1023)
  * Add vercel.app and vercel.dev and update now.sh listing in private section (#1019)
  * Add *.backyards.banzaicloud.io and *.banzai.cloud (#1025)
  * add seidat.net private domain (#974)
  * Added gentlentapis.com (#984)
  * Update public_suffix_list.dat (#1037)
  * Remove bitballoon.com and netlify.com (#1020)
  * Add *.owo.codes (#973)
  * Add plesk.page and pdns.page suffix to private section (#1022)
  * Add kasserver.com to Private Section (#1016)
  * Update Linode PSL entries (#1026)
  * Add fly.io suffixes (#1015)
  * Update public_suffix_list.dat (#1000)
  * Add Voxel.sh DNS public suffixes (#1014)
* Mon May 18 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 20200506 (bsc#1171819):
  * gTLD autopull: 2020-05-06 (#1030)
  * Update public_suffix_list.dat (#993)
  * Add shopware.store domain (#958)
  * Add clic2000.net to Private Section (#1010)
  * Add Fabrica apps domain: onfabrica.com (#999)
  * Add dyndns.dappnode.io (#912)
  * Added curv.dev to public_suffix_list.dat (#968)
  * Add panel.gg and daemon.panel.gg (#978)
  * adding sth.ac.at (#997)
  * Add netlify.app (#1012)
  * Added Wiki Link as info resource (#1011)
  * Add schulserver.de, update IServ GmbH contact information (#996)
  * Add conn.uk, copro.uk, couk.me and ukco.me domains (#963)
  * Remove flynnhub.com (#971)
  * Added graphox.us domain (#960)
  * Add domains for FASTVPS EESTI OU (#941)
  * Add platter.dev user app domains (#935)
  * Add playstation-cloud.com (#1006)
  * gTLD autopull: 2020-04-02 (#1005)
  * ACI prefix (#930)
  * Update public_suffix_list.dat (#923)
  * Add toolforge.org and wmcloud.org (#970)
  * gTLD autopull: 2020-03-29 (#1003)
* Sat Mar 28 2020 Andreas Stieger <andreas.stieger@gmx.de>
- Update to version 20200326:
  * aero registry removal
  * Add Mineduc subregistry for public schools: aprendemas.cl
  * Update public_suffix_list.dat - Existing Section
  * gTLD autopull: 2020-03-15
  * Add "urown.cloud" and "dnsupdate.info"
  * Remove site.builder.nu
  * Remove unnecessary trailing whitespace for name.fj
  * Update .eu IDNs to add Greek and URL for Cyrillic
  * Update fj entry
* Tue Feb  4 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 20200201:
  * gTLD autopull: 2020-02-01 (#952)
  * gTLD autopull: 2020-01-31 (#951)
  * Add WoltLab Cloud domains (#947)
  * Add qbuser.com domain (#943)
  * Added senseering domain (#946)
  * Add u.channelsdvr.net to PSL (#950)
  * Add discourse.team (#949)
  * gTLD autopull: 2020-01-06 (#942)
  * gTLD autopull: 2019-12-25 (#939)
  * Urgent removal of eq.edu.au (#924)
  * gTLD autopull: 2019-12-20 (#938)
  * gTLD autopull: 2019-12-11 (#932)
  * Added adobeaemcloud domains (#931)
  * Add Observable domain: observableusercontent.com. (#914)
  * Correct v.ua sorting
  * add v.ua (#919)
  * Add en-root.fr domain (#910)
  * add Datawire private domain (#925)
  * Add amsw.nl private domain to PSL (#929)
  * Add *.on-k3s.io (#922)
  * Add *.r.appspot.com to public suffix list (#920)
  * Added gentapps.com (#916)
  * Add oya.to (#908)
  * Add Group 53, LLC Domains (#900)
  * Add perspecta.cloud (#898)
  * Add 0e.vc to PSL (#896)
  * Add skygearapp.com (#892)
  * Update Hostbip Section (#871)
  * Add qcx.io and *.sys.qcx.io (#868)
  * Add builtwithdark.com to the public suffix list (#857)
  * Add_customer-oci.com (#811)
  * Move out old .ru reserved domains
  * gTLD autopull: 2019-12-02 (#928)
  * gTLD autopull: 2019-11-20 (#926)
* Mon Nov 18 2019 andreas.stieger@gmx.de
- Update to version 20191115:
  * Add gov.scot for Scottish Government
  * update gTLD list to 2019-11-15 state
  * remove go-vip.co, go-vip.net, wpcomstaging.com
* Sat Oct 26 2019 andreas.stieger@gmx.de
- Update to version 20191025:
  * gTLD list updated to 2019-10-24 state
  * Update .so suffix list
  * Add the new TLD .ss
  * Add xn--mgbah1a3hjkrd (موريتانيا)
  * Add lolipop.io
  * Add altervista.org
  * Remove zone.id from list
  * Add new domain to Synology dynamic dns service
* Tue Aug 13 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 20190808:
  * tools: update newgtlds.go to filter removed gTLDs (#860)
  * gTLD autopull: 2019-08-08 (#862)
  * Remove non-public nuernberg.museum nuremberg.museum domains (#859)
  * gTLD autopull: 2019-08-02 (#858)
  * Update public_suffix_list.dat (#825)
  * Update reference as per #855
  * add nic.za
  * Update contact for SymfonyCloud (#854)
  * Add lelux.site (#849)
  * Add *.webhare.dev (#847)
  * Update Hostbip Section (#846)
  * Add Yandex Cloud domains (#850)
  * Add ASEINet domains (#844)
  * Update nymnom section (#771)
  * Add Handshake zones (#796)
  * Add iserv.dev for IServ GmbH (#826)
  * Add trycloudflare.com to Cloudflare's domains (#835)
  * Add shopitsite.com (#838)
  * Add pubtls.org (#839)
  * Add qualifio.com domains (#840)
  * Update newgtlds tooling & associated gTLD data. (#834)
  * Add web.app for Google (#830)
  * Add iobb.net (#828)
  * Add cloudera.site (#829)
* Wed May 29 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 20190529:
  * Add Balena domains (#814)
  * Add KingHost domains (#827)
  * Add dyn53.io (#820)
  * Add azimuth.network and arvo.network (#812)
  * Update .rw domains per ccTLD (#821)
  * Add b-data.io (#759)
  * Add co.bn (#789)
  * Add Zitcom domains (#817)
  * Add Carrd suffixes (#816)
  * Add Linode Suffixes (#810)
  * Add lab.ms (#807)
  * Add wafflecell.com (#805)
  * Add häkkinen.fi (#804)
  * Add prvcy.page (#803)
  * Add SRCF user domains: soc.srcf.net, user.srcf.net (#802)
  * Add KaasHosting (#801)
  * Adding cloud66.zone (#797)
  * Add gehirn.ne.jp and usercontent.jp for Gehirn Inc. (#795)
  * Add Clerk user domains (#791)
  * Add loginline (.app, .dev, .io, .services, .site) (#790)
  * Add wnext.app (#785)
  * Add Hostbip Registry Domains (#770)
  * Add glitch.me (#769)
  * added thingdustdata.com (#767)
  * Add dweb.link (#766)
  * Add onred.one (#764)
  * Add mo-siemens.io (#762)
  * Add Render domains (#761)
  * Add *.moonscale.io (#757)
  * Add Stackhero domain (#755)
  * Add voorloper.cloud (#750)
  * Add repl.co and repl.run (#748)
  * Add edugit.org (#736)
  * Add Hakaran domains (#733)
  * Add barsy.ca (#732)
  * Add Names.of.London Domains (#543)
  * Add nctu.me (#746)
  * Br 201904 update (#809)
  * Delete DOHA
  * Add app.banzaicloud.io (#730)
  * Update .TR (#741)
  * Add Nabu Casa (#781)
  * Added uk0.bigv.io under Bytemark Hosting (#745)
  * Add GOV.UK PaaS client domains (#765)
  * Add discourse.group for Civilized Discourse Construction Kit, Inc. (#768)
  * Add on-rancher.cloud and on-rio.io (#779)
  * Syncloud dynamic dns service (#727)
  * Add git-pages.rit.edu (#690)
  * Add workers.dev (#772)
  * Update .AM (#756)
  * Add go-vip.net. (#793)
  * Add site.builder.nu (#723)
  * Update .FR sectorial domains (#527)
  * Remove ACTIVE
  * Remove SPIEGEL
  * Remove EPOST
  * Remove ZIPPO
  * Remove BLANCO
* Mon Feb 18 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 20190205:
  * Add domains of Individual Network Berlin e.V. (#711)
  * Added bss.design to PSL (#685)
  * Add fastly-terrarium.com (#729)
  * Add Swisscom Application Cloud domains (#698)
  * Update public_suffix_list.dat with api.stdlib.com (#751)
  * Add regional domain for filegear.me (#713)
  * Remove bv.nl (#758)
  * Update public_suffix_list.dat
* Tue Feb 12 2019 Fridrich Strba <fstrba@suse.com>
- Link public_suffix_list.dat to effective_tld_names.dat for the
  purpose of httpcomponents-client
* Fri Jan 18 2019 Tomáš Chvátal <tchvatal@suse.com>
- Do not pull in full python3, psl-make-dafsa already pulls in
  what it needs to generate the things
* Sat Jan  5 2019 astieger@suse.com
- Update to version 20181227:
  * Add run.app and a.run.app to the psl (#681)
  * Add telebit.io .app .xyz (#726)
  * Add Leadpages domains (#731)
  * Add public suffix entries for dapps.earth (#708)
  * Add Bytemark Hosting domains (#620)
  * Remove .STATOIL
  * linter: Expect rules to be in NFKC (#725)
  * Convert list data from NFKD to NFKC (#720)
  * Update LS (#718)
* Tue Oct 30 2018 astieger@suse.com
- Update to version 20181030:
  * Add readthedocs.io (#722)
  * Remove trailing whitespace from L11948 (#721)
  * Add krasnik.pl, leczna.pl, lubartow.pl, lublin.pl, poniatowa.pl
    and swidnik.pl domains to the Public Suffix List (#670)
  * Add instantcloud.cn by Redstar Consultants (#696)
  * Add Fermax and mydobiss.com domain (#706)
  * Add shop.th & online.th (#716)
  * Add siteleaf.net (#655)
  * Add wpcomstaging.com and go-vip.co to the PSL (#719)
* Mon Oct 15 2018 astieger@suse.com
- Update to version 20181003:
  * Remove deleted TLDs (#710)
  * Added apigee.io (#712)
  * Add AWS ElasticBeanstalk Ningxia, CN region (#597)
  * Add Github PULL REQUEST TEMPLATE (#699)
  * Add ong.br 2nd level domain (#707)
* Wed Aug 15 2018 astieger@suse.com
- Update to version 20180813:
  * Update .ID list (#703)
  * Updated .bn ccTLD. Removed wildcard. (#702)
  * Remove stackspace.space from PSL (#691)
  * Remove XPERIA (#697)
* Tue Jul 24 2018 astieger@suse.com
- Update to version 20180719:
  * Remove .IWC
  * Update Kuwait's ccTLD (.kw)
  * htts://www.transip.nl => https://www.transip.nl
  * Remove MEO and SAPO
* Tue May 29 2018 astieger@suse.com
- Update to version 20180523:
  * Remove 1password domains (#632)
  * Add cleverapps.io (Clever Cloud) (#634)
  * Remove .BOOTS
  * Add azurecontainer.io to Microsoft domains (#637)
  * Change the patchnewgtlds tool for the updated .zw domain
  * Add new gTLDs up to 2018-04-17 and new ccTLDs up to 2018-04-17
  * cloud.muni.cz cloud subdomains (#622)
  * Add YunoHost DynDns domains: nohost.me & noho.st (#615)
  * Use a custom token for the newGTLD list (#645)
  * lug.org.uk (#514)
  * Adding xnbay.com,u2.xnbay.com,u2-local.xnbay.com to public_suffix_list.dat. (#506)
  * Adding customer.speedpartner.de (#585)
  * Adding ravendb.net subdomains (#535)
  * Adding own.pm (#544)
  * pcloud.host (#531)
  * Add additional Lukanet Ltd domains (#652)
  * Add zone.id (#575)
  * Add half.host (#571)
  * Update 香港 TLD (#568)
  * Add Now-DNS domains (#560)
  * Added blackbaudcdn.net private domain to PSL (#558)
  * Adding IServ GmbH domains (#552)
  * Add FASTVPS EESTI OU domains (#541)
  * nic.it - update regions and provinces (#524)
  * Update Futureweb OG Private Domains (#520)
  * add United Gameserver virtualuser domains (#600)
  * Add Lightmaker Property Manager, Inc domains (#604)
  * Update Uberspace domains (#616)
  * Add Datto, Inc domains
  * Add memset hosting domains (#625)
  * Add utwente.io (#626)
  * Add bci.dnstrace.pro (#630)
  * Add May First domains (#635)
  * Add Linki Tools domains (#636)
  * Update NymNom domains
  * Add Co & Co domains (#650)
  * Add new gTLDs up to 2018-05-08 (#653)
  * Correct linter issues (#654)
  * Add cnpy.gdn as private domain (#633)
  * Add freedesktop.org (#619)
  * Add Omnibond Systems (#656)
  * Add hasura.app to the list (#668)
  * Update gu ccTLD suffixes (#669)
* Fri Apr  6 2018 mpluskal@suse.com
- Update to version 20180328:
  * Add gwiddle.co.uk (#521)
  * Add ox.rs (#522)
  * Add myjino.ru (#512)
  * Add ras.ru domains (#511)
  * Add AWS ElasticBeanstalk Osaka, JP region (#628)
  * Remove trailing whitespace (#621)
* Tue Mar 13 2018 astieger@suse.com
- Update to version 20180312:
  * Add Cloudeity customer subdomains
  * Removed se.com
  * .br updated - one new city domain barueri.br
- use %%license (bsc#1082318)
* Wed Feb 28 2018 astieger@suse.com
- Update to version 20180223:
  * Add mozilla-iot.org (#605)
* Tue Feb 20 2018 astieger@suse.com
- update to 20180218:
  * Add YesCourse private entry for official.academy
  * Add schokokeks.net
  * Add 2038.io
  * Adding cloud66.ws customer domain for Cloud66
  * Add linkyard.cloud
* Fri Jan 26 2018 astieger@suse.com
- Update to version 20180125:
  * .br updated - 12 new 2nd level city domains
  * Update .ke suffixes to include second-level domains
  * Remove myfusion.cloud domain
* Fri Jan  5 2018 mpluskal@suse.com
- Update to version 20171228:
  * Add Paris region (#579)
  * Fixed alwaysdata.net. (#555)
  * Add Combell domains (#565)
  * Adding scrysec.com (#528)
  * Add Fedora Openshift app domains (#533)
  * Add resin.io device domains to list (#499)
  * Add nh-serv.co.uk to list file (#491)
  * Add 1Password domains (#562)
  * Add s5y.io (#572)
  * Add social domains - NIC.bo (#467)
* Tue Nov  7 2017 astieger@suse.com
- Update to version 20171028:
  * remove .htc TLD (#548)
  * Delete "REMOVED" TLDs (#536)
  * .br updated - 19 new 2nd level city domains (#546)
* Mon Oct  9 2017 mpluskal@suse.com
- Update to version 20170910:
  * Add pixolino.com domain (#456)
  * Add Fancy Bits domains to the PSL (#495)
  * Update AWS Elastic Beanstalk domains. (#484)
  * Add domreg.merit.edu registry (#293)
  * Update WeDeploy/Liferay domains. (#510)
  * Add v-info.info (#508)
  * Add debian.net (#516)
  * .br updated - 18 new 2nd level city domains (#507)
* Fri Aug 18 2017 astieger@suse.com
- Update to version 20170809:
  * Update Futureweb OG Private Domains (#498)
  * Add byen.site (#490)
* Thu Jul 20 2017 astieger@suse.com
- Update to version 20170713:
  * Add newly delegated ICANN ccTLDs based on 2017-07-10 database (#483)
  * Add boomla.net domain (#476)
  * Add Dynu.com domain names to the PSL (#447)
  * Add Netlify domains (#469)
  * add Nodeart domains (#471)
  * Add additional evennode.com domains (#481)
  * Add LiquidNet domains (#452)
  * Add NymNom domains (#425)
  * Add Sub 6 Limited domains (#462)
  * Pull request for adding org.ru, net.ru and pp.ru names (#412)
* Mon Jul  3 2017 astieger@suse.com
- Update to version 20170622:
  * .br updated 2nd level domains + 3rd level gov.br (#464)
  * Adding WeDeploy domains (#420)
  * Add nodum.io aPaas (#431)
  * Add Filegear domain (#434)
  * Add Lukanet Ltd domains (#439)
  * Add metacentrum.cz cloud subdomains (#438)
  * Add flynnhosting.net for Flynn (#459)
  * Add lima-city/TrafficPlex domains (#454)
  * Add mytuleap.com domain (#453)
  * Add lcube-server.de, svn-repos.de, git-repos.de (#455)
  * Added Thingdusts per-user subdomains. (#419)
  * Update XS4ALL domains (#457)
  * Add CloudAccess.net domains (#466)
  * Add info.cx (#460)
  * Add DrayDNS domains (#475)
  * Update GitHub domains
* Mon Jun 12 2017 astieger@suse.com
- Update to version 20170608:
  * Add nom.nc (#305)
  * Add definima domain suffix (#383)
  * Sort by company
  * Delete .ORIENTEXPRESS (#437)
  * Add cloud.goog (#449)
* Tue May  9 2017 astieger@suse.com
- Update to version 20170424:
  * Additional evennode.com domains (#428)
  * Update .zw extensions (#369)
  * Add Ici la Lune hosting domain (#370)
  * Update Daplie, Inc domains (#388)
  * Add XS4ALL Internet bv domains (#397)
  * Add Octopodal Solutions, LLC domains (#404)
  * Add Cloud66 domains (#409)
  * Add A.W. AdvisorWebsites.com Software Inc domains (#413)
  * Add Fedora domains (#414)
  * Add Synology, Inc. domains (#415)
  * Correct Fedora domain sorting
  * Adding IPiFony Systems, Inc. domains (#429)
  * Add Uberspace domains (#432)
  * Add SensioLabs, SAS domains (#423)
  * Update .ar ccTLD (#406)
  * Update .ไทย domains (#408)
  * Add Qutheory, LLC domains (#407)
  * Adding Quip domains (#427)
  * Add eDirect Corp domains (#398)
  * Add bplaced network domains (#433)
  * Add Mail.ru Group domains (#421)
  * Update Platform.sh / Commerce Guys SAS domains (#417)
  * Formatting
* Tue Apr  4 2017 tchvatal@suse.com
- Update to version 20170331:
  * Include fastly.net subdomain for related services (#424)
* Thu Mar 16 2017 astieger@suse.com
- Update to version 20170303:
  * Add new gTLDs up to 2017-02-23 (#405)
  * adding storj.farm for Storj Labs Inc. (#400)
* Fri Feb 10 2017 astieger@suse.com
- Update to version 20170206:
  * Add additional private Fastly domains (#371)
  * Add onion (#386)
  * Removing s3.amazonaws.com wildcard, adding AWS eu-west-2 regional endpoints (#387)
  * Add .RU and .SU geographic suffixes owned by FAITID (#384)
* Sat Jan 14 2017 mpluskal@suse.com
- Update to version 20170105:
  * Add Amune.org to Public Suffix List (#357)
  * Adding TwoDNS TLD's to public_suffix_list.dat (#328)
  * Remove ro.com from Public Suffix List (#346)
  * Add 1gb.ua domains (#353)
  * Add homeoffice.gov.uk (#342)
  * Update list of .RU reserved domains (#359)
  * Add remotewd.com for Western Digital
- Enable syntax checks
* Wed Dec 14 2016 astieger@suse.com
- Update to version 20161211:
  * Remove volgograd.ru from Public Suffix List (#340)
  * Add user.party.eus to PRIVATE section (#348)
  * Adding wildcard for *.s3.amazonaws.com, ca-central-1 AWS region and changing Amazon contact info (#351)
  * Added on-web.fr (Planet-Work shared hosting) (#349)
  * Added .ni as a valid user registerable domain. (#336)
  * Sort .NI
* Sat Dec  3 2016 mpluskal@suse.com
- Update to version 20161128:
  * Update Futureweb OG Private Domains (#332)
  * DynamicDNS and Portmapping Service Feste-IP.net (#295)
  * Added Enonic Cloud domains to list (#330)
  * Added dynamic domains for Yombo (#331)
  * Update Amazon AWS domains (#259)
  * Merge new gTLDs up through 2016-11-29 (#341)
- Use _service for easier updating
* Tue Nov 22 2016 astieger@suse.com
- build compact DAFSA format of the list
* Mon Nov 14 2016 astieger@suse.com
- 2016-11-10 update:
  * Add sinacloud domains: appchizi.com, applinzi.com
  * Add apps.lair.io and stolos.io
  * Add ddnss.org domains
  * Update .JP suffix
  * Add Securepoint Dynamic DNS domains
  * Add now.sh
  * Add shiftedit.io
* Mon Oct 24 2016 astieger@suse.com
- 2016-10-21 update:
  * Update .mz suffixes according to registry
  * Add Futureweb OG Private Domains
  * Add alwaysdata.net
  * Add publishproxy.com
  * Add TAIFUN Software AG domains
  * Add Revitalised Limited domains
  * Add opencraft.hosting
  * Add KnightPoint Systems domain
  * Brazilian .leg.br
  * Add Keyweb AG domains
  * Add ClouDNS domains
  * Add TransIP domains
  * Add .cy suffix
  * Add myfusion.cloud
* Tue Aug 30 2016 astieger@suse.com
- 2016-08-26 update:
  * update .krd
  * Add js.org
  * Move lib.de.us to private section
  * Add wmflabs.orgf
  * Add new gTLSs up to 2016-08-17
  * Add bnr.la
  * Add Joyent Triton
  * Add protonet.io
* Mon Aug  8 2016 astieger@suse.com
- 2016-08-05 update:
  * Add myasustor.com
  * Add myqnapcloud domains
* Mon Aug  1 2016 astieger@suse.com
- 2016-07-31 update:
  * Add meteorapp.com
  * Add Drud domains
  * Add backplaneapp.io
  * Add gitlab.io
  * Add static.land
  * Add stackspace.space
  * Add browsersafetymark.io
* Mon Jul  4 2016 astieger@suse.com
- 2016-07-03 update:
  * Add mycd.eu
  * Add beep.pl
  * Add hepforge.org
  * Add certmgr.org
  * Add fhapp.xyz
  * Update .jp suffixes
  * Add tuxfamily.com
  * Add evennode.com
  * Add realm.cz
  * Add logoip.de, logoip.com
  * Add virtueldomein.nl
  * Add *.magnetosite.cloud
  * Add cyryptonomic.net
  * Correct Amazon AWS EC2 China
  * Add hasura-app.io.
  * Update .BA suffixes
* Fri Jun 10 2016 astieger@suse.com
- 2016-06-10 update:
  * Add spacekit.io
  * Add potager.org domains
  * Add boxfuse.io
* Fri May 27 2016 astieger@suse.com
- 2016-05-25 update:
  * Add No-IP.com's domains
  * Add pgfog.com
  * Add Freebox domains
  * Add e4.cz
  * Add skyhat.io
  * Add dy.fi, tunk.org
  * Update .jp
* Tue May 10 2016 astieger@suse.com
- 2016-05-09 update:
  * Add new gTLDs up to 2016-05-09
  * Add dnshome.de
* Fri Apr 22 2016 astieger@suse.com
- 2016-04-20 update:
  * Add ownprovider.com for OwnProvider
  * Add nerdpol.ovh part of nsupdate.info dyndns service
  * Add townnews customer domain suffixes
  * Add on-aptible.com
  * Add router.management
  * Add compute.estate and alces.network
  * Update .zm TLD
  * Add GoIP DNS Services
  * Add chirurgiens-dentistes-en-france.fr
  * Add myfritz.net for AVM
  * Add nsupdate.info dyndns service
  * Add dedyn.io
  * Google: Add *.0emm.com
  * Add daplie.me
  * Add hzc.io
  * Add new gTLDs up to 2016-04-04
* Thu Mar 31 2016 idonmez@suse.com
- 2016-03-15 update:
  * add .xn--e1a4c, oy.lc
  * add new gTLDs through 2016-03-25
* Sat Mar 12 2016 astieger@suse.com
- 2016-03-10 update:
  * add co.dk, biz.dk, firm.dk, store.dk, reg.dk
  * add cyon.link and cyon.site
  * remove patheon.io, add patheonsite.io
* Sun Mar  6 2016 astieger@suse.com
- 2016-03-02 update:
  * add apps.fbsbx.com
  * update github list
  * add new gTLDs up through 2016-03-01
* Fri Feb 19 2016 astieger@suse.com
- 2016-02-19 update:
  * Add xenapponazure.com to the PSL
  * Add dynv6 dynamic DNS service
  * Add new .pro suffixes
  * Update AWS domains
* Tue Feb  2 2016 psimons@suse.com
- 2016-02-02 update:
  * add *.i.ng
  * update ng reference URL
  * sort entries alphabetically
* Fri Jan 29 2016 astieger@suse.com
- 2016-01-29 update:
  * Add Drobo Dynamic DNS service
  * add TLD .co.cz
  * Minor change for .rs and .срб (xn--90a3ac) domains
  * Add prgmr.com customer domain suffix
* Thu Jan 21 2016 astieger@suse.com
- 2016-01-15 update:
  * Clean-up some inconsistency of data
  * Add additional entries to .GY ccTLD
  * Remove .TP, TLD has been decommissioned
  * Renamed agrica.za to agric.za
* Thu Jan  7 2016 astieger@suse.com
- 2016-01-06 update:
  * Add cloudfunctions.net to Google, Inc. section
  * Add new gTLDs up to 2016-01-04
* Mon Dec  7 2015 astieger@suse.com
- update to 20151205
* Tue Dec  1 2015 astieger@suse.com
- update to 20151130:
  * Remove .an domains from the list (deleted from root zone).
  * Update .ni to have explicit list.
  * Remove taxi.aero, marketplace.aero
* Sun Nov 15 2015 astieger@suse.com
- initial package for openSUSE / SLE based on Fedora spec
- update to 20151112

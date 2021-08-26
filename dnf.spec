%global py3pluginpath %{python3_sitelib}/%{name}-plugins
%global relate_libdnf_version 0.48.0-3

Name:                 dnf
Version:              4.2.23
Release:              6
Summary:              A software package manager that manages packages on Linux distributions.
License:              GPLv2+ and GPLv2 and GPL
URL:                  https://github.com/rpm-software-management/dnf
Source0:              https://github.com/rpm-software-management/dnf/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:               Fix-module-remove-all-when-no-match.patch
Patch1:               Prevent-traceback-catch-ValueError-if-pkg-is-from-cmdline.patch
Patch2:               Check-for-specific-key-string-when-verifing-signatures.patch
Patch3:               Use-rpmkeys-to-verify-package-signature-with-_pkgverify_level.patch
Patch4:               Remove-key-regex-matching-rpm-sprintf-output-varies-too-much.patch
Patch5:               Add-missing-check-if-path-exists-fixes-dead-code.patch
Patch6:               dnf-rpm-miscutils.py-fix-usage-of-_.patch
Patch7:               Pass-the-package-to-rpmkeys-stdin.patch
Patch8:               Use-rpmkeys-alone-to-verify-signature.patch

BuildArch:            noarch
BuildRequires:        cmake gettext systemd bash-completion python3-sphinx
Requires:             python3-%{name} = %{version}-%{release} libreport-filesystem
Recommends:           (%{_bindir}/sqlite3 if bash-completion) (python3-dbus if NetworkManager)
Provides:             dnf-command(alias) dnf-command(autoremove) dnf-command(check-update) dnf-command(clean)
Provides:             dnf-command(distro-sync) dnf-command(downgrade) dnf-command(group)  dnf-command(history)
Provides:             dnf-command(info) dnf-command(install) dnf-command(list) dnf-command(makecache)
Provides:             dnf-command(mark) dnf-command(provides) dnf-command(reinstall) dnf-command(remove)
Provides:             dnf-command(repolist) dnf-command(repoquery) dnf-command(repository-packages)
Provides:             dnf-command(search) dnf-command(updateinfo) dnf-command(upgrade) dnf-command(upgrade-to)
Conflicts:            python2-dnf-plugins-core < 4.0.6 python3-dnf-plugins-core < 4.0.6
Provides:             %{name}-data = %{version}-%{release} %{name}-conf = %{version}-%{release} %{name}-automatic = %{version}-%{release}
Obsoletes:            %{name}-data < %{version}-%{release} %{name}-conf < %{version}-%{release} %{name}-automatic < %{version}-%{release}

%description
DNF is a software package manager that installs, updates, and removespackages
on RPM-based Linux distributions. It automatically computes dependencies and
determines the actions required to install packages.DNF also makes it easier
to maintain groups of machines, eliminating the need to manually update each
one using rpm.

%package -n           yum 
Requires:             %{name} = %{version}-%{release}
Summary:              Package manager 

%description -n       yum
Utility that allows users to manage packages on their systems.\
It supports RPMs, modules and comps groups & environments.

%package -n           python3-%{name}
Summary:              Python 3 interface to DNF
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:        python3-devel python3-hawkey >= 0.48.0 python3-libdnf >= 0.48.0
BuildRequires:        python3-libcomps >= 0.1.8 libmodulemd >= 1.4.0
BuildRequires:        python3-nose python3-gpg python3-rpm >= 4.14.0
Requires:             python3-gpg %{name}-data = %{version}-%{release} libmodulemd >= 1.4.0
Requires:             python3-hawkey >= 0.48.0 python3-libdnf >= %{relate_libdnf_version}
Requires:             python3-libcomps >= 0.1.8 python3-rpm >= 4.14.0
Recommends:           python3-unbound
Obsoletes:	      python2-%{name}

%description -n python3-%{name}
Python 3 interface to DNF.

%package              help
Summary:	      Documents for dnf and yum
Buildarch:	      noarch
Requires:	      man info
Provides:	      yum-help = %{version}-%{release}
Obsoletes:	      yum-help < %{version}-%{release}

%description help
Man pages and other related documents for dnf and yum

%prep
%autosetup -p1
mkdir build-py3

%build
pushd build-py3
%cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python3}
%make_build all doc-man
popd

%install
pushd build-py3
%make_install
popd

%find_lang %{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/vars
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/aliases.d
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/plugins/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.d
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/dnf
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.defaults.d
mkdir -p %{buildroot}%{py3pluginpath}/__pycache__/
mkdir -p %{buildroot}%{_localstatedir}/log/
mkdir -p %{buildroot}%{_var}/cache/dnf/
touch %{buildroot}%{_localstatedir}/log/%{name}.log
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
rm -vf %{buildroot}%{_bindir}/dnf-automatic-*
mv -f %{buildroot}%{_sysconfdir}/%{name}/%{name}-strict.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf %{buildroot}%{_sysconfdir}/yum.conf
ln -sr  %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/yum
mkdir -p %{buildroot}%{_sysconfdir}/yum
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/plugins %{buildroot}%{_sysconfdir}/yum/pluginconf.d
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/protected.d %{buildroot}%{_sysconfdir}/yum/protected.d
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/vars %{buildroot}%{_sysconfdir}/yum/vars

%check
export TERM=linux
pushd build-py3
ctest -VV
popd

%post
%systemd_post dnf-makecache.timer
%systemd_post dnf-automatic.timer
%systemd_post dnf-automatic-notifyonly.timer
%systemd_post dnf-automatic-download.timer
%systemd_post dnf-automatic-install.timer

%preun
%systemd_preun dnf-automatic.timer
%systemd_preun dnf-makecache.timer
%systemd_preun dnf-automatic-notifyonly.timer
%systemd_preun dnf-automatic-download.timer
%systemd_preun dnf-automatic-install.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer
%systemd_postun_with_restart dnf-automatic.timer
%systemd_postun_with_restart dnf-automatic-notifyonly.timer
%systemd_postun_with_restart dnf-automatic-download.timer
%systemd_postun_with_restart dnf-automatic-install.timer

%files
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/%{name}
%{_bindir}/%{name}-automatic
%{_sysconfdir}/bash_completion.d/%{name}
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-makecache.timer
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-makecache.service
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%{_var}/cache/%{name}/
%{python3_sitelib}/%{name}/automatic/
%dir %{_sysconfdir}/%{name} 
%dir %{_sysconfdir}/%{name}/modules.d
%dir %{_sysconfdir}/%{name}/modules.defaults.d
%dir %{_sysconfdir}/%{name}/plugins
%dir %{_sysconfdir}/%{name}/protected.d
%dir %{_sysconfdir}/%{name}/vars
%dir %{_sysconfdir}/%{name}/aliases.d
%exclude %{_sysconfdir}/%{name}/aliases.d/zypper.conf
%config(noreplace) %{_sysconfdir}/%{name}/automatic.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/protected.d/%{name}.conf
%ghost %attr(644,-,-) %{_localstatedir}/log/hawkey.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.librepo.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.rpm.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.plugin.log
%ghost %attr(755,-,-) %dir %{_sharedstatedir}/%{name}
%ghost %attr(644,-,-) %{_sharedstatedir}/%{name}/groups.json
%ghost %attr(755,-,-) %dir %{_sharedstatedir}/%{name}/yumdb
%ghost %attr(755,-,-) %dir %{_sharedstatedir}/%{name}/history
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files -n yum 
%{_bindir}/yum
%{_sysconfdir}/yum/vars
%{_sysconfdir}/yum.conf
%{_sysconfdir}/yum/pluginconf.d
%{_sysconfdir}/yum/protected.d
%config(noreplace) %{_sysconfdir}/%{name}/protected.d/yum.conf

%files -n python3-%{name}
%{_bindir}/%{name}-3
%exclude %{python3_sitelib}/%{name}/automatic
%{python3_sitelib}/%{name}/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__

%files help
%{_datadir}/locale/*
%{_datadir}/bash-completion/*
%{_mandir}/man8/yum.8*
%{_mandir}/man8/yum2dnf.8*
%{_mandir}/man8/%{name}.8*
%{_mandir}/man5/yum.conf.5.*
%{_mandir}/man8/yum-shell.8*
%{_mandir}/man1/yum-aliases.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man7/dnf.modularity.7*
%{_mandir}/man8/%{name}-automatic.8*

%changelog
* Tue Aur 3 2021 Jianmin <jianmin@iscas.ac.cn> - 4.2.23-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove dnf-help dependency

* Thu Jul 15 2021 gaihuiying <gaihuiying1@huawei.com> - 4.2.23-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove recommends rpm-plugins-systemd-inhibit
       backport community patches and fix CVE-2021-3445
       delete duplicate python3-libdnf dependency

* Thu Apr 1 2021 gaihuiying <gaihuiying1@huawei.com> - 4.2.23-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix errors when use "yum module remove --all per:common" command
       fix test test_mode_tty failed

* Fri Nov 20 2020 lunankun <lunankun@huawei.com> - 4.2.23-3
- Type:requirement
- ID:NA
- SUG:NA
- DESC:remove depend deltarpm

* Mon Nov 09 2020 quanhongfei <quanhongfei@huawei.com> - 4.2.23-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:add dnf-help dependency for dnf

* Sat Aug 29 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.23-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade from 4.2.15 to 4.2.23

* Tue Aug 18 2020 chenyaqiang <chenyaqiang@huawei.com> - 2.2.53-8
- rebuild for package build

* Wed Mar 18 2020 songnannan <songnannan2@huawei.com> - 4.2.15-8
- add obsoletes the python2-dnf

* Tue Mar 3 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-7
- modify the patch name

* Thu Feb 27 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-6
- remove extra brace

* Mon Feb 24 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-5
- Revert Fix messages for starting and failing scriptlets

* Fri Feb 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-4
- remove python2

* Fri Jan 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-3
- bug fix format problem

* Mon Jan 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-2
- Package Init

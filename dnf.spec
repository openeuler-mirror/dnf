%bcond_with python2
%bcond_without python3

%if %{with python2}
    %global py2pluginpath %{python2_sitelib}/%{name}-plugins
%endif

%if %{with python3}
    %global py3pluginpath %{python3_sitelib}/%{name}-plugins
%endif

Name:                 dnf
Version:              4.2.15
Release:              3
Summary:              A software package manager that manages packages on Linux distributions.
License:              GPLv2+ and GPLv2 and GPL
URL:                  https://github.com/rpm-software-management/dnf
Source0:              https://github.com/rpm-software-management/dnf/archive/%{version}/%{name}-%{version}.tar.gz

Patch9000:            Bugfix-format-problem.patch

BuildArch:            noarch
BuildRequires:        cmake gettext systemd bash-completion %{_bindir}/sphinx-build-3 %{_bindir}/sphinx-build
Requires:             python3-%{name} = %{version}-%{release} libreport-filesystem python2-%{name} = %{version}-%{release} 
Recommends:           (%{_bindir}/sqlite3 if bash-completion) (python3-dbus if NetworkManager)
Provides:             dnf-command(alias) dnf-command(autoremove) dnf-command(check-update) dnf-command(clean)
Provides:             dnf-command(distro-sync) dnf-command(downgrade) dnf-command(group)  dnf-command(history)
Provides:             dnf-command(info) dnf-command(install) dnf-command(list) dnf-command(makecache)
Provides:             dnf-command(mark) dnf-command(provides) dnf-command(reinstall) dnf-command(remove)
Provides:             dnf-command(repolist) dnf-command(repoquery) dnf-command(repository-packages)
Provides:             dnf-command(search) dnf-command(updateinfo) dnf-command(upgrade) dnf-command(upgrade-to)
Conflicts:            python2-dnf-plugins-core < 4.0.6 python3-dnf-plugins-core < 4.0.6
Provides:             dnf-data %{name}-conf = %{version}-%{release} %{name}-automatic = %{version}-%{release}
Obsoletes:            dnf-data %{name}-conf < %{version}-%{release} %{name}-automatic < %{version}-%{release}

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

%package -n           python2-%{name}
Summary:              Python 2 interface to DNF
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:        python2-devel python2-hawkey >= 0.37.0 python2-libdnf >= 0.37.0
BuildRequires:        python2-libcomps >= 0.1.8 python2-libdnf libmodulemd >= 1.4.0
BuildRequires:        python2-gpg python2-enum34 python2-rpm >= 4.14.0 python2-nose
Requires:             python2-gpg libmodulemd >= 1.4.0 python2-enum34 python2-enum34 python2-libdnf
Requires:             %{name}-data = %{version}-%{release} deltarpm python2-hawkey >= 0.37.0
Requires:             python2-libdnf >= 0.37.0 python2-libcomps >= 0.1.8 python2-rpm >= 4.14.0
Recommends:           rpm-plugin-systemd-inhibit
Conflicts:            dnfdaemon < 0.3.19

%description -n python2-%{name}
Python 2 interface to DNF.

%package -n           python3-%{name}
Summary:              Python 3 interface to DNF
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:        python3-devel python3-hawkey >= 0.37.0 python3-libdnf >= 0.37.0
BuildRequires:        python3-libcomps >= 0.1.8 python3-libdnf libmodulemd >= 1.4.0
BuildRequires:        python3-nose python3-gpg python3-rpm >= 4.14.0
Requires:             python3-gpg %{name}-data = %{version}-%{release} libmodulemd >= 1.4.0
Requires:             deltarpm python3-hawkey >= 0.37.0 python3-libdnf >= 0.37.0
Requires:             python3-libcomps >= 0.1.8 python3-libdnf  python3-rpm >= 4.14.0
Recommends:           python3-unbound rpm-plugin-systemd-inhibit

%description -n python3-%{name}
Python 3 interface to DNF.

%package_help

%prep
%autosetup -p1
mkdir build-py2
mkdir build-py3

%build
%if %{with python2}
    pushd build-py2
    %cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python2}
    %make_build all doc-man
    popd
%endif

%if %{with python3}
    pushd build-py3
    %cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python3}
    %make_build all doc-man
    popd
%endif

%install
%if %{with python2}
    pushd build-py2
    %make_install
    popd
%endif

%if %{with python3}
    pushd build-py3
    %make_install
    popd
%endif

%find_lang %{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/vars
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/aliases.d
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/plugins/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.d
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/dnf
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.defaults.d
mkdir -p %{buildroot}%{py2pluginpath}/
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
%if %{with python2}
    pushd build-py2
    ctest -VV
    popd
%endif

%if %{with python3}
    pushd build-py3
    ctest -VV
    popd
%endif

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

%if %{with python2}
%files -n python2-%{name}
%{_bindir}/%{name}-2
%exclude %{python2_sitelib}/%{name}/automatic
%{python2_sitelib}/%{name}/
%dir %{py2pluginpath}
%endif

%if %{with python3}
%files -n python3-%{name}
%{_bindir}/%{name}-3
%exclude %{python3_sitelib}/%{name}/automatic
%{python3_sitelib}/%{name}/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__
%endif

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
* Fri Jan 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-3
- bug fix format problem

* Mon Jan 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-2
- Package Init

#
Summary:	Enlightened display manager
Summary(pl):	O¶wiecony zarz±dca ekranu
Name:		entrance
Version:	0.9.0.007
Release:	1
License:	BSD
Group:		X11/Applications
Source0:	http://enlightenment.freedesktop.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	b789d09fa76e76a6466a786f0628d0ff
Source1:	%{name}.init
Source2:	%{name}.Xsession
Source3:	%{name}.gen-conf
Patch0:		%{name}-conf.in.patch
Patch1:		%{name}-use_bash.patch
URL:		http://enlightenment.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	edje
BuildRequires:	esmart-devel
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-theme
Requires:	/bin/bash
Requires(post,preun):	/sbin/chkconfig
Requires:	ecore
Requires:	evas-engine-software_x11
Requires:	evas-loader-eet
Requires:	pam
Requires:	sessreg
Requires:	xinitrc-ng
Obsoletes:	X11-xdm
Obsoletes:	kdm
Obsoletes:	gdm
Obsoletes:	wdm
Obsoletes:	xdm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Entrance is the Enlightenment Display Manager. And like Enlightenment,
it takes beauty and customization to levels that KDM and GDM can only
dream about... and without the bloat.

%description -l pl
Entrance to zarz±dca ekranu (Display Manager) dla Enlightenmenta.
Podobnie jak Enlightenment ma piêkno i mo¿liwo¶ci konfiguracji, o
jakich KDM czy GDM mog± tylko pomarzyæ... i to bez narzutu.

%package theme-default
Summary:	Default Entrance theme
Summary(pl):	Domy¶lny motyw Entrance
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-theme

%description theme-default
Default Entrance theme.

%description theme-default -l pl
Domy¶lny motyw Entrance.

%package theme-Nebulous
Summary:	Nebulous Entrance theme
Summary(pl):	Motyw Entrance Nebulous
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-theme

%description theme-Nebulous
Nebulous Entrance theme.

%description theme-Nebulous -l pl
Motyw Entrance Nebulous.

%package theme-darkrock
Summary:	Darkrock Entrance theme
Summary(pl):	Motyw Entrance Darkrock
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-theme

%description theme-darkrock
Darkrock Entrance theme.

%description theme-darkrock -l pl
Motyw Entrance Darkrock.

%package theme-taillights
Summary:	Taillights Entrance theme
Summary(pl):	Motyw Entrance Taillights
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-theme

%description theme-taillights
Taillights Entrance theme.

%description theme-taillights -l pl
Motyw Entrance Taillights.

%prep
%setup -q
# -n %{name}
%patch0 -p1
%patch1 -p1
mv data/images/sessions/enlightenment{,DR17}.png
sed 's/enlightenment.png/enlightenmentDR17.png/' \
	-i data/images/sessions/Makefile.am

sed '/PACKAGE_CFG_DIR/s@"${sysconfdir}"@"${localstatedir}/lib/${PACKAGE}"@' \
	-i configure.in
sed -n '/xsession="You should reconfigure --with-xsession"/!p' \
	-i configure.in

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-xsession=%{_sysconfdir}/X11/%{name}/Xsession
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/X11/%{name},/etc/rc.d/init.d,%{_var}/lib/%{name}}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/entrance
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/X11/%{name}/Xsession
install %{SOURCE3} \
	$RPM_BUILD_ROOT%{_sysconfdir}/X11/%{name}/generate-config
install data/config/build_config.sh.in \
	$RPM_BUILD_ROOT%{_sysconfdir}/X11/%{name}/
touch $RPM_BUILD_ROOT%{_var}/lib/%{name}/entrance_config.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add entrance
if [ -f /var/lock/subsys/entrance ]; then
	echo "Run \"/etc/rc.d/init.d/entrance restart\" to restart entrance." >&2
else
	echo "Run \"/etc/rc.d/init.d/entrance start\" to start entrance." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/entrance ]; then
		/etc/rc.d/init.d/entrance stop >&2
	fi
	/sbin/chkconfig --del entrance
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING* README
%attr(754,root,root) /etc/rc.d/init.d/entrance
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/entrance
%attr(755,root,root) %{_bindir}/entrance*
%attr(755,root,root) %{_sbindir}/entranced
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/images
%dir %{_datadir}/%{name}/themes
%{_datadir}/%{name}/users
%dir %{_sysconfdir}/X11/%{name}
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/%{name}/Xsession
%attr(755,root,root) %{_sysconfdir}/X11/%{name}/generate-config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/%{name}/build_config.sh.in
%dir %{_var}/lib/%{name}
%ghost %{_var}/lib/%{name}/entrance_config.cfg

%files theme-default
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/default.edj

%files theme-Nebulous
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/Nebulous.edj

%files theme-darkrock
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/darkrock.edj

%files theme-taillights
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/taillights.edj

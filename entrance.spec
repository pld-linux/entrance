Summary:	Enlightened display manager
Summary(pl.UTF-8):	Oświecony zarządca ekranu
Name:		entrance
Version:	0.9.0.009
Release:	1
License:	BSD
Group:		X11/Applications
Source0:	http://enlightenment.freedesktop.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	0e3f4d6830431ab7ea4e862c3585fbd0
Source1:	%{name}.init
Source2:	%{name}.Xsession
Source3:	%{name}.gen-conf
Patch0:		%{name}-conf.in.patch
Patch1:		%{name}-use_bash.patch
URL:		http://enlightenment.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1.4
# ecore-evas ecore-file ecore-ipc ecore-config ecore-desktop
BuildRequires:	ecore-devel >= 0.9.9.038
BuildRequires:	edje >= 0.5.0.038
BuildRequires:	edje-devel >= 0.5.0.038
BuildRequires:	esmart-devel >= 0.9.0.008
BuildRequires:	evas-devel >= 0.9.9.038
BuildRequires:	evas-loader-jpeg >= 0.9.9.038
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-theme
#Requires:	/bin/bash
Requires:	ecore >= 0.9.9.038
Requires:	evas-engine-software_x11 >= 0.9.9.038
Requires:	evas-loader-eet >= 0.9.9.038
Requires:	pam
Requires:	sessreg
Requires:	xinitrc-ng
Provides:	XDM
# disappeared from 0.9.0.009
Obsoletes:	entrance-theme-Nebulous < 0.9.0.009
Obsoletes:	entrance-theme-taillights < 0.9.0.009
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Entrance is the Enlightenment Display Manager. And like Enlightenment,
it takes beauty and customization to levels that KDM and GDM can only
dream about... and without the bloat.

%description -l pl.UTF-8
Entrance to zarządca ekranu (Display Manager) dla Enlightenmenta.
Podobnie jak Enlightenment ma piękno i możliwości konfiguracji, o
jakich KDM czy GDM mogą tylko pomarzyć... i to bez narzutu.

%package libs
Summary:	Entrance library
Summary(pl.UTF-8):	Biblioteka Entrance
Group:		X11/Libraries
Requires:	ecore-config >= 0.9.9.038
Requires:	ecore-desktop >= 0.9.9.038
Requires:	ecore-evas >= 0.9.9.038
Requires:	ecore-file >= 0.9.9.038
Requires:	ecore-ipc >= 0.9.9.038

%description libs
Entrance library.

%description libs -l pl.UTF-8
Biblioteka Entrance.

%package devel
Summary:	Header file for Entrance library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki Entrance
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
# ecore-evas ecore-file ecore-ipc ecore-config ecore-desktop
Requires:	ecore-devel >= 0.9.9.038

%description devel
Header file for Entrance library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki Entrance.

%package static
Summary:	Static Entrance library
Summary(pl.UTF-8):	Statyczna biblioteka Entrance
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Entrance library.

%description static -l pl.UTF-8
Statyczna biblioteka Entrance.

%package theme-default
Summary:	Default Entrance theme
Summary(pl.UTF-8):	Domyślny motyw Entrance
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-theme

%description theme-default
Default Entrance theme.

%description theme-default -l pl.UTF-8
Domyślny motyw Entrance.

%package theme-darkrock
Summary:	Darkrock Entrance theme
Summary(pl.UTF-8):	Motyw Entrance Darkrock
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-theme

%description theme-darkrock
Darkrock Entrance theme.

%description theme-darkrock -l pl.UTF-8
Motyw Entrance Darkrock.

%prep
%setup -q
%patch0 -p1
# no-no-no, find real problem
#%patch1 -p1
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
	--with-pam-config=entrance \
	--with-vt=auto \
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
	$RPM_BUILD_ROOT%{_sysconfdir}/X11/%{name}
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

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.edje TODO
%attr(754,root,root) /etc/rc.d/init.d/entrance
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/entrance
%attr(755,root,root) %{_bindir}/entrance
%attr(755,root,root) %{_bindir}/entrance_edit
%attr(755,root,root) %{_bindir}/entrance_edit-config
%attr(755,root,root) %{_bindir}/entrance_wrapper
%attr(755,root,root) %{_sbindir}/entranced
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/entrance_login
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

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libentrance_edit.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libentrance_edit.so
%{_libdir}/libentrance_edit.la
%{_includedir}/Entrance_Edit.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libentrance_edit.a

%files theme-default
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/default.edj

%files theme-darkrock
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/darkrock.edj

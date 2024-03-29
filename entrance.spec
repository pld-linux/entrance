%define		ecore_ver	0.9.9.044
%define		edje_ver	0.9.9.044
%define		efreet_ver	0.0.3.005
%define		esmart_ver	0.9.0.043
%define		evas_ver	0.9.9.044

%define		_snap	20080823

Summary:	Enlightened display manager
Summary(pl.UTF-8):	Oświecony zarządca ekranu
Name:		entrance
Version:	0.9.9.043
Release:	0.%{_snap}.1
License:	BSD
Group:		X11/Applications
Source0:	%{name}-%{version}-%{_snap}.tar.bz2
# Source0-md5:	8c33ec9d4890dab98ad620333cedff1a
Source1:	%{name}.init
Source2:	%{name}.Xsession
URL:		http://enlightenment.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1.6
# ecore ecore-evas ecore-file ecore-ipc ecore-config
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	edje >= %{edje_ver}
BuildRequires:	edje-devel >= %{edje_ver}
BuildRequires:	efreet-devel >= %{efreet_ver}
# esmart_container esmart_text_entry
BuildRequires:	esmart-devel >= %{esmart_ver}
BuildRequires:	evas-devel >= %{evas_ver}
BuildRequires:	evas-loader-jpeg >= %{evas_ver}
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-theme
#Requires:	/bin/bash
Requires:	ecore >= %{ecore_ver}
Requires:	efreet >= %{efreet_ver}
Requires:	evas-engine-software_x11 >= %{evas_ver}
Requires:	evas-loader-eet >= %{evas_ver}
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
Requires:	ecore-config >= %{ecore_ver}
Requires:	ecore-desktop >= %{ecore_ver}
Requires:	ecore-evas >= %{ecore_ver}
Requires:	ecore-file >= %{ecore_ver}
Requires:	ecore-ipc >= %{ecore_ver}

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
Requires:	ecore-devel >= %{ecore_ver}

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
%setup -q -n %{name}-%{version}-%{_snap}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-pam-config=entrance \
	--with-vt=9 \
	--with-xsession=%{_datadir}/%{name}/Xsession \
	--with-xbin=%{_bindir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},/etc/rc.d/init.d}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/entrance
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/entrance/Xsession
install data/config/build_config.sh $RPM_BUILD_ROOT%{_datadir}/%{name}
sed -e 's|./entrance_config.cfg|%{_sysconfdir}/entrance_config.cfg|g' -i $RPM_BUILD_ROOT%{_datadir}/%{name}/build_config.sh
install data/config/entrance_config.cfg $RPM_BUILD_ROOT/%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add entrance
if [ -f /var/lock/subsys/entrance ]; then
	echo "Run \"service entrance restart\" to restart entrance." >&2
else
	echo "Run \"service entrance start\" to start entrance." >&2
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entrance_config.cfg
%attr(755,root,root) %{_datadir}/%{name}/build_config.sh
%attr(755,root,root) %{_datadir}/%{name}/Xsession

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libentrance_edit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libentrance_edit.so.0

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

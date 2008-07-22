# enable_gtkdoc: Toggle if gtkdoc stuff should be rebuilt
#	0 = no
#	1 = yes
%define enable_gtkdoc	0


# Note that this is NOT a relocatable package
%define api_version	2.0
%define lib_major	0
%define lib_name	%mklibname %{name}_ %{lib_major}
%define libgio_name	%mklibname gio%{api_version}_ %{lib_major}
%define develname %mklibname -d %name

Summary:   GIMP Toolkit and GIMP Drawing Kit support library
Name:      glib%{api_version}
Version:   2.17.4
Release: %mkrel 1
License:   LGPLv2+
Group:     System/Libraries
Source0:   ftp://ftp.gnome.org/pub/GNOME/sources/glib/glib-%{version}.tar.bz2
Source1:   glib20.sh
Source2:   glib20.csh
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL:       http://www.gtk.org
Requires:  common-licenses
BuildRequires:	fam-devel
BuildRequires:	libpcre-devel
BuildRequires:  gettext
BuildRequires:	libtool >= 1.4.2-2mdk
BuildRequires: locales-en
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.10
%endif


%description
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

%package common
Summary: data files used by glib
Group: System/Libraries
Conflicts:  %{_lib}glib2.0_0 < 2.12.3-2mdv2007.0

%description common
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

This package contains data used by glib library.

%package -n %{lib_name}
Summary: %{summary}
Group: %{group}
Provides:	glib2 = %{version}-%{release}
Provides:	libglib2 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Conflicts:  libglib1.3_13
Requires:	%{name}-common >= %{version}-%{release}

%description -n %{lib_name}
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

This package contains the library needed to run programs dynamically
linked with the glib.

%package -n %{libgio_name}
Summary: GIO is the input, output and streaming API of glib
Group: %{group}
Requires:	%{lib_name} = %{version}
Suggests:	%mklibname gvfs 0

%description -n %{libgio_name}
GIO is the input, output and streaming API of glib. It on the one hand
provides a set of various streaming classes to access data from different
sources in a convenient way and on the other hand it provides a high level
file system abstraction to access file and directories not only local but also
on the network. For the latter you need to install gvfs.

%package -n %develname
Summary: Static libraries and header files of %{name}
Group:   Development/C
Provides:	glib2-devel = %{version}-%{release}
Provides:	libglib2-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}
Requires:	%{libgio_name} = %{version}
Requires:	glib-gettextize >= %{version}
Conflicts:  libglib1.3_13-devel
Obsoletes: %mklibname -d %{name}_ 0
%description -n %develname
Static libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.


%package -n glib-gettextize
Summary: Gettextize replacement
Group: Development/Other

%description -n glib-gettextize
%{name} package is designed to replace gettextize completely.
Various gettext related files are modified in glib and gtk+ to
allow better and more flexible i18n; however gettextize overwrites
them with its own copy of files, thus nullifying the changes.
If this replacement of gettextize is run instead, then all gnome
packages can potentially benefict from the changes.

%prep
%setup -n glib-%{version} -q

%build

%configure2_5x \
	--with-pcre=system \
	--enable-static \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make

%check
#gw http://bugzilla.gnome.org/show_bug.cgi?id=440544
#make check

%install
rm -rf $RPM_BUILD_ROOT


%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/50glib20.sh
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/50glib20.csh
%find_lang glib20

rm -f %buildroot%_libdir/gio/modules/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libgio_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libgio_name} -p /sbin/ldconfig
%endif

%files common -f glib20.lang
%defattr(-, root, root)
%doc README
%config(noreplace) %{_sysconfdir}/profile.d/*

%files -n %{lib_name}
%defattr(-, root, root)
%doc README
%{_libdir}/libglib-%{api_version}.so.*
%{_libdir}/libgmodule-%{api_version}.so.*
%{_libdir}/libgthread-%{api_version}.so.*
%{_libdir}/libgobject-%{api_version}.so.*

%files -n %{libgio_name}
%defattr(-, root, root)
%{_libdir}/libgio-%{api_version}.so.*
%dir %_libdir/gio/
%dir %_libdir/gio/modules/
%_libdir/gio/modules/libgiofam.so

%files -n %develname
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_libdir}/glib-%{api_version}
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*
%{_datadir}/aclocal/glib-%{api_version}.m4
%{_bindir}/glib-genmarshal
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%_bindir/gtester*

%files -n glib-gettextize
%defattr(-, root, root)
%{_bindir}/glib-gettextize
%{_datadir}/aclocal/glib-gettext.m4
%{_datadir}/glib-%{api_version}



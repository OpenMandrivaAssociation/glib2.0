%define enable_gtkdoc	0

# gw bootstrap: fam pulls glib2, so build without fam
%define bootstrap 0

# Note that this is NOT a relocatable package
%define api_version	2.0
%define lib_major	0
%define lib_name	%mklibname %{name}_ %{lib_major}
%define libgio		%mklibname gio%{api_version}_ %{lib_major}
%define libgmodule	%mklibname gmodule%{api_version}_ %{lib_major}
%define libgthread	%mklibname gthread%{api_version}_ %{lib_major}
%define libgobject	%mklibname gobject%{api_version}_ %{lib_major}
%define develname	%mklibname -d %{name}
%if %{_lib} == lib
%define	bit	32
%else
%define	bit	64
%endif
%define gio	gio2.0-%{bit}

Summary:   GIMP Toolkit and GIMP Drawing Kit support library
Group:     System/Libraries
Name:      glib%{api_version}
Epoch:     1
Version:   2.32.0
Release:   1
License:   LGPLv2+
URL:       http://www.gtk.org
Source0:   ftp://ftp.gnome.org/pub/GNOME/sources/glib/glib-%{version}.tar.xz
Source1:   glib20.sh
Source2:   glib20.csh

%if !%bootstrap
BuildRequires:	pkgconfig(gamin)
%endif
BuildRequires:	pkgconfig(libpcre) >= 8.11
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  gettext
BuildRequires:	libtool >= 1.4.2-2
BuildRequires:	locales-en
%if %enable_gtkdoc
BuildRequires:	pkgconfig(gtk-doc) >= 0.10
%endif
Requires:	pkgconfig(shared-mime-info) >= 0.70

#gw this was required since 2.23.2 (new atomic OPs?)
%define _requires_exceptions GLIBC_PRIVATE

%description
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

%package common
Summary:	data files used by glib
Group:		System/Libraries
Conflicts:	gio2.0_0 < 2.28.4-2

%description common
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

This package contains data used by glib library.

%package -n %{lib_name}
Summary:	%{summary}
Group:		%{group}
Provides:	glib2 = %{epoch}:%{version}-%{release}
Provides:	lib%{name} = %{epoch}:%{version}-%{release}
Conflicts:	%{_lib}gio2.0_0 < 2.28.4-2
Conflicts:	%{develname} < 1:2.31.2

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with libglib.

%package -n %{libgio}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{lib_name} < 1:2.31.2

%description -n %{libgio}
This package contains the library needed to run programs dynamically
linked with libgio.

%package -n %{libgmodule}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{lib_name} < 1:2.31.2

%description -n %{libgmodule}
This package contains the library needed to run programs dynamically
linked with libgmodule.

%package -n %{libgobject}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{lib_name} < 1:2.31.2

%description -n %{libgobject}
This package contains the library needed to run programs dynamically
linked with libgobject.

%package -n %{libgthread}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{lib_name} < 1:2.31.2

%description -n %{libgthread}
This package contains the library needed to run programs dynamically
linked with libgthread.

%package -n %{gio}
Summary:	GIO is the input, output and streaming API of glib
Group:		%{group}
Conflicts:	%{name}-common < 2.23.4-2mdv2010.1
Provides:	gio2.0
Obsoletes:	%{libgio} < 2.28.4-3

%description -n %{gio}
GIO is the input, output and streaming API of glib. It on the one hand
provides a set of various streaming classes to access data from different
sources in a convenient way and on the other hand it provides a high level
file system abstraction to access file and directories not only local but also
on the network. For the latter you need to install gvfs.

%package -n %{develname}
Summary:	Static libraries and header files of %{name}
Group:		Development/C
Requires:	glib-gettextize = %{epoch}:%{version}
Requires:	%{lib_name} = %{epoch}:%{version}
Requires:	%{libgio} = %{epoch}:%{version}
Requires:	%{libgmodule} = %{epoch}:%{version}
Requires:	%{libgobject} = %{epoch}:%{version}
Requires:	%{libgthread} = %{epoch}:%{version}
Provides:	glib2-devel = %{epoch}:%{version}-%{release}
Provides:	libglib2-devel = %{version}-%{release}
#gw for %{_datadir}/glib-%{api_version}/gdb
Conflicts:	glib-gettextize < 2.25.3
Obsoletes:	%mklibname -d %{name}_ 0
Requires: %name-common = %{epoch}:%{version}-%{release}

%description -n %{develname}
Static libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.

%package -n glib-gettextize
Summary:	Gettextize replacement
Group:		Development/Other

%description -n glib-gettextize
%{name} package is designed to replace gettextize completely.
Various gettext related files are modified in glib and gtk+ to
allow better and more flexible i18n; however gettextize overwrites
them with its own copy of files, thus nullifying the changes.
If this replacement of gettextize is run instead, then all gnome
packages can potentially benefict from the changes.

%prep
%setup -qn glib-%{version}

%build
%configure2_5x \
	--with-pcre=system \
	--disable-static \
	--disable-selinux \
	--with-runtime-libdir=../../%{_lib} \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make

%check
#gw http://bugzilla.gnome.org/show_bug.cgi?id=440544
#make check

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/50glib20.sh
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/50glib20.csh
%find_lang glib20

# remove files
find %{buildroot} -name "*.la" -delete
rm -f %{buildroot}%{_libdir}/gio/modules/lib*a

mv %{buildroot}%{_bindir}/gio-querymodules %{buildroot}%{_bindir}/gio-querymodules-%{bit}
mv %{buildroot}%{_mandir}/man1/gio-querymodules.1 %{buildroot}%{_mandir}/man1/gio-querymodules-%{bit}.1

#ghost files
touch %{buildroot}%{_libdir}/gio/modules/giomodule.cache \
      %{buildroot}%{_datadir}/glib-2.0/schemas/gschemas.compiled

# use consistent naming and permissions for completion scriplets
mv %{buildroot}%{_sysconfdir}/bash_completion.d/gdbus-bash-completion.sh \
    %{buildroot}%{_sysconfdir}/bash_completion.d/gdbus

mv %{buildroot}%{_sysconfdir}/bash_completion.d/gsettings-bash-completion.sh \
    %{buildroot}%{_sysconfdir}/bash_completion.d/gsettings

mv %{buildroot}%{_sysconfdir}/bash_completion.d/gresource-bash-completion.sh \
    %{buildroot}%{_sysconfdir}/bash_completion.d/gresource

chmod 644 %{buildroot}%{_sysconfdir}/bash_completion.d/*

#gw at the moment, don't ship these:
rm -f %{buildroot}%{_datadir}/systemtap/tapset/{glib,gobject}.stp


%post -n %{gio}
%{_bindir}/gio-querymodules-%{bit} %{_libdir}/gio/modules 

%triggerin -n %{gio} -- %{_libdir}/gio/modules/*.so
%{_bindir}/gio-querymodules-%{bit} %{_libdir}/gio/modules

%triggerpostun -n %{gio} -- %{_libdir}/gio/modules/*.so
%{_bindir}/gio-querymodules-%{bit} %{_libdir}/gio/modules

%post common
%{_bindir}/glib-compile-schemas --allow-any-name %{_datadir}/glib-2.0/schemas/

%triggerin common -- %{_datadir}/glib-2.0/schemas/*.xml
%{_bindir}/glib-compile-schemas --allow-any-name %{_datadir}/glib-2.0/schemas/

%triggerpostun common -- %{_datadir}/glib-2.0/schemas/*.xml
%{_bindir}/glib-compile-schemas --allow-any-name %{_datadir}/glib-2.0/schemas/

%files common -f glib20.lang
%doc README
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_sysconfdir}/bash_completion.d/gdbus
%{_sysconfdir}/bash_completion.d/gsettings
%{_bindir}/gdbus
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_mandir}/man1/glib-compile-schemas.1*
%{_mandir}/man1/gsettings.1*
%{_mandir}/man1/gdbus.1*
%dir %{_datadir}/glib-2.0/
%dir %{_datadir}/glib-2.0/schemas/
%{_datadir}/glib-2.0/schemas/gschema.dtd
%ghost %{_datadir}/glib-2.0/schemas/gschemas.compiled

%files -n %{libgio}
/%{_lib}/libgio-%{api_version}.so.*

%files -n %{lib_name}
/%{_lib}/libglib-%{api_version}.so.*

%files -n %{libgmodule}
/%{_lib}/libgmodule-%{api_version}.so.*

%files -n %{libgthread}
/%{_lib}/libgthread-%{api_version}.so.*

%files -n %{libgobject}
/%{_lib}/libgobject-%{api_version}.so.*

%files -n %{gio}
%{_bindir}/gio-querymodules-%{bit}
%{_mandir}/man1/gio-querymodules-%{bit}.1*
%if !%bootstrap
%dir %{_libdir}/gio/
%dir %{_libdir}/gio/modules/
%{_libdir}/gio/modules/libgiofam.so
%endif
%ghost %{_libdir}/gio/modules/giomodule.cache

%files -n %{develname}
%doc AUTHORS ChangeLog NEWS
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/lib*.so
%{_libdir}/glib-%{api_version}/include/
%{_libdir}/gdbus-%{api_version}/codegen/
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/gdbus-codegen.1*
%{_mandir}/man1/glib-compile-resources.1*
%{_mandir}/man1/glib-genmarshal.1*
%{_mandir}/man1/glib-mkenums.1*
%{_mandir}/man1/gobject-query.1*
%{_mandir}/man1/gresource.1*
%{_mandir}/man1/gtester-report.1*
%{_mandir}/man1/gtester.1*
%{_datadir}/aclocal/glib-%{api_version}.m4
%{_datadir}/aclocal/gsettings.m4
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/glib-genmarshal
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gresource
%{_bindir}/gtester*
%{_datadir}/gdb/auto-load/%{_lib}/lib*-gdb.py
%{_datadir}/glib-%{api_version}/gdb/
%{_sysconfdir}/bash_completion.d/gresource

%files -n glib-gettextize
%{_bindir}/glib-gettextize
%{_mandir}/man1/glib-gettextize.1*
%{_datadir}/aclocal/glib-gettext.m4
%{_datadir}/glib-%{api_version}/gettext/

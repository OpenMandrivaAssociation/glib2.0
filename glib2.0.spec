%global __requires_exclude bin/python3
%define _python_bytecompile_build 0

%define enable_gtkdoc 0

# gw bootstrap: fam pulls glib2, so build without fam
%bcond_with bootstrap
%bcond_with crosscompile
# As of 2019/08/14 (llvm 9.0.0-rc2),
# PGO breaks things badly ("corrupt input file: version definition index 0 for symbol __gcov_var is out of bounds")
# and doesn't bring much of a performance advantage.
%bcond_with pgo

# (tpg) optimize it a bit
%global optflags %optflags -O3

# Note that this is NOT a relocatable package
%define api 2.0
%define major 0
%define libname %mklibname %{name}_ %{major}
%define libgio %mklibname gio %{api} %{major}
%define libgmodule %mklibname gmodule %{api} %{major}
%define libgthread %mklibname gthread %{api} %{major}
%define libgobject %mklibname gobject %{api} %{major}
%define devname %mklibname -d %{name}
%if "%{_lib}" == "lib"
%define bit 32
%else
%define bit 64
%endif
%define gio gio2.0-%{bit}

Summary:	GIMP Toolkit and GIMP Drawing Kit support library
Name:		glib%{api}
Epoch:		1
Version:	2.63.3
Release:	1
Group:		System/Libraries
License:	LGPLv2+
Url:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glib/%(echo %{version} |cut -d. -f1-2)/glib-%{version}.tar.xz
Source1:	glib20.sh
Source2:	glib20.csh
Patch0:		glib-2.34.1-no-warnings.patch
# (tpg) ClearLinux patches
# (tpg) Doing the malloc_trim every sleep is too much
#Patch10:	memory.patch
#Patch11:	madvise.patch
Patch12:	wakeups.patch
Patch13:	gerror-return-on-null.patch
Patch14:	0001-Remove-debugging-in-gspawn.c.patch
# dont remove it!!!
#Patch15:	disable-tests.patch

BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	dbus
BuildRequires:	glibc-devel
BuildRequires:	gettext
BuildRequires:	locales-en
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	chrpath
BuildRequires:	pkgconfig(libattr)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(libpcre) >= 8.11
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(mount)
BuildRequires:	pkgconfig(libelf)
%if !%{with bootstrap}
BuildRequires:	pkgconfig(gamin)
%endif
%if %{enable_gtkdoc}
BuildRequires:	pkgconfig(gtk-doc) >= 0.10
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
Summary:	Data files used by glib
Group:		System/Libraries
Conflicts:	gio2.0_0 < 2.28.4-2
# for GIO content-type support
Recommends:	shared-mime-info

%description common
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

This package contains data used by glib library.

%package doc
Summary:	Documentation for %{name}
Group:		Books/Computer books
Conflicts:	%{mklibname -d %{name}} < 2.54.3-2

%description doc
Documentation for %{name}.

%package -n %{libname}
Summary:	%{summary}
Group:		%{group}
Provides:	glib2 = %{EVRD}
Conflicts:	%{_lib}gio2.0_0 < 2.28.4-2
Conflicts:	%{devname} < 1:2.31.2

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libglib.

%package -n %{libgio}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{libname} < 1:2.31.2

%description -n %{libgio}
This package contains the library needed to run programs dynamically
linked with libgio.

%package -n %{libgmodule}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{libname} < 1:2.31.2

%description -n %{libgmodule}
This package contains the library needed to run programs dynamically
linked with libgmodule.

%package -n %{libgobject}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{libname} < 1:2.31.2

%description -n %{libgobject}
This package contains the library needed to run programs dynamically
linked with libgobject.

%package -n %{libgthread}
Summary:	%{summary}
Group:		%{group}
Conflicts:	%{libname} < 1:2.31.2

%description -n %{libgthread}
This package contains the library needed to run programs dynamically
linked with libgthread.

%package -n %{gio}
Summary:	GIO is the input, output and streaming API of glib
Group:		%{group}
Conflicts:	%{name}-common < 2.23.4-2mdv2010.1
Provides:	gio2.0 = %{EVRD}
Obsoletes:	%{libgio} < 2.28.4-3

%description -n %{gio}
GIO is the input, output and streaming API of glib. It on the one hand
provides a set of various streaming classes to access data from different
sources in a convenient way and on the other hand it provides a high level
file system abstraction to access file and directories not only local but also
on the network. For the latter you need to install gvfs.

%package -n %{devname}
Summary:	Development libraries and header files of %{name}
Group:		Development/C
Requires:	glib-gettextize = %{EVRD}
Requires:	%{name}-common = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libgio} = %{EVRD}
Requires:	%{libgmodule} = %{EVRD}
Requires:	%{libgobject} = %{EVRD}
Requires:	%{libgthread} = %{EVRD}

%description -n %{devname}
Development libraries and header files for the support library for the GIMP's X
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

%package systemtap
Summary:	Systemtap integration for %{name}
Group:		Development/Other
BuildRequires:	systemtap-devel >= 3.0

%description systemtap
Systemtap integration for %{name}.

%prep
%autosetup -n glib-%{version} -p1

%build
# (tpg) remove pcre as we use system one
rm -rf glib/pcre/*.[ch]

#FIXME (angry)
# GCC build with ldd linker failed with this error:
# error: gfileinfo.c:(.debug_info+0x7D514): has non-ABS relocation R_386_GOTOFF against symbol '.LC40'
# this error is observed on many i686 packages (wine, libvirt) and appeared after changing linker to ldd.
# as temporary solution, switch to GCC (if clang was enabled), if still won't build then use other linker like gold or bfd
# if issue is still present (like in this case), then force "-Wl,-z,notext"
%ifarch %{ix86}
%global ldflags %{ldflags} -Wl,-z,notext
%global ldflags %{ldflags} -fuse-ld=gold
%endif

%if %{with crosscompile}
export glib_cv_stack_grows=no
export glib_cv_uscore=no
export ac_cv_func_posix_getpwuid_r=yes
export ac_cv_func_posix_getgrgid_r=no
%endif

%if %{with pgo}
%meson \
	-Db_pgo=generate \
	-Dman=false \
	--default-library=both \
%if !%{with bootstrap}
	-Dfam=true \
%else
	-Dfam=false \
%endif
	-Dsystemtap=true \
	-Dselinux=disabled \
	-Dinstalled_tests=false \
	-Dtapset_install_dir=%{_datadir}/systemtap \
	-Dgio_module_dir="%{_libdir}/gio/modules"

%meson_build

# (tpg) run performance tests to generate data
./build/tests/gobject/performance

# (tpg) clean build
ninja -C build -t clean

%meson \
	-Db_pgo=use \
	-Dman=true \
	--default-library=both \
%if !%{with bootstrap}
	-Dfam=true \
%else
	-Dfam=false \
%endif
	-Dsystemtap=true \
	-Dselinux=disabled \
	-Dinstalled_tests=false \
	-Dtapset_install_dir=%{_datadir}/systemtap \
	-Dgio_module_dir="%{_libdir}/gio/modules" \
	--reconfigure

%else

%meson \
	-Db_pgo=off \
	-Dman=true \
	--default-library=both \
%if !%{with bootstrap}
	-Dfam=true \
%else
	-Dfam=false \
%endif
	-Dsystemtap=true \
	-Dselinux=disabled \
	-Dinstalled_tests=false \
	-Dtapset_install_dir=%{_datadir}/systemtap \
	-Dgio_module_dir="%{_libdir}/gio/modules"
%endif

%meson_build

%check
#gw http://bugzilla.gnome.org/show_bug.cgi?id=440544
#make check

%install
%meson_install

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/50glib20.sh
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/50glib20.csh
%find_lang glib20

mv %{buildroot}%{_bindir}/gio-querymodules %{buildroot}%{_bindir}/gio-querymodules-%{bit}

#ghost files
mkdir -p %{buildroot}%{_libdir}/gio/modules
touch %{buildroot}%{_libdir}/gio/modules/giomodule.cache %{buildroot}%{_datadir}/glib-2.0/schemas/gschemas.compiled

# bash-completion scripts need not be executable
chmod 644 %{buildroot}%{_datadir}/bash-completion/completions/*

#gw at the moment, don't ship these:
rm -fv %{buildroot}%{_datadir}/systemtap/tapset/{glib,gobject}.stp

# (tpg) delete rpath
chrpath --delete %{buildroot}%{_libdir}/*.so
#chrpath --delete %{buildroot}/%{_lib}/*.so.*

rm -rf  %{buildroot}%{_libexecdir}installed-tests %{buildroot}%{_datadir}/installed-tests

# automatic gschema compilation on rpm installs/removals
%transfiletriggerpostun -n %{name}-common --  %{_datadir}/glib-2.0/schemas/
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas --allow-any-name %{_datadir}/glib-2.0/schemas/
fi

%transfiletriggerin -n %{name}-common --  %_datadir/glib-2.0/schemas/
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas --allow-any-name %{_datadir}/glib-2.0/schemas/
fi

# automatic update of gio module cache
%transfiletriggerpostun -n %{name}-common --  %{_libdir}/gio/modules/
%{_bindir}/gio-querymodules-%{bit} %{_libdir}/gio/modules

%transfiletriggerin -n %{name}-common --  %{_libdir}/gio/modules/
%{_bindir}/gio-querymodules-%{bit} %{_libdir}/gio/modules

%files common -f glib20.lang
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_datadir}/bash-completion/completions/gapplication
%{_datadir}/bash-completion/completions/gdbus
%{_datadir}/bash-completion/completions/gsettings
%{_bindir}/gdbus
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gapplication
%{_mandir}/man1/gapplication.1*
%{_mandir}/man1/glib-compile-schemas.1*
%{_mandir}/man1/gsettings.1*
%{_mandir}/man1/gdbus.1*
%dir %{_datadir}/glib-2.0/
%dir %{_datadir}/glib-2.0/schemas/
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/gettext/its/gschema.its
%{_datadir}/gettext/its/gschema.loc
%ghost %{_datadir}/glib-2.0/schemas/gschemas.compiled

%files -n %{libgio}
%{_libdir}/libgio-%{api}.so.%{major}*

%files -n %{libname}
%{_libdir}/libglib-%{api}.so.%{major}*

%files -n %{libgmodule}
%{_libdir}/libgmodule-%{api}.so.%{major}*

%files -n %{libgthread}
%{_libdir}/libgthread-%{api}.so.%{major}*

%files -n %{libgobject}
%{_libdir}/libgobject-%{api}.so.%{major}*

%files -n %{gio}
%{_bindir}/gio
%{_bindir}/gio-querymodules-%{bit}
%{_bindir}/gio-launch-desktop
%{_mandir}/man1/gio-querymodules*.1*
%{_mandir}/man1/gio.1.*
%{_datadir}/bash-completion/completions/gio
%if !%{with bootstrap}
%dir %{_libdir}/gio/
%dir %{_libdir}/gio/modules/
%{_libdir}/gio/modules/libgiofam.so
%endif
%ghost %{_libdir}/gio/modules/giomodule.cache

%files -n %{devname}
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/glib-genmarshal
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gresource
%{_bindir}/gtester*
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_libdir}/glib-%{api}/include/
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/glib-%{api}.m4
%{_datadir}/gdb/auto-load/%{_libdir}/lib*-gdb.py
%{_datadir}/aclocal/gsettings.m4
%{_datadir}/glib-%{api}/codegen/
%{_datadir}/glib-%{api}/gdb/
%{_datadir}/glib-%{api}/valgrind/
%{_datadir}/bash-completion/completions/gresource
%{_includedir}/*
%{_mandir}/man1/gdbus-codegen.1*
%{_mandir}/man1/glib-compile-resources.1*
%{_mandir}/man1/glib-genmarshal.1*
%{_mandir}/man1/glib-mkenums.1*
%{_mandir}/man1/gobject-query.1*
%{_mandir}/man1/gresource.1*
%{_mandir}/man1/gtester-report.1*
%{_mandir}/man1/gtester.1*

%files -n glib-gettextize
%{_bindir}/glib-gettextize
%{_mandir}/man1/glib-gettextize.1*
%{_datadir}/aclocal/glib-gettext.m4
%{_datadir}/glib-%{api}/gettext/

%files systemtap
#% {_datadir}/systemtap/

%if %{enable_gtkdoc}
%files doc
%doc AUTHORS NEWS README
%doc %{_datadir}/gtk-doc/html/*
%endif

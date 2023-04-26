# glib2.0 is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global __requires_exclude bin/python3
%define _python_bytecompile_build 0

%bcond_with gtkdoc

%bcond_without pgo

# disable LTO as this package provides static libraries
#define _disable_lto 1

# (tpg) optimize it a bit
%global optflags %{optflags} -O3

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

%define lib32name lib%{name}_%{major}
%define lib32gio libgio%{api}_%{major}
%define lib32gmodule libgmodule%{api}_%{major}
%define lib32gthread libgthread%{api}_%{major}
%define lib32gobject libgobject%{api}_%{major}
%define dev32name lib%{name}-devel
%define gio32 gio2.0-32

Summary:	GIMP Toolkit and GIMP Drawing Kit support library
Name:		glib%{api}
Epoch:		1
# Do not upgrade to unstable release. 2.76 is stable, 2.77 unstable. Unstable may change ABI and break a lot of stuff.
Version:	2.76.2
Release:	2
Group:		System/Libraries
License:	LGPLv2+
Url:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glib/%(echo %{version} |cut -d. -f1-2)/glib-%{version}.tar.xz
Source1:	glib20.sh
Source2:	glib20.csh
Patch0:		glib-2.34.1-no-warnings.patch
Patch1:		glib-2.70.0-dont-use-lld-when-hardcoding-bfd-specific-options.patch
# Workaround for -Wcast-function-type-strict strictness with clang >= 16
Patch2:		glib-2.76.1-clang-16.patch
# (tpg) ClearLinux patches
# (tpg) Doing the malloc_trim every sleep is too much
#Patch10:	memory.patch
Patch11:	madvise.patch
Patch12:	wakeups.patch
Patch13:	gerror-return-on-null.patch
Patch14:	0001-meson-Run-atomics-test-on-clang-as-well.patch
#Patch15:	0001-Remove-debugging-in-gspawn.c.patch


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
BuildRequires:	bash-completion
BuildRequires:	dbus-daemon
BuildRequires:	pkgconfig(libattr)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(mount)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(libattr)
%if %{with gtkdoc}
BuildRequires:	pkgconfig(gtk-doc) >= 0.10
%endif
%if %{with compat32}
BuildRequires:	cross-i686-openmandriva-linux-gnu-binutils
BuildRequires:	devel(libpcre2-8)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libelf)
BuildRequires:	devel(libz)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libdbus-1)
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
Provides:	%{name}-devel = %{EVRD}
Provides:	glib2-devel = %{EVRD}
Requires:	glib-gettextize = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}
Provides:	glib2-static-devel = %{EVRD}
Requires:	%{name}-common = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libgio} = %{EVRD}
Requires:	%{libgmodule} = %{EVRD}
Requires:	%{libgobject} = %{EVRD}
Requires:	%{libgthread} = %{EVRD}
Requires:	pkgconfig(libpcre2-8)

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	%{summary} (32-bit)
Group:		%{group}

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked with libglib.

%package -n %{lib32gio}
Summary:	%{summary} (32-bit)
Group:		%{group}

%description -n %{lib32gio}
This package contains the library needed to run programs dynamically
linked with libgio.

%package -n %{lib32gmodule}
Summary:	%{summary} (32-bit)
Group:		%{group}

%description -n %{lib32gmodule}
This package contains the library needed to run programs dynamically
linked with libgmodule.

%package -n %{lib32gobject}
Summary:	%{summary} (32-bit)
Group:		%{group}

%description -n %{lib32gobject}
This package contains the library needed to run programs dynamically
linked with libgobject.

%package -n %{lib32gthread}
Summary:	%{summary} (32-bit)
Group:		%{group}

%description -n %{lib32gthread}
This package contains the library needed to run programs dynamically
linked with libgthread.

%package -n %{gio32}
Summary:	GIO is the input, output and streaming API of glib (32-bit)
Group:		%{group}

%description -n %{gio32}
GIO is the input, output and streaming API of glib. It on the one hand
provides a set of various streaming classes to access data from different
sources in a convenient way and on the other hand it provides a high level
file system abstraction to access file and directories not only local but also
on the network. For the latter you need to install gvfs.

%package -n %{dev32name}
Summary:	Development libraries and header files of %{name} (32-bit)
Group:		Development/C
Requires:	glib-gettextize = %{EVRD}
Requires:	%{name}-common = %{EVRD}
Requires:	%{lib32name} = %{EVRD}
Requires:	%{lib32gio} = %{EVRD}
Requires:	%{lib32gmodule} = %{EVRD}
Requires:	%{lib32gobject} = %{EVRD}
Requires:	%{lib32gthread} = %{EVRD}
Requires:	%{devname} = %{EVRD}
Requires:	devel(libpcre2-8)
Requires:	devel(libz)
Requires:	devel(libmount)
Requires:	devel(libffi)

%description -n %{dev32name}
Development libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.
%endif

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

%if %{with compat32}
# Forcing gcc is a workaround for bogus inline assembly (x86_32 only)
export CC="gcc -m32"
export CXX="g++ -m32"
%meson32 \
	-Dman=false \
	-Dsystemtap=false \
	-Dinstalled_tests=false \
	-Dgio_module_dir="%{_prefix}/lib/gio/modules" \
	-Dbsymbolic_functions=true \
	-Dgtk_doc=false \
	-Dselinux=disabled
# glib has no idea about crosscompiling
sed -i -e 's,ld.bfd,i686-linux-gnu-ld.bfd,g' build32/build.ninja
%ninja_build -C build32
unset CC
unset CXX
%endif

%if %{with pgo}
# (tpg) 2023-04-26
# LLVM Profile Warning: Unable to track new values:
# Running out of static counters.
# Consider using option -mllvm -vp-counters-per-site=<n> to allocate more value profile counters at compile time.
%global __cc %{__cc} -mllvm -vp-counters-per-site=8
%global __cxx %{__cxx} -mllvm -vp-counters-per-site=8

%meson \
	-Db_pgo=generate \
	-Dman=false \
	--default-library=both \
	-Dsystemtap=true \
	-Dselinux=disabled \
	-Dinstalled_tests=false \
	-Dtapset_install_dir=%{_datadir}/systemtap \
%if ! %{with gtkdoc}
	-Dgtk_doc=false \
%endif
	-Dbsymbolic_functions=true \
	-Dgio_module_dir="%{_libdir}/gio/modules"

%meson_build

# (tpg) run performance tests to generate data
./build/gobject/tests/performance/performance

# (tpg) clean build
ninja -C build -t clean

%meson \
	-Db_pgo=use \
	-Dman=true \
	--default-library=both \
	-Dsystemtap=true \
	-Dselinux=disabled \
	-Dinstalled_tests=false \
	-Dtapset_install_dir=%{_datadir}/systemtap \
%if ! %{with gtkdoc}
	-Dgtk_doc=false \
%endif
	-Dbsymbolic_functions=true \
	-Dgio_module_dir="%{_libdir}/gio/modules" \
	--reconfigure

%else

%meson \
	-Db_pgo=off \
	-Dman=true \
	--default-library=both \
	-Dsystemtap=true \
	-Dselinux=disabled \
%if ! %{with gtkdoc}
	-Dgtk_doc=false \
%endif
	-Dbsymbolic_functions=true \
	-Dinstalled_tests=false \
	-Dtapset_install_dir=%{_datadir}/systemtap \
	-Dgio_module_dir="%{_libdir}/gio/modules"
%endif

%meson_build

%check
#gw http://bugzilla.gnome.org/show_bug.cgi?id=440544
#make check

%install
%if %{with compat32}
%ninja_install -C build32
mv %{buildroot}%{_bindir}/gio-querymodules %{buildroot}%{_bindir}/gio-querymodules-32
mkdir -p %{buildroot}%{_prefix}/lib/gio/modules
touch %{buildroot}%{_prefix}/lib/gio/modules/giomodule.cache
chrpath --delete %{buildroot}%{_prefix}/lib/*.so
%endif
%meson_install

%if ! %{with gtkdoc}
# If all dependencies are there, the build process builds part
# of the documentation even if told not to, causing "Installed
# but unpackaged files found" errors.
rm -rf %{buildroot}%{_docdir}/glib-2.0
%endif

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

rm -rf  %{buildroot}%{_libexecdir}/installed-tests %{buildroot}%{_datadir}/installed-tests

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

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
%{_libexecdir}/gio-launch-desktop
%doc %{_mandir}/man1/gapplication.1*
%doc %{_mandir}/man1/glib-compile-schemas.1*
%doc %{_mandir}/man1/gsettings.1*
%doc %{_mandir}/man1/gdbus.1*
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
%doc %{_mandir}/man1/gio-querymodules*.1*
%doc %{_mandir}/man1/gio.1.*
%{_datadir}/bash-completion/completions/gio
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
%doc %{_mandir}/man1/gdbus-codegen.1*
%doc %{_mandir}/man1/glib-compile-resources.1*
%doc %{_mandir}/man1/glib-genmarshal.1*
%doc %{_mandir}/man1/glib-mkenums.1*
%doc %{_mandir}/man1/gobject-query.1*
%doc %{_mandir}/man1/gresource.1*
%doc %{_mandir}/man1/gtester-report.1*
%doc %{_mandir}/man1/gtester.1*

%files -n glib-gettextize
%{_bindir}/glib-gettextize
%doc %{_mandir}/man1/glib-gettextize.1*
%{_datadir}/aclocal/glib-gettext.m4
%{_datadir}/glib-%{api}/gettext/

%files systemtap
#% {_datadir}/systemtap/

%if %{with gtkdoc}
%files doc
%doc NEWS
%doc %{_docdir}/glib-2.0
%endif

%if %{with compat32}
%files -n %{lib32gio}
%{_prefix}/lib/libgio-%{api}.so.%{major}*

%files -n %{lib32name}
%{_prefix}/lib/libglib-%{api}.so.%{major}*

%files -n %{lib32gmodule}
%{_prefix}/lib/libgmodule-%{api}.so.%{major}*

%files -n %{lib32gthread}
%{_prefix}/lib/libgthread-%{api}.so.%{major}*

%files -n %{lib32gobject}
%{_prefix}/lib/libgobject-%{api}.so.%{major}*

%files -n %{gio32}
%{_bindir}/gio-querymodules-32
%dir %{_prefix}/lib/gio/
%dir %{_prefix}/lib/gio/modules/
%ghost %{_prefix}/lib/gio/modules/giomodule.cache

%files -n %{dev32name}
%{_prefix}/lib/lib*.so
%{_prefix}/lib/glib-%{api}/include/
%{_prefix}/lib/pkgconfig/*
%{_datadir}/gdb/auto-load/%{_prefix}/lib/lib*-gdb.py

# automatic update of gio module cache
%transfiletriggerpostun -n %{gio32} --  %{_prefix}/lib/gio/modules/
%{_bindir}/gio-querymodules-32 %{_prefix}/lib/gio/modules

%transfiletriggerin -n %{gio32} --  %{_prefix}/lib/gio/modules/
%{_bindir}/gio-querymodules-32 %{_prefix}/lib/gio/modules
%endif

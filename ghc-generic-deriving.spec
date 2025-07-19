#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	generic-deriving
Summary:	Generic programming library for generalised deriving
Summary(pl.UTF-8):	Biblioteka programowania generycznego do uogólnionych wywodów
Name:		ghc-%{pkgname}
Version:	1.13.1
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a0cddab953bd4d9fa479b16281a14fc0
URL:		http://hackage.haskell.org/package/generic-deriving
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-containers >= 0.1
BuildRequires:	ghc-containers < 0.7
BuildRequires:	ghc-ghc-prim < 1
BuildRequires:	ghc-template-haskell >= 2.4
BuildRequires:	ghc-template-haskell < 2.17
BuildRequires:	ghc-th-abstraction >= 0.3
BuildRequires:	ghc-th-abstraction < 0.4
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-containers-prof >= 0.1
BuildRequires:	ghc-ghc-prim-prof
BuildRequires:	ghc-template-haskell-prof >= 2.4
BuildRequires:	ghc-th-abstraction-prof >= 0.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base >= 4.3
Requires:	ghc-containers >= 0.1
Requires:	ghc-ghc-prim
Requires:	ghc-template-haskell >= 2.4
Requires:	ghc-th-abstraction >= 0.3
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides functionality for generalising the deriving
mechanism in Haskell to arbitrary classes. It was first described in
the paper:

A generic deriving mechanism for Haskell. Jose Pedro Magalhaes, Atze
Dijkstra, Johan Jeuring, and Andres Loeh. Haskell'10.

%description -l pl.UTF-8
Ten pakiet dostarcza mechanizm uogólnionych wywodów w Haskellu dla
dowolych klas. Po raz pierwszy został on opisany w dokumencie:

A generic deriving mechanism for Haskell. Jose Pedro Magalhaes, Atze
Dijkstra, Johan Jeuring, and Andres Loeh. Haskell'10.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.3
Requires:	ghc-containers-prof >= 0.1
Requires:	ghc-ghc-prim-prof
Requires:	ghc-template-haskell-prof >= 2.4
Requires:	ghc-th-abstraction-prof >= 0.3

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Base
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Base/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Base/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Monoid
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Monoid/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Monoid/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Semigroup
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Semigroup/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Semigroup/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/TH
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/TH/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/TH/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Base/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Monoid/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/Semigroup/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Generics/Deriving/TH/*.p_hi
%endif

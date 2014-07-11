# CodeSourcery releases are identified by a date, a release number,
# and a package number for downloading from their web site
%global cs_date        2008q3
%global cs_rel         66
%global cs_pkgnum      10925
%global binutils_ver   2.23

%global processor_arch arm
%global target         %{processor_arch}-none-eabi

Name:           %{target}-binutils-cs
Version:        %{cs_date}.%{cs_rel}
Release:        6%{?dist}
Summary:        GNU Binutils for cross-compilation for %{target} target
Group:          Development/Tools
# Most of the sources are licensed under GPLv3+ with these exceptions:
# LGPLv2+ bfd/hosts/x86-64linux.h, include/demangle.h, include/xregex2.h,
# GPLv2+  gprof/cg_print.h
# BSD     gprof/cg_arcs.h, gprof/utils.c, ld/elf-hints-local.h,
# Public Domain libiberty/memmove.c
License:        GPLv2+ and GPLv3+ and LGPLv2+ and BSD
URL:            http://www.codesourcery.com/sgpp/lite/%{processor_arch}

#we don't use orignal tarball, because it's HUGE
Source0:        binutils-%{cs_date}-%{cs_rel}.tar.bz2
#Source0 origin:
#wget https://sourcery.mentor.com/GNUToolchain/package%{cs_pkgnum}/public/%{target}/%{processor_arch}-%{cs_date}-%{cs_rel}-%{target}.src.tar.bz2
#tar jxvf %{processor_arch}-%{cs_date}-%{cs_rel}-%{target}.src.tar.bz2

Source1:        README.fedora
Patch1:         arm-none-eabi-binutils-cs-2008q3-66-fixtex.patch
Patch2:	        arm-none-eabi-binutils-cs-2008q3-66-stopcheck.patch
BuildRequires:  flex bison ppl-devel cloog-ppl-devel
BuildRequires:  perl-podlators
#BuildRequires: texinfo texinfo-tex
Provides:       %{target}-binutils = %{binutils_ver}

%description
This is a cross-compilation version of GNU Binutils, which can be used to
assemble and link binaries for the %{target} platform.  

This Binutils package is based on the CodeSourcery
%{cs_date}-%{cs_rel} release, which includes improved ARM target
support compared to the corresponding FSF release.  CodeSourcery
contributes their changes to the FSF, but it takes a while for them to
get merged.  For the ARM target, effectively CodeSourcery is upstream
of FSF.

%prep
%setup -q -n binutils-stable
%patch1 -p1
%patch2 -p1
cp -p %{SOURCE1} .

%build
./configure CFLAGS="$RPM_OPT_FLAGS" \
            --target=%{target} \
            --enable-interwork \
            --enable-multilib \
            --disable-nls \
            --disable-shared \
            --disable-threads \
	    --with-gcc --with-gnu-as --with-gnu-ld \
            --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --infodir=%{_infodir} \
            --with-docdir=share/doc/%{name} \
            --disable-werror \
            --with-pkgversion="Fedora %{version}-%{release}" \
            --with-bugurl="https://bugzilla.redhat.com/"
make %{?_smp_mflags}

%check
make check 

%install
make install DESTDIR=%{buildroot}
# these are for win targets only
rm %{buildroot}%{_mandir}/man1/%{target}-{dlltool,nlmconv,windres}.1
# we don't want these as we are a cross version
rm -r %{buildroot}%{_infodir}
rm    %{buildroot}%{_libdir}/libiberty.a
rmdir %{buildroot}%{_libdir}


%files
%defattr(-,root,root,-)
%doc COPYING* ChangeLog README.fedora
%{_prefix}/%{target}
%{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*.1.gz


%changelog
* Fri Aug 23 2013 Michal Hlavinka <mhlavink@redhat.com> - 2013.05.23-6
- updated to 2013.05-23

* Thu Aug 08 2013 Michal Hlavinka <mhlavink@redhat.com> - 2012.09.63-5
- use unversioned docdir (#993677)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.09.63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Michal Hlavinka <mhlavink@redhat.com> - 2012.09.63-3
- add provides, so we can combine CodeSourcery and upstream versions

* Wed Feb 20 2013 Michal Hlavinka <mhlavink@redhat.com> - 2012.09.63-2
- make it build with new texinfo

* Mon Dec 03 2012 Michal Hlavinka <mhlavink@redhat.com> - 2012.09.63-1
- new spec for arm-none-eabi using CodeSourcery release

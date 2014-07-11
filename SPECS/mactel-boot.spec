Name:		mactel-boot
Version:	0.9
Release:	9%{?dist}
Summary:	Intel Mac boot files

Group:		System Environment/Base
License:	GPLv2+
URL:		http://www.codon.org.uk/~mjg59/mactel-boot/
Source:		http://www.codon.org.uk/~mjg59/mactel-boot/%{name}-%{version}.tar.bz2
Source1:	mactel-boot-setup
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

ExclusiveArch:	x86_64

Requires:	coreutils

%description
Files for booting Fedora on Intel-based Apple hardware using EFI.

%prep
%setup -q

%build
make PRODUCTVERSION="Fedora %{fedora}" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -D -m 644 SystemVersion.plist $RPM_BUILD_ROOT/boot/efi/System/Library/CoreServices/SystemVersion.plist
echo "This file is required for booting" >$RPM_BUILD_ROOT/boot/efi/mach_kernel
touch $RPM_BUILD_ROOT/boot/efi/System/Library/CoreServices/boot.efi
touch $RPM_BUILD_ROOT/boot/efi/.VolumeIcon.icns
install -D %{SOURCE1} $RPM_BUILD_ROOT/usr/libexec/mactel-boot-setup

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL
%doc Copyright
/usr/share/man/man1/hfs-bless.1.gz
/boot/efi/mach_kernel
/boot/efi/System/Library/CoreServices/SystemVersion.plist
/usr/sbin/hfs-bless
/usr/libexec/mactel-boot-setup
%attr(0755, root, root) %ghost /boot/efi/System/Library/CoreServices/boot.efi
%attr(0644, root, root) %ghost /boot/efi/.VolumeIcon.icns

%triggerin -- grub-efi grub2-efi fedora-logos generic-logos
/usr/libexec/mactel-boot-setup

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 06 2012 Matthew Garrett <mjg@redhat.com> - 0.9-7
- update mactel-boot-setup for F18

* Mon May 14 2012 Matthew Garrett <mjg@redhat.com> - 0.9-6
- Fix destination path for disk label install

* Wed Apr 25 2012 Matthew Garrett <mjg@redhat.com> - 0.9-5
- Move trigger functionality into an external script

* Thu Apr 19 2012 Matthew Garrett <mjg@redhat.com> - 0.9-4
- Blessing must take place after linking

* Thu Apr 19 2012 Matthew Garrett <mjg@redhat.com> - 0.9-3
- Hardlink the bootloader to boot.efi, rather than symlinking
- Redo the spec file to make better use of macros

* Tue Feb 28 2012 Matthew Garrett <mjg@redhat.com> - 0.9-2
- add support for volume labels

* Tue Feb 07 2012 Matthew Garrett <mjg@redhat.com> - 0.9-1
- new upstream, uses kernel ioctl rather than editing the fs by hand

* Wed Dec 14 2011 Matthew Garrett <mjg@redhat.com> - 0.1-4
- Fix symlinks

* Tue Dec 13 2011 Matthew Garrett <mjg@redhat.com> - 0.1-3
- rename binary to hfs-bless
- make sure writes actually hit disk

* Mon Nov 21 2011 Matthew Garrett <mjg@redhat.com> - 0.1-2
- switch to using triggers
- ensure that the filesystem is HFS+ before running bless

* Fri Nov 18 2011 Matthew Garrett <mjg@redhat.com> - 0.1-1
- initial release

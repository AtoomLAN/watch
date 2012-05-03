Summary: watch
Name: watch 
Version: 1.0.0
Release: 42 
License: Jeroen Habraken
Group: EOS/Extension
Source0: watch.tar
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: Eos-release >= 2:4.9.0
%description 
Arista watch extension
%prep
%setup -q -n watch 
%build
%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/CliPlugin
cp -R Watch.py $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/CliPlugin/
%files
%defattr(755,root,root,-)
/usr/lib/python2.7/site-packages/CliPlugin/Watch.py

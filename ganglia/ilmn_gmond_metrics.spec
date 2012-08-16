Summary:	custom gmond metrics for Illumina
Name:		ilmn_gmond_metrics.spec
Version:	1
Release:	1
Group:		System Environment/Base
Packager:       Todd Hartmann <thartmann@illumina.com>
License:	GPL

%description
Custom gmond metrics for Illumina

%prep

%build

%install

%clean

%files
%defattr(-,root,root,-)
%doc
/opt/ganglia/lib64/ganglia/python_modules/sge_slots.py
/opt/ganglia/etc/conf.d/sge_slots.pyconf
/var/www/html/ganglia/graph.d/sgeslots_report.php

%changelog

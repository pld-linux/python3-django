%define		module	Django

Summary:	The web framework for perfectionists with deadlines
Summary(pl):	Szkielet WWW dla perfekcjonistów z ograniczeniami czasowymi
Name:		python-django
Version:	0.91
Release:	0.2
License:	BSD
Group:		Development/Languages/Python
Source0:	http://media.djangoproject.com/releases/%{version}/Django-%{version}.tar.gz
# Source0-md5:	b1f13aa828c0a564581043658c66ae3d
URL:		http://www.djangoproject.com/
%pyrequires_eq	python
BuildRequires:	python-devel
BuildRequires:	unzip
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Django is a high-level Python Web framework that encourages rapid
development and clean, pragmatic design.

%description -l pl
Django to wysokopoziomowy szkielet dla serwisów WWW w Pythonie
wspieraj±cy szybkie tworzenie i czysty, pragmatyczny projekt.

%prep
%setup -q -n %{module}-%{version}


%build
python ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python ./setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name '*.pyc' -exec rm "{}" ";"
find $RPM_BUILD_ROOT -type f -name '*.pyo' -exec rm "{}" ";"
find $RPM_BUILD_ROOT -type f -exec sed -i -e "s#$RPM_BUILD_ROOT##g" "{}" ";"

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
# %%py_postclean
find $RPM_BUILD_ROOT%{py_sitescriptdir} -type f -name '*.py' -exec rm "{}" ";"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*.* README
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/%{module}*
%{py_sitescriptdir}/django

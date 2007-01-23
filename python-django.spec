%define		module	Django

Summary:	The web framework for perfectionists with deadlines
Summary(pl):	Szkielet WWW dla perfekcjonistów z ograniczeniami czasowymi
Name:		python-django
Version:	0.95.1
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://media.djangoproject.com/releases/0.95/Django-%{version}.tar.gz
# Source0-md5:	07f09d8429916481e09e84fd01e97355
URL:		http://www.djangoproject.com/
BuildRequires:	python-devel
BuildRequires:	python-setuptools >= 0.6-0.c1
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python
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
find $RPM_BUILD_ROOT%{py_sitescriptdir} -type f -name '*.py' -a -not -path '*_template*' -exec rm "{}" ";"
find $RPM_BUILD_ROOT%{py_sitescriptdir} -type f -path '*_template*' -a -name '*.py[oc]' -exec rm "{}" ";"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*.* README
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/%{module}*
%{py_sitescriptdir}/django

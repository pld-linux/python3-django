%define		module	django

Summary:	The web framework for perfectionists with deadlines
Summary(pl.UTF-8):	Szkielet WWW dla perfekcjonistów z ograniczeniami czasowymi
Name:		python-%{module}
Version:	1.4
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://www.djangoproject.com/m/releases/1.4/Django-%{version}.tar.gz
# Source0-md5:	ba8e86198a93c196015df0b363ab1109
Patch0:		%{name}-pyc.patch
URL:		http://www.djangoproject.com/
BuildRequires:	python-devel >= 2.5
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	sphinx-pdg
%pyrequires_eq	python
Suggests:	python-MySQLdb
Suggests:	python-PyGreSQL
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Django is a high-level Python Web framework that encourages rapid
development and clean, pragmatic design.

%description -l pl.UTF-8
Django to wysokopoziomowy szkielet dla serwisów WWW w Pythonie
wspierający szybkie tworzenie i czysty, pragmatyczny projekt.

%package doc
Summary:	Documentation on Django
Summary(de.UTF-8):	Dokumentation zu Django
Summary(es.UTF-8):	Documentación para Django
Summary(fr.UTF-8):	Documentation sur Django
Summary(pl.UTF-8):	Dokumentacja do Django
Group:		Documentation

%description doc
Documentation on Django.

%description doc -l pl.UTF-8
Dokumentacja do Django.

%prep
%setup -q -n Django-%{version}
%patch0 -p1

%build
python ./setup.py build

%{__make} -C docs html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_docdir}

python ./setup.py install \
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

ln -sf python-django-doc-%{version} $RPM_BUILD_ROOT%{_docdir}/python-django-doc
rm -rf docs/_build/html/_sources

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/%{module}*
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/Django-*.egg-info
%endif

%files doc
%defattr(644,root,root,755)
%doc docs/_build/html
%{_docdir}/python-django-doc

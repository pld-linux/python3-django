# Conditional build:
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module

%define		module	django
Summary:	The web framework for perfectionists with deadlines
Summary(pl.UTF-8):	Szkielet WWW dla perfekcjonistów z ograniczeniami czasowymi
Name:		python-%{module}
Version:	1.5.4
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	http://www.djangoproject.com/m/releases/1.5/Django-%{version}.tar.gz
# Source0-md5:	b2685469bb4d1fbb091316e21f4108de
Patch0:		%{name}-pyc.patch
URL:		http://www.djangoproject.com/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-distribute
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	sphinx-pdg
%pyrequires_eq	python
Requires:	python-modules
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

%package -n python3-%{module}
Summary:	The web framework for perfectionists with deadlines
Summary(pl.UTF-8):	Szkielet WWW dla perfekcjonistów z ograniczeniami czasowymi
Group:		Libraries/Python
%pyrequires_eq	python3
Requires:	python3-modules
#Suggests:	python3-MySQLdb  # not available yet
Suggests:	python3-psycopg2

%description -n python3-%{module}
Django is a high-level Python Web framework that encourages rapid
development and clean, pragmatic design.

%description -n python3-%{module} -l pl.UTF-8
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
%{__python} setup.py build
%{__make} -C docs html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_docdir}

%if %{with python2}
%{__python} setup.py install \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT
cp $RPM_BUILD_ROOT%{_bindir}/{django-admin.py,py2-django-admin}
%endif

%if %{with python3}
%{__python3} setup.py install \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT
cp $RPM_BUILD_ROOT%{_bindir}/{django-admin.py,py3-django-admin}
%if %{with python2}
# default to python2 if built
cp $RPM_BUILD_ROOT%{_bindir}/{py2-django-admin,django-admin.py}
%endif
%endif

find $RPM_BUILD_ROOT -type f -name '*.py[co]' | xargs rm
find $RPM_BUILD_ROOT -type f -exec sed -i -e "s#$RPM_BUILD_ROOT##g" "{}" ";"

%if %{with python2}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}

# %%py_postclean (only for python2!)
find $RPM_BUILD_ROOT%{py_sitescriptdir} -type f -name '*.py' -a -not -path '*_template*' | xargs rm
find $RPM_BUILD_ROOT%{py_sitescriptdir} -type f -path '*_template*' -a -name '*.py[oc]' | xargs rm
%endif

%if %{with python3}
%py3_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py3_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%endif

ln -sf python-django-doc-%{version} $RPM_BUILD_ROOT%{_docdir}/python-django-doc
rm -rf docs/_build/html/_sources

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/django-admin.py
%attr(755,root,root) %{_bindir}/py2-django-admin
%{py_sitescriptdir}/%{module}*
%{py_sitescriptdir}/Django-*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%if %{without python2}
%attr(755,root,root) %{_bindir}/django-admin.py
%endif
%attr(755,root,root) %{_bindir}/py3-django-admin
%{py3_sitescriptdir}/%{module}*
%{py3_sitescriptdir}/Django-*.egg-info
%endif

%files doc
%defattr(644,root,root,755)
%doc docs/_build/html
%{_docdir}/python-django-doc

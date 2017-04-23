#
# Conditional build:
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module

%define		module		django
%define		egg_name	Django
Summary:	The web framework for perfectionists with deadlines
Summary(pl.UTF-8):	Szkielet WWW dla perfekcjonistów z ograniczeniami czasowymi
Name:		python-%{module}
# stay on LTS line
# https://www.djangoproject.com/download/#supported-versions
Version:	1.11
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://www.djangoproject.com/m/releases/1.11/Django-%{version}.tar.gz
# Source0-md5:	5008d266f198c2fe761916139162a0c2
URL:		https://www.djangoproject.com/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	sphinx-pdg
Suggests:	python-MySQLdb
Suggests:	python-PyGreSQL
Suggests:	python-devel-tools
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
Suggests:	python3-MySQLdb
Suggests:	python3-devel-tools
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

%build
%if %{with python2}
%py_build
%endif

%{__make} -C docs html
rm -r docs/_build/html/_sources

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean

mv $RPM_BUILD_ROOT%{_bindir}/{django-admin.py,django-admin-2}
ln -s django-admin-2 $RPM_BUILD_ROOT%{_bindir}/py2-django-admin
%endif

%if %{with python3}
%py3_install

mv $RPM_BUILD_ROOT%{_bindir}/{django-admin.py,django-admin-3}
ln -s django-admin-3 $RPM_BUILD_ROOT%{_bindir}/py3-django-admin
%endif

# setup "django-admin" global alias
# this needs to be done after both Python versions are installed
# otherwise file contents would be overwritten via symlink
%if %{with python2}
# default to python2 if built
ln -sf py2-django-admin $RPM_BUILD_ROOT%{_bindir}/django-admin
# default to python2 if built
%else
%if %{with python3}
ln -sf py3-django-admin $RPM_BUILD_ROOT%{_bindir}/django-admin
%endif
%endif

install -d $RPM_BUILD_ROOT%{_docdir}
ln -sf python-django-doc-%{version} $RPM_BUILD_ROOT%{_docdir}/python-django-doc

# don't package .po sources
find \
	%{?with_python2:$RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}} \
	%{?with_python3:$RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}} \
	-name django.po -o \
	-name djangojs.po | xargs rm -v

%find_lang django --all-name

# create %dir directives
# FIXME: move this to find-lang.sh?
sed -rne 's,.* (/.*)/LC_MESSAGES/.*,\1,p' django.lang | sort -u > dirs
>localedirs
while read dir; do
	lang=${dir##*/}
	echo "%lang($lang) %dir $dir/LC_MESSAGES"
done < dirs >> django.lang

find \
	%{?with_python2:$RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}} \
	%{?with_python3:$RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}} \
	-type d -name locale > localedirs
while read ldir; do
	ldir=${ldir#$RPM_BUILD_ROOT}
	echo "%dir $ldir"
	if [ "$(ls $RPM_BUILD_ROOT$ldir/*.py* 2>/dev/null)" ]; then
		echo "$ldir/*.py*"
	fi
	for dir in $RPM_BUILD_ROOT$ldir/*; do
		test -d "$dir" || continue
		dir=${dir#$RPM_BUILD_ROOT}
		lang=${dir##*/}
		echo "%lang($lang) %dir $dir"
		if [ "$(ls $RPM_BUILD_ROOT$dir/*.py* 2>/dev/null)" ]; then
			echo "%lang($lang) $dir/*.py*"
		fi
		if [ "$(ls $RPM_BUILD_ROOT$dir/__pycache__ 2>/dev/null)" ]; then
			echo "%lang($lang) $dir/__pycache__"
		fi
	done
done < localedirs >> django.lang

# separate lang to Python 2 and Python 3 files
%if %{with python2}
grep python2 django.lang > python2-django.lang
%endif
%if %{with python3}
grep python3 django.lang > python3-django.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files -f python2-django.lang
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/django-admin
%attr(755,root,root) %{_bindir}/py2-django-admin
%attr(755,root,root) %{_bindir}/django-admin-2
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}/apps
%{py_sitescriptdir}/%{module}/bin
%{py_sitescriptdir}/%{module}/core
%{py_sitescriptdir}/%{module}/db
%{py_sitescriptdir}/%{module}/dispatch
%{py_sitescriptdir}/%{module}/forms
%{py_sitescriptdir}/%{module}/http
%{py_sitescriptdir}/%{module}/middleware
%{py_sitescriptdir}/%{module}/template
%{py_sitescriptdir}/%{module}/templatetags
%{py_sitescriptdir}/%{module}/test
%{py_sitescriptdir}/%{module}/urls
%{py_sitescriptdir}/%{module}/utils
%{py_sitescriptdir}/%{module}/views

%dir %{py_sitescriptdir}/%{module}/conf
%{py_sitescriptdir}/%{module}/conf/*.py[co]
%{py_sitescriptdir}/%{module}/conf/app_template
%{py_sitescriptdir}/%{module}/conf/project_template
%{py_sitescriptdir}/%{module}/conf/urls

%dir %{py_sitescriptdir}/%{module}/contrib
%dir %{py_sitescriptdir}/%{module}/contrib/admin
%dir %{py_sitescriptdir}/%{module}/contrib/admindocs
%dir %{py_sitescriptdir}/%{module}/contrib/auth
%dir %{py_sitescriptdir}/%{module}/contrib/contenttypes
%dir %{py_sitescriptdir}/%{module}/contrib/flatpages
%dir %{py_sitescriptdir}/%{module}/contrib/gis
%dir %{py_sitescriptdir}/%{module}/contrib/humanize
%dir %{py_sitescriptdir}/%{module}/contrib/messages
%dir %{py_sitescriptdir}/%{module}/contrib/postgres
%dir %{py_sitescriptdir}/%{module}/contrib/redirects
%dir %{py_sitescriptdir}/%{module}/contrib/sessions
%dir %{py_sitescriptdir}/%{module}/contrib/sites
%{py_sitescriptdir}/%{module}/contrib/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/admin/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/admin/migrations
%{py_sitescriptdir}/%{module}/contrib/admin/static
%{py_sitescriptdir}/%{module}/contrib/admin/templates
%{py_sitescriptdir}/%{module}/contrib/admin/templatetags
%{py_sitescriptdir}/%{module}/contrib/admin/views
%{py_sitescriptdir}/%{module}/contrib/admindocs/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/admindocs/templates
%{py_sitescriptdir}/%{module}/contrib/auth/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/auth/common-passwords.txt.gz
%{py_sitescriptdir}/%{module}/contrib/auth/handlers
%{py_sitescriptdir}/%{module}/contrib/auth/management
%{py_sitescriptdir}/%{module}/contrib/auth/migrations
%{py_sitescriptdir}/%{module}/contrib/auth/templates
%{py_sitescriptdir}/%{module}/contrib/auth/tests
%{py_sitescriptdir}/%{module}/contrib/contenttypes/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/contenttypes/management
%{py_sitescriptdir}/%{module}/contrib/contenttypes/migrations
%{py_sitescriptdir}/%{module}/contrib/flatpages/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/flatpages/migrations
%{py_sitescriptdir}/%{module}/contrib/flatpages/templatetags
%{py_sitescriptdir}/%{module}/contrib/gis/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/gis/admin
%{py_sitescriptdir}/%{module}/contrib/gis/db
%{py_sitescriptdir}/%{module}/contrib/gis/forms
%{py_sitescriptdir}/%{module}/contrib/gis/gdal
%{py_sitescriptdir}/%{module}/contrib/gis/geoip
%{py_sitescriptdir}/%{module}/contrib/gis/geoip2
%{py_sitescriptdir}/%{module}/contrib/gis/geometry
%{py_sitescriptdir}/%{module}/contrib/gis/geos
%{py_sitescriptdir}/%{module}/contrib/gis/management
%{py_sitescriptdir}/%{module}/contrib/gis/serializers
%{py_sitescriptdir}/%{module}/contrib/gis/sitemaps
%{py_sitescriptdir}/%{module}/contrib/gis/static
%{py_sitescriptdir}/%{module}/contrib/gis/templates
%{py_sitescriptdir}/%{module}/contrib/gis/utils
%{py_sitescriptdir}/%{module}/contrib/humanize/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/humanize/templatetags
%{py_sitescriptdir}/%{module}/contrib/messages/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/messages/storage
%{py_sitescriptdir}/%{module}/contrib/postgres/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/postgres/aggregates
%{py_sitescriptdir}/%{module}/contrib/postgres/fields
%{py_sitescriptdir}/%{module}/contrib/postgres/forms
%{py_sitescriptdir}/%{module}/contrib/redirects/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/redirects/migrations
%{py_sitescriptdir}/%{module}/contrib/sessions/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/sessions/backends
%{py_sitescriptdir}/%{module}/contrib/sessions/management
%{py_sitescriptdir}/%{module}/contrib/sessions/migrations
%{py_sitescriptdir}/%{module}/contrib/sitemaps
%{py_sitescriptdir}/%{module}/contrib/sites/*.py[co]
%{py_sitescriptdir}/%{module}/contrib/sites/migrations
%{py_sitescriptdir}/%{module}/contrib/staticfiles
%{py_sitescriptdir}/%{module}/contrib/syndication
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module} -f python3-django.lang
%defattr(644,root,root,755)
%doc README.rst
%if %{without python2}
%attr(755,root,root) %{_bindir}/django-admin
%endif
%attr(755,root,root) %{_bindir}/py3-django-admin
%attr(755,root,root) %{_bindir}/django-admin-3
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}/apps
%{py3_sitescriptdir}/%{module}/bin
%{py3_sitescriptdir}/%{module}/core
%{py3_sitescriptdir}/%{module}/db
%{py3_sitescriptdir}/%{module}/dispatch
%{py3_sitescriptdir}/%{module}/forms
%{py3_sitescriptdir}/%{module}/http
%{py3_sitescriptdir}/%{module}/middleware
%{py3_sitescriptdir}/%{module}/template
%{py3_sitescriptdir}/%{module}/templatetags
%{py3_sitescriptdir}/%{module}/test
%{py3_sitescriptdir}/%{module}/urls
%{py3_sitescriptdir}/%{module}/utils
%{py3_sitescriptdir}/%{module}/views

%dir %{py3_sitescriptdir}/%{module}/conf
%{py3_sitescriptdir}/%{module}/conf/*.py
%{py3_sitescriptdir}/%{module}/conf/__pycache__
%{py3_sitescriptdir}/%{module}/conf/app_template
%{py3_sitescriptdir}/%{module}/conf/project_template
%{py3_sitescriptdir}/%{module}/conf/urls

%dir %{py3_sitescriptdir}/%{module}/contrib
%dir %{py3_sitescriptdir}/%{module}/contrib/admin
%dir %{py3_sitescriptdir}/%{module}/contrib/admindocs
%dir %{py3_sitescriptdir}/%{module}/contrib/auth
%dir %{py3_sitescriptdir}/%{module}/contrib/contenttypes
%dir %{py3_sitescriptdir}/%{module}/contrib/flatpages
%dir %{py3_sitescriptdir}/%{module}/contrib/gis
%dir %{py3_sitescriptdir}/%{module}/contrib/humanize
%dir %{py3_sitescriptdir}/%{module}/contrib/messages
%dir %{py3_sitescriptdir}/%{module}/contrib/postgres
%dir %{py3_sitescriptdir}/%{module}/contrib/redirects
%dir %{py3_sitescriptdir}/%{module}/contrib/sessions
%dir %{py3_sitescriptdir}/%{module}/contrib/sites
%{py3_sitescriptdir}/%{module}/contrib/*.py
%{py3_sitescriptdir}/%{module}/contrib/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/admin/*.py
%{py3_sitescriptdir}/%{module}/contrib/admin/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/admin/migrations
%{py3_sitescriptdir}/%{module}/contrib/admin/static
%{py3_sitescriptdir}/%{module}/contrib/admin/templates
%{py3_sitescriptdir}/%{module}/contrib/admin/templatetags
%{py3_sitescriptdir}/%{module}/contrib/admin/views
%{py3_sitescriptdir}/%{module}/contrib/admindocs/*.py
%{py3_sitescriptdir}/%{module}/contrib/admindocs/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/admindocs/templates
%{py3_sitescriptdir}/%{module}/contrib/auth/*.py
%{py3_sitescriptdir}/%{module}/contrib/auth/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/auth/common-passwords.txt.gz
%{py3_sitescriptdir}/%{module}/contrib/auth/handlers
%{py3_sitescriptdir}/%{module}/contrib/auth/management
%{py3_sitescriptdir}/%{module}/contrib/auth/migrations
%{py3_sitescriptdir}/%{module}/contrib/auth/templates
%{py3_sitescriptdir}/%{module}/contrib/auth/tests
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/*.py
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/management
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/migrations
%{py3_sitescriptdir}/%{module}/contrib/flatpages/*.py
%{py3_sitescriptdir}/%{module}/contrib/flatpages/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/flatpages/migrations
%{py3_sitescriptdir}/%{module}/contrib/flatpages/templatetags
%{py3_sitescriptdir}/%{module}/contrib/gis/*.py
%{py3_sitescriptdir}/%{module}/contrib/gis/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/gis/admin
%{py3_sitescriptdir}/%{module}/contrib/gis/db
%{py3_sitescriptdir}/%{module}/contrib/gis/forms
%{py3_sitescriptdir}/%{module}/contrib/gis/gdal
%{py3_sitescriptdir}/%{module}/contrib/gis/geoip
%{py3_sitescriptdir}/%{module}/contrib/gis/geoip2
%{py3_sitescriptdir}/%{module}/contrib/gis/geometry
%{py3_sitescriptdir}/%{module}/contrib/gis/geos
%{py3_sitescriptdir}/%{module}/contrib/gis/management
%{py3_sitescriptdir}/%{module}/contrib/gis/serializers
%{py3_sitescriptdir}/%{module}/contrib/gis/sitemaps
%{py3_sitescriptdir}/%{module}/contrib/gis/static
%{py3_sitescriptdir}/%{module}/contrib/gis/templates
%{py3_sitescriptdir}/%{module}/contrib/gis/utils
%{py3_sitescriptdir}/%{module}/contrib/humanize/*.py
%{py3_sitescriptdir}/%{module}/contrib/humanize/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/humanize/templatetags
%{py3_sitescriptdir}/%{module}/contrib/messages/*.py
%{py3_sitescriptdir}/%{module}/contrib/messages/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/messages/storage
%{py3_sitescriptdir}/%{module}/contrib/postgres/*.py
%{py3_sitescriptdir}/%{module}/contrib/postgres/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/postgres/aggregates
%{py3_sitescriptdir}/%{module}/contrib/postgres/fields
%{py3_sitescriptdir}/%{module}/contrib/postgres/forms
%{py3_sitescriptdir}/%{module}/contrib/redirects/*.py
%{py3_sitescriptdir}/%{module}/contrib/redirects/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/redirects/migrations
%{py3_sitescriptdir}/%{module}/contrib/sessions/*.py
%{py3_sitescriptdir}/%{module}/contrib/sessions/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/sessions/backends
%{py3_sitescriptdir}/%{module}/contrib/sessions/management
%{py3_sitescriptdir}/%{module}/contrib/sessions/migrations
%{py3_sitescriptdir}/%{module}/contrib/sitemaps
%{py3_sitescriptdir}/%{module}/contrib/sites/*.py
%{py3_sitescriptdir}/%{module}/contrib/sites/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/sites/migrations
%{py3_sitescriptdir}/%{module}/contrib/staticfiles
%{py3_sitescriptdir}/%{module}/contrib/syndication

%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%{_docdir}/python-django-doc

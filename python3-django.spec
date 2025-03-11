#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests [1 failure as of 2.2.17]

%define		module		django
%define		egg_name	Django
Summary:	The web framework for perfectionists with deadlines
Summary(pl.UTF-8):	Szkielet WWW dla perfekcjonistów z ograniczeniami czasowymi
Name:		python3-%{module}
# stay on LTS line
# https://www.djangoproject.com/download/#supported-versions
Version:	2.2.28
Release:	3
License:	BSD
Group:		Libraries/Python
Source0:	https://www.djangoproject.com/m/releases/2.2/Django-%{version}.tar.gz
# Source0-md5:	62550f105ef66ac7d08e0126f457578a
URL:		https://www.djangoproject.com/
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.40
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytz
BuildRequires:	python3-selenium
BuildRequires:	python3-sqlparse >= 0.2.2
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg >= 1.6.0
%endif
Suggests:	python3-MySQLdb
Suggests:	python3-PyGreSQL
Suggests:	python3-devel-tools
Conflicts:	python-django < 1.11.29
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

%build
%py3_build

%if %{with tests}
LC_ALL=C.UTF-8 \
PYTHONPATH=$(pwd)/build-3/lib:$(pwd) \
%{__python3} tests/runtests.py --parallel 1
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{django-admin.py,django-admin-3}
ln -s django-admin-3 $RPM_BUILD_ROOT%{_bindir}/py3-django-admin

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' $RPM_BUILD_ROOT%{py3_sitescriptdir}/django/conf/project_template/manage.py-tpl
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' $RPM_BUILD_ROOT%{py3_sitescriptdir}/django/bin/django-admin.py

# setup "django-admin" global alias
ln -sf django-admin-3 $RPM_BUILD_ROOT%{_bindir}/django-admin

%if %{with doc}
install -d $RPM_BUILD_ROOT%{_docdir}
ln -sf python-django-doc-%{version} $RPM_BUILD_ROOT%{_docdir}/python-django-doc
%endif

# don't package .po sources
find \
	%{?with_python2:$RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}} \
	%{?with_python3:$RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}} \
	-name django.po -o \
	-name djangojs.po | xargs %{__rm} -v

%find_lang django --with-django --all-name

# fix after find-lang:
# - remove __pycache__ "language"
# - drop charsets from lang names (django uses non-standard _Charset instead of @charset)
grep -v __pycache__ <django.lang | \
	sed -e 's/lang(sr_Latn)/lang(sr)/;s/lang(zh_Hans)/lang(zh_CN)/;s/lang(zh_Hant)/lang(zh_TW)/' > %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%attr(755,root,root) %{_bindir}/django-admin
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
%dir %{py3_sitescriptdir}/%{module}/conf/locale
%{py3_sitescriptdir}/%{module}/conf/locale/__init__.py
%{py3_sitescriptdir}/%{module}/conf/locale/__pycache__
%{py3_sitescriptdir}/%{module}/conf/project_template
%{py3_sitescriptdir}/%{module}/conf/urls

%dir %{py3_sitescriptdir}/%{module}/contrib
%{py3_sitescriptdir}/%{module}/contrib/*.py
%{py3_sitescriptdir}/%{module}/contrib/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/admin
%{py3_sitescriptdir}/%{module}/contrib/admin/*.py
%{py3_sitescriptdir}/%{module}/contrib/admin/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/admin/locale
%{py3_sitescriptdir}/%{module}/contrib/admin/migrations
%{py3_sitescriptdir}/%{module}/contrib/admin/static
%{py3_sitescriptdir}/%{module}/contrib/admin/templates
%{py3_sitescriptdir}/%{module}/contrib/admin/templatetags
%{py3_sitescriptdir}/%{module}/contrib/admin/views
%dir %{py3_sitescriptdir}/%{module}/contrib/admindocs
%{py3_sitescriptdir}/%{module}/contrib/admindocs/*.py
%{py3_sitescriptdir}/%{module}/contrib/admindocs/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/admindocs/locale
%{py3_sitescriptdir}/%{module}/contrib/admindocs/templates
%dir %{py3_sitescriptdir}/%{module}/contrib/auth
%{py3_sitescriptdir}/%{module}/contrib/auth/*.py
%{py3_sitescriptdir}/%{module}/contrib/auth/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/auth/common-passwords.txt.gz
%{py3_sitescriptdir}/%{module}/contrib/auth/handlers
%dir %{py3_sitescriptdir}/%{module}/contrib/auth/locale
%{py3_sitescriptdir}/%{module}/contrib/auth/management
%{py3_sitescriptdir}/%{module}/contrib/auth/migrations
%{py3_sitescriptdir}/%{module}/contrib/auth/templates
%dir %{py3_sitescriptdir}/%{module}/contrib/contenttypes
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/*.py
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/contenttypes/locale
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/management
%{py3_sitescriptdir}/%{module}/contrib/contenttypes/migrations
%dir %{py3_sitescriptdir}/%{module}/contrib/flatpages
%{py3_sitescriptdir}/%{module}/contrib/flatpages/*.py
%{py3_sitescriptdir}/%{module}/contrib/flatpages/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/flatpages/locale
%{py3_sitescriptdir}/%{module}/contrib/flatpages/migrations
%{py3_sitescriptdir}/%{module}/contrib/flatpages/templatetags
%dir %{py3_sitescriptdir}/%{module}/contrib/gis
%{py3_sitescriptdir}/%{module}/contrib/gis/*.py
%{py3_sitescriptdir}/%{module}/contrib/gis/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/gis/admin
%{py3_sitescriptdir}/%{module}/contrib/gis/db
%{py3_sitescriptdir}/%{module}/contrib/gis/forms
%{py3_sitescriptdir}/%{module}/contrib/gis/gdal
%{py3_sitescriptdir}/%{module}/contrib/gis/geoip2
%{py3_sitescriptdir}/%{module}/contrib/gis/geos
%dir %{py3_sitescriptdir}/%{module}/contrib/gis/locale
%{py3_sitescriptdir}/%{module}/contrib/gis/management
%{py3_sitescriptdir}/%{module}/contrib/gis/serializers
%{py3_sitescriptdir}/%{module}/contrib/gis/sitemaps
%{py3_sitescriptdir}/%{module}/contrib/gis/static
%{py3_sitescriptdir}/%{module}/contrib/gis/templates
%{py3_sitescriptdir}/%{module}/contrib/gis/utils
%dir %{py3_sitescriptdir}/%{module}/contrib/humanize
%{py3_sitescriptdir}/%{module}/contrib/humanize/*.py
%{py3_sitescriptdir}/%{module}/contrib/humanize/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/humanize/locale
%{py3_sitescriptdir}/%{module}/contrib/humanize/templatetags
%dir %{py3_sitescriptdir}/%{module}/contrib/messages
%{py3_sitescriptdir}/%{module}/contrib/messages/*.py
%{py3_sitescriptdir}/%{module}/contrib/messages/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/messages/storage
%dir %{py3_sitescriptdir}/%{module}/contrib/postgres
%{py3_sitescriptdir}/%{module}/contrib/postgres/*.py
%{py3_sitescriptdir}/%{module}/contrib/postgres/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/postgres/aggregates
%{py3_sitescriptdir}/%{module}/contrib/postgres/fields
%{py3_sitescriptdir}/%{module}/contrib/postgres/forms
%{py3_sitescriptdir}/%{module}/contrib/postgres/jinja2
%dir %{py3_sitescriptdir}/%{module}/contrib/postgres/locale
%{py3_sitescriptdir}/%{module}/contrib/postgres/templates
%dir %{py3_sitescriptdir}/%{module}/contrib/redirects
%{py3_sitescriptdir}/%{module}/contrib/redirects/*.py
%{py3_sitescriptdir}/%{module}/contrib/redirects/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/redirects/locale
%{py3_sitescriptdir}/%{module}/contrib/redirects/migrations
%dir %{py3_sitescriptdir}/%{module}/contrib/sessions
%{py3_sitescriptdir}/%{module}/contrib/sessions/*.py
%{py3_sitescriptdir}/%{module}/contrib/sessions/__pycache__
%{py3_sitescriptdir}/%{module}/contrib/sessions/backends
%dir %{py3_sitescriptdir}/%{module}/contrib/sessions/locale
%{py3_sitescriptdir}/%{module}/contrib/sessions/management
%{py3_sitescriptdir}/%{module}/contrib/sessions/migrations
%{py3_sitescriptdir}/%{module}/contrib/sitemaps
%dir %{py3_sitescriptdir}/%{module}/contrib/sites
%{py3_sitescriptdir}/%{module}/contrib/sites/*.py
%{py3_sitescriptdir}/%{module}/contrib/sites/__pycache__
%dir %{py3_sitescriptdir}/%{module}/contrib/sites/locale
%{py3_sitescriptdir}/%{module}/contrib/sites/migrations
%{py3_sitescriptdir}/%{module}/contrib/staticfiles
%{py3_sitescriptdir}/%{module}/contrib/syndication

%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,faq,howto,internals,intro,misc,ref,releases,topics,*.html,*.js}
%{_docdir}/python-django-doc
%endif

from edc_navbar import NavbarItem, site_navbars, Navbar


data_report = Navbar(name='data_report')


data_report.append_item(
    NavbarItem(
        name='home',
        label='Home',
        fa_icon='far fa-user-circle',
        url_name='home_url'))

site_navbars.register(data_report)

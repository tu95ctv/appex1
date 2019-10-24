# -*- coding: utf-8 -*-
{
    'name': "eastlog check expire license certification",

    'summary': """ Has Cron job check expire license and send mail expired license
        """,

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/license_certificate.xml',
        'views/fleet_vehicle.xml',
        'report/license_certificate_report_template.xml',
        'report/license_certificate_report.xml',
        'data/mail_template.xml',
        'data/license_check_cron.xml',
        'demo/demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
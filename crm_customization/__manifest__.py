# -*- coding: utf-8 -*-
{
    'name': "CRM Customization",
    'summary': "Custom email behavior for Contact Us form + CRM Lead enhancements",
    'description': """
        - Override website form submission
        - Capture Contact Us form values
        - Send mail.mail with proper body to company email
        - Avoid duplicate blank mail.message emails
    """,
    'author': "Your Company",
    'version': '1.0',
    'category': 'Sales/CRM',
    'license': 'LGPL-3',
    'depends': [
        'crm',
        'hr_recruitment',
        'website',
    ],
    'data': [],
    'installable': True,
    'application': False,
}

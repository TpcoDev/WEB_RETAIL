# -*- coding: utf-8 -*-
{
    'name': "WS Enrolamiento",
    'description': """
           """,

    'author': "TPCO",
    'website': "http://www.tpco.com",
    'version': '14.20210208',

    # any module necessary for this one to work correctly

    'depends': ['product_expiry'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml'

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}

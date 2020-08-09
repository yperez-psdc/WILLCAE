# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Aprobacion de presupuesto',
    'version': '12.0',
    'category': 'Sales',
    'author': 'PSDC Inc.',
    'sequence': 15,
    'summary': 'Aprobacion de presupuesto',
    'description': """
Administra la aprobacion de presupuestos para poder ser emitidos por correo.
    """,
    'author': 'PSDC Inc. - Jega',
    'website': 'https://www.psdc.com.pa',
    'license': 'LGPL-3',
    'support': 'info@psdc.com.pa',
    'depends': ['base_setup','sale', 'sales_team'],
    'data': [
        'wizard/sale_approval_reason_view.xml',
        'views/res_user_views.xml',
        'views/sale_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

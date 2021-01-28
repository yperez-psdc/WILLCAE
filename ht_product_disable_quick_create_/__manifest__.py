# -*- coding: utf-8 -*-
##############################################################################
#
#    Harhu IT Solutions
#    Copyright (C) 2019-TODAY Harhu IT Solutions(<http://www.harhutech.com>).
#    Author: Harhu IT Solutions(<http://www.harhutech.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Product Disable Quick Create',
    'version': '13.0.0.1.0',
    'summary': "Disable quick creation of product on sale, purchase,invoice,picking and MO line to avoid wrong product creation by users.",
    'author': 'Harhu IT Solutions',
    'maintainer': 'Harhu IT Solutions',
    'contributors': ['Harhu IT Solutions'],
    'website': 'http://www.harhutech.com',
    'live_test_url': 'https://www.harhutech.com/contact.html',
    'depends': ['sale_management', 'purchase', 'account', 'mrp', 'stock'],
    'data': [
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/account_move_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml'
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'images': ['static/description/poster_image.png',
        ],
    'price': 10.00,
    'currency': 'USD',
}

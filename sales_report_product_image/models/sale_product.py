# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_image = fields.Boolean(
        'Con Imagenes', help="""If ticked, you can see the product image in
        report of sale order/quotation""")
    image_sizes = fields.Selection(
        [('image', 'Imagen Grande'), ('image_medium', 'Imagen Mediana'),
         ('image_small', 'Imagen Chica')],
        'Tamaño de imagen', default="image_small",
        help="Image size to be displayed in report")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    image_small = fields.Binary(
        'Product Image', related='product_id.image_1920')

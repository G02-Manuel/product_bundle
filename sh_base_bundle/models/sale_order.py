from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _onchange_order_line_bundle(self):
        if not self.order_line:
            return

        # Usamos un conjunto para seguir los ID de las líneas de los bundles ya procesadas
        processed_bundle_lines = set()

        for line in self.order_line:
            if line.product_id and line.product_id.sh_is_bundle:
                # Evitamos procesar el bundle más de una vez, usando el ID de la línea
                if line.id not in processed_bundle_lines:
                    processed_bundle_lines.add(line.id)

                    # Agrega las líneas de productos del bundle
                    for p in line.product_id.sh_bundle_product_ids:
                        self.order_line += self.order_line.new({
                            'product_id': p.sh_product_id.id,
                            'product_uom': p.sh_uom.id,
                            'product_uom_qty': p.sh_qty,
                            'price_unit': p.sh_bundle_id.list_price,
                        })

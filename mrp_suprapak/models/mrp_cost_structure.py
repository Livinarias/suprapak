# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpCostStructure(models.AbstractModel):
    _inherit = 'report.mrp_account_enterprise.mrp_cost_structure'

    def get_lines(self, productions):
        res = super(MrpCostStructure, self).get_lines(productions)
        ProductProduct = self.env['product.product']
        count = 0
        for product in productions.mapped('product_id'):
            mos = productions.filtered(lambda m: m.product_id == product)
            #get the cost of operations line
            operations_line = []
            Workorders = self.env['mrp.workorder'].search([('production_id', 'in', mos.ids)])
            if Workorders:
                query_str = """SELECT w.operation_id, op.name, partner.name, sum(t.duration), wc.costs_hour, wc.costs_hour_mod, wc.costs_hour_cif, wc.costs_hour_maq
                                FROM mrp_workcenter_productivity t
                                LEFT JOIN mrp_workorder w ON (w.id = t.workorder_id)
                                LEFT JOIN mrp_workcenter wc ON (wc.id = t.workcenter_id )
                                LEFT JOIN res_users u ON (t.user_id = u.id)
                                LEFT JOIN res_partner partner ON (u.partner_id = partner.id)
                                LEFT JOIN mrp_routing_workcenter op ON (w.operation_id = op.id)
                                WHERE t.workorder_id IS NOT NULL AND t.workorder_id IN %s
                                GROUP BY w.operation_id, op.name, partner.name, t.user_id, wc.costs_hour, wc.costs_hour_mod, wc.costs_hour_cif, wc.costs_hour_maq
                                ORDER BY op.name, partner.name
                            """
                self.env.cr.execute(query_str, (tuple(Workorders.ids), ))
                for op_id, op_name, user, duration, cost_hour, cost_hour_mod, costs_hour_cif, costs_hour_maq in self.env.cr.fetchall():
                    operations_line.append([user, op_id, op_name, duration / 60.0, cost_hour, cost_hour_mod, costs_hour_cif, costs_hour_maq])
            res[count]['operations_line'] = operations_line
            #get the cost of raw material effectively used
            raw_material_moves_line = []
            query_str = """SELECT sm.product_id, sm.bom_line_id, abs(SUM(sml.qty_done)), abs(SUM(sm.price_unit))
                             FROM stock_move AS sm
                             INNER JOIN stock_move_line AS sml ON sml.move_id = sm.id
                            WHERE sm.raw_material_production_id in %s AND sm.state != 'cancel' AND sm.product_qty != 0 AND scrapped != 't'
                         GROUP BY sm.bom_line_id, sm.product_id"""
            self.env.cr.execute(query_str, (tuple(mos.ids), ))
            for product_id, bom_line_id, qty, cost in self.env.cr.fetchall():
                raw_material_moves_line.append({
                    'qty': qty,
                    'cost': cost,
                    'product_id': ProductProduct.browse(product_id),
                    'bom_line_id': bom_line_id
                })
            res[count]['raw_material_moves_line'] = raw_material_moves_line
            # Costs before
            cost_planned = []
            mrp_productions = self.env['mrp.production'].browse(mos.ids)
            for mrp in mrp_productions:
                for i, line in enumerate(mrp.finished_move_line_ids):
                    bom_total = 0
                    cost_planned.append({
                        'product': line.product_id,
                        'initial_qty': line.product_uom_qty,
                        'cost': line.product_id.standard_price,
                        'components': None,
                        'total': bom_total,
                    })
                    components = []
                    for bom_line in mrp.bom_id.bom_line_ids:
                        components.append({
                            'product': bom_line.product_id,
                            'qty': bom_line.product_qty * cost_planned[i]['initial_qty'],
                            'cost': bom_line.product_id.standard_price * cost_planned[i]['initial_qty'],
                            'BoM_cost': bom_line.product_id.standard_price,
                        })
                        bom_total += bom_line.product_id.standard_price
                    cost_planned[i]['components'] = components
                    cost_planned[i]['total'] += bom_total
            res[count]['cost_planned'] = cost_planned
            count += 1
        return res

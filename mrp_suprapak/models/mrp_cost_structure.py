# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpCostStructure(models.AbstractModel):
    _inherit = 'report.mrp_account_enterprise.mrp_cost_structure'

    def get_lines(self, productions):
        res = super(MrpCostStructure, self).get_lines(productions)
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
            count += 1
        return res

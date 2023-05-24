from time import strftime

from odoo import models, fields, api, _, tools
from odoo.http import request
from datetime import date

import datetime


class ReportLineFields(models.Model):
    _inherit = "account.move.line"

    ctn = fields.Char("Qty in CTN", store=True, force_save="1" )

    # @api.onchange('ctn')
    # def onchange_compute_ctn(self):
    #     for q in self:
    #         q.ctn = q.ctn




class SaleDeliveryReport(models.Model):
    _inherit = "sale.order.line"

    mo_date = fields.Date("MFG Date")
    pack = fields.Char("Pack Numbers")
    qtyp = fields.Float("QTY in Pkg")
    pkts = fields.Char(related='product_id.pkt_ctn',string="Pkts/CTN")
    net = fields.Char(related='product_id.net_ctn', string="Net Wt/CTN")
    total_net = fields.Char( string= "Total Net Wt in KGS")
    grs = fields.Char(related='product_id.gross_ctn',string="Gross Wt/CTN")
    total_grs = fields.Float("Total GRS Wt in KGS")
    batch = fields.Char("Batch No")
    exp = fields.Date("EXP date")



    @api.onchange('qtyp')
    def onchange_compute_total_net(self):
        for line in self:
            total_net_val = float(line.net) * float(line.qtyp)
            line.total_net = round(total_net_val,2)

    @api.onchange('qtyp')
    def onchange_compute_total_grs(self):
        for line in self:
            total_val_grs = float(line.grs) * float(line.qtyp)
            line.total_grs = round(total_val_grs,2)






class ItemMasterInherit(models.Model):
    _inherit = "product.template"

    pkt_ctn = fields.Char("Pkts/CTN")
    net_ctn = fields.Char("Net Wt/CTN")
    gross_ctn = fields.Char("Gross Wt/CTN")



class LotNumberDate(models.Model):
    _inherit = "stock.production.lot"

    dated = fields.Date(compute='onchange_compute_date',string="Date")

    # @api.onchange('product_id')
    def onchange_compute_date(self):
        for lot in self:
            creation_date = lot.create_date
            new_date = (creation_date + datetime.timedelta(days=2 * 365)).strftime('%Y-%m-%d')
            lot.dated =new_date




class LocationAddress(models.Model):
    _inherit = "stock.location"

    address = fields.Many2one("res.partner" , string="Address")

















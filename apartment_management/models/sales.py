from odoo import api,models, fields,_


class ApartmentRecord(models.Model):
    _name = "apartment.sales"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    cname = fields.Many2one('apartment.customer',string='Customer Name')
    name_seq = fields.Char(string='Sales Id', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))
    date = fields.Date(string='Invoice Date')
    addres = fields.Char(string='GST IN')
    phone = fields.Selection([('o', 'One Time'), ('e', 'EMI'), ('r', 'Rental')],string='Payment Terms')
    method = fields.Selection([('c', 'Cash'), ('ca', 'Card'), ('ch', 'Cheque')],string='Payment Method')
    spersn = fields.Many2one('apartment.salesteam',string='Sales Person')
    name = fields.Many2one('apartment.flats',string='Flat name',domain="[('state','=','un'),('projname','=',projname)]")
    projname = fields.Many2one('apartment.configuration', string='Project Name')
    # projname = fields.Many2one(string='Project Name',related='name.projname')
    bloname = fields.Many2one(string='Block Name',related='name.bloname')
    floor = fields.Many2one(string='Floor Name',related='name.floor')
    utype = fields.Many2one(string='Unit Name',related='name.utype')
    price = fields.Char(string='Price',related='name.price')
    serv = fields.Char(string='Service cost')
    main = fields.Char(string='Maintanance Cost')
    # camount = fields.Many2one('apartment.enquiry.camount',string='Commission Amount')
    # def action_open_customer(self):
    #     return {
    #         'name': _('Customer'),
    #         'domain': [('name', '=', self.id)],
    #         'res_model': 'apartment.customer',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'type': 'ir.actions.act_window',
    #     }


    @api.model
    def create(self, vals):
        # if not vals.get('note'):
        #         vals['note'] = 'New Patient'

        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('apartment.sales') or _('New')
        res = super(ApartmentRecord, self).create(vals)
        return res

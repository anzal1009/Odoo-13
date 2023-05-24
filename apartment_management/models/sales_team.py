from odoo import api,models, fields,_


class ApartmentRecord(models.Model):
    _name = "apartment.salesteam"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Employee Name')
    name_seq = fields.Char(string='Emp Id', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))
    addres = fields.Text(string='Address')
    phone = fields.Char(string='Mobile No')
    dept = fields.Selection([('s', 'Sales'), ('a', 'Accounting'), ('c', 'Customer Care')], string='Department')
    email = fields.Char(string='Email Id')
    # commission =fields.Many2one('apartment.enquiry.cpercent',string='Commission')

    data_line = fields.One2many('apartment.salesteam.lines','data',string='Data Line')

    sales_count = fields.Integer(string='Sales Count', compute='_compute_sales_count')

    def _compute_sales_count(self):
        sales_count = self.env['apartment.enquiry'].search_count([('sperson', '=', self.id)])
        self.sales_count = sales_count

    def action_open_sales(self):
        return {
            'name': _('Sold'),
            'domain': [('sperson', '=', self.id),('state','=','so')],
            'res_model': 'apartment.enquiry',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def action_open_sales1(self):
        return {
            'name': _('Sales'),
            'domain': [('sperson', '=', self.id)],
            'res_model': 'apartment.enquiry',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }


    @api.model
    def create(self, vals):
        # if not vals.get('note'):
        #         vals['note'] = 'New Patient'

        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('apartment.salesteam') or _('New')
        res = super(ApartmentRecord, self).create(vals)
        return res


class ApartmentRecord(models.Model):
        _name = "apartment.salesteam.lines"

        eqid = fields.Many2one('apartment.enquiry',string='Eq id',domain="[('state','=','so')]")
        flat = fields.Char(string='Flat name')
        commission = fields.Char(string="commission")

        data = fields.Many2one('apartment.salesteam', string='Data')

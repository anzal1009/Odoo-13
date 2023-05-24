from odoo import api,models, fields,_

class ApartmentRecord(models.Model):
        _name = "apartment.enquiry"
        _inherit = ['mail.thread', 'mail.activity.mixin']



        name = fields.Many2one('apartment.customer',string='Customer Name')
        name_seq = fields.Char(string='Enquiry No', required=True, copy=False, readonly=True,
                               default=lambda self: _('New'))
        phone = fields.Char(string='Mobile No',related='name.phone')
        email = fields.Char(string='Email',related='name.email')
        advance = fields.Char(string='Advance')
        gender = fields.Selection(string='Gender',related='name.gender')
        age = fields.Char(string='Age',related='name.age')
        sperson = fields.Many2one('apartment.salesteam',string='Sales Person')
        desc = fields.Text(string='Description')
        eqname = fields.Char(string='Enquiry Name')
        # cpercent = fields.Char(string='Commission')
        # cpercent = fields.Selection(
        #         [('f', '5 %'), ('t', '10 %'), ('to', '20 %')],
        #         string='Commission')
        cpercent = fields.Integer(string='Commission Percent',default='3')
        camount =fields.Float(string='Commission Amount',compute='amount',domain="[('state','=','so')]")
        # data_line = fields.One2many('apartment.enquiry.lines','data',string='Data Line')

        # cpercentage = fields.Char(string='Commission Amount',default='%',compute="compute_percent")






        projname = fields.Many2one('apartment.configuration',string='Project Name')
        dist = fields.Char(string='District',related='projname.dist')
        states = fields.Char(string='State',related='projname.states')
        flatname =fields.Many2one('apartment.flats',string='Flat Name',domain="[('projname','=',projname),('state','=','un')]")

        bloname = fields.Many2one(string='Block Name',related='flatname.bloname')
        floor = fields.Many2one( string='Floor',related='flatname.floor')
        utype = fields.Many2one( string='Unit type',related='flatname.utype')
        price = fields.Char( string='Rate',related='flatname.price')

        state = fields.Selection(
                [('un', 'Un sold'), ('bo', 'Booked'), ('so', 'Sold')],
                default='un', string='Status', tracking=True)

        @api.model
        def create(self, vals):
                # if not vals.get('note'):
                #         vals['note'] = 'New Patient'

                if vals.get('name_seq', _('New')) == _('New'):
                        vals['name_seq'] = self.env['ir.sequence'].next_by_code('apartment.enquiry') or _('New')
                res = super(ApartmentRecord, self).create(vals)
                return res



        def action_booked(self):
                self.flatname.state = 'bo'
                self.state = 'bo'

        def action_sold(self):
                self.flatname.state = 'so'
                self.state = 'so'

        @api.depends('cpercent','price')
        def amount(self):
                for row in self:
                        row.camount = float(row.price)  * float(row.cpercent)
                        row.camount =float(row.camount)/100
                        return row.camount

        # def action_booked(self):
        #         self.flatname.state = 'bo'

        # @api.depends('price','cpercent')
        # def compute_percent(self):
        #         for row in self:
        #                 row.cpercentage = row.cpercent * (row.price)
        #                 return row.cpercentage


#
# class ApartmentRecord(models.Model):
#         _name = "apartment.enquiry.lines"
#
#         activity = fields.Char(string='Name')
#         sno = fields.Integer(string='S no')
#         date = fields.Datetime(string="Date")
#
#         data = fields.Many2one('apartment.enquiry', string='Data')
#

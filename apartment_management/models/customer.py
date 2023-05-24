from odoo import api,models, fields,_

class ApartmentRecord(models.Model):
        _name = "apartment.customer"
        _inherit = ['mail.thread', 'mail.activity.mixin']


        name = fields.Char(string='Customer Name')
        name_seq = fields.Char(string='Customer ID', required=True, copy=False, readonly=True,
                               default=lambda self: _('New'))
        photo = fields.Binary(string='Photo')
        phone = fields.Char(string='Mobile No')
        addres = fields.Text(string='Address')
        age = fields.Char(string='Age')
        gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender')
        email = fields.Char(string='Email')
        bank = fields.Char(string="Bank Name")
        acc = fields.Char(string="Account Number")
        br = fields.Char(string='Branch')
        sale =fields.Char(string='C\O')
        dep = fields.Char(string='Other')
        # data_line = fields.One2many('apartment.customer.lines','data',string='Data Line')



        sales_count = fields.Integer(string='Sales Count', compute='_compute_sales_count')

        def _compute_sales_count(self):
            sales_count = self.env['apartment.enquiry'].search_count([('name', '=', self.id)])
            self.sales_count = sales_count

        def action_open_sales(self):
            return {
                'name': _('Enquiry'),
                'domain': [('name', '=', self.id)],
                'res_model': 'apartment.enquiry',
                'view_id': False,
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }

        meeting_count = fields.Integer(string='Meeting Count', compute='_compute_meeting_count')
        #
        def _compute_meeting_count(self):
                meeting_count = self.env['calendar.event'].search_count([('name', '=', self.name)])
                self.meeting_count = meeting_count

        # meeting_ids = fields.Many2many('calendar.event', string='Meetings', copy=False)
        # meeting_count = fields.Integer("Meetings", compute='_compute_meeting_count')
        #
        # def _compute_meeting_count(self):
        #         for partner in self:
        #                 partner.meeting_count = len(partner.meeting_ids)

        # def action_open_meetings(self):
        #         name = self.ids
        #         name.append(self.env.user.partner_id.id)
        #         action = self.env.ref('calendar.action_calendar_event').read()[0]
        #         action['context'] = {
        #                 'default_partner_ids': name,
        #         }
        #         action['domain'] = ['|', ('name', 'in', self.meeting_ids.ids), ('name', 'in', self.ids)]
        #         return action
        def action_open_meetings(self):
                return {
                        'name': _('Meeting'),
                        'domain': [('name', '=', self.name)],
                        'res_model': 'calendar.event',
                        'view_id': False,
                        'view_mode': 'tree,form',
                        'type': 'ir.actions.act_window',
                }

        # def action_open_meetings(self):
        #     meetings = self.env['calendar.event'].search([('res_model', '=', self._name),('res_id', '=', self.id)])
        #     for rec in meetings:
                # vals = {
                #     'activity': rec.name,
                #     'sno' :rec.start,
                #     'date':rec.stop
                # }
                # action_open_meetings = self.env['apartment.customer.lines'].create(vals)
            # print(action_open_meetings)
            #     print("Name", rec.name)
                # return {
                #     "type": "ir.actions.do_nothing"
                # }

        @api.model
        def create(self, vals):
                # if not vals.get('note'):
                #         vals['note'] = 'New Patient'

                if vals.get('name_seq', _('New')) == _('New'):
                         vals['name_seq'] = self.env['ir.sequence'].next_by_code('apartment.customer') or _('New')
                res = super(ApartmentRecord, self).create(vals)
                return res
#
#
# class ApartmentRecordlines(models.Model):
#     _name = "apartment.customer.lines"
#
#     activity = fields.Char(string='Activity')
#     sno = fields.Datetime(string='S no')
#     descr = fields.Char(string='Description')
#     date = fields.Datetime(string='Date')
#
#     data = fields.Many2one('apartment.customer',string='Data')




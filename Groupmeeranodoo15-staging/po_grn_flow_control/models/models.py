# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Picking(models.Model):
    _inherit = "stock.picking"

    # PO GRN Approval code
    # @api.depends('move_lines.quantity_done')
    # def compute_approval_required(self):
    #     for record in self:
    #         if any(line.quantity_done > (line.purchase_line_id.product_qty-line.purchase_line_id.qty_received) for line in record.move_lines):
    #             record.qty_approval_required = True
    #         else:
    #             record.qty_approval_required = False
    #
    # qty_approval_required = fields.Boolean('Approval Required', compute='compute_approval_required')
    # approval_state = fields.Selection([('draft', 'Draft'),
    #                                    ('waiting_for_approval', 'Waiting For Approval'),
    #                                    ('approved', 'Approved')], string='Approval Status', default='draft', copy=False)

    # def button_validate(self):
    #     if self.purchase_id:
    #         if any(self.move_lines.filtered(lambda line: line.quantity_done > (line.purchase_line_id.product_qty-line.purchase_line_id.qty_received))):
    #             if self.approval_state != 'approved' and not self.env.user.has_group("po_grn_flow_control.group_po_grn_flow_approve"):
    #                 if self.approval_state == 'draft':
    #                     raise ValidationError(_("You can't validate this receipt due to done quantity exceeds ordered qty. Please send this for approval."))
    #                 if self.approval_state == 'waiting_for_approval':
    #                     raise ValidationError(
    #                         _("You can't validate this receipt due to done quantity exceeds ordered qty. Please wait for the approval."))
    #
    #     self.approval_state = 'approved'
    #     return super(Picking, self).button_validate()

    # def action_approve_grn(self):
    #     for record in self:
    #         msg = _('This receipt has been approved by %(user)s', user=self.env.user.name)
    #         record.message_post(body=msg)
    #         record.approval_state = 'approved'

    def button_validate(self):
        if self.purchase_id:
            if any(self.move_lines.filtered(lambda line: line.quantity_done > (line.purchase_line_id.product_qty-line.purchase_line_id.qty_received))):
                raise ValidationError(_("You can't validate this receipt due to done quantity exceeds ordered qty"))

        return super(Picking, self).button_validate()



# class ResPartner(models.Model):
#     _inherit = "res.partner"
#
#     def name_get(self):
#         res = []
#         for partner in self.filtered(lambda picking: picking.vat):
#             name = partner._get_name()
#             res.append((partner.id, name))
#         return res
#
#     @api.model
#     def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
#         # args.append([('vat', '!=', False)])
#         if not args:
#             args = [['vat', '!=', False]]
#         else:
#             args.append(['vat', '!=', False])
#         res = super(ResPartner, self)._name_search(name, args=args, operator=operator, limit=limit,
#                                                    name_get_uid=name_get_uid)
#         return res
#
#     @api.model
#     def search(self, args, offset=0, limit=None, order=None, count=False):


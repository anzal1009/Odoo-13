# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class StockPickingApproval(models.TransientModel):
    _name = "stock.picking.qty.approval"
    _description = 'Stock Picking Approval'

    @api.model
    def default_get(self, fields):
        res = super(StockPickingApproval, self).default_get(fields)
        if self.env.context.get('active_id') and self.env.context.get('active_model') == 'stock.picking':
            if len(self.env.context.get('active_ids', list())) > 1:
                raise UserError(_("You may only approve one picking at a time."))
            picking = self.env['stock.picking'].browse(self.env.context.get('active_id'))
            if picking.exists():
                res.update({'picking_id': picking.id})
        return res

    picking_id = fields.Many2one('stock.picking')
    company_id = fields.Many2one(related='picking_id.company_id')
    reason = fields.Text(string="Comment", required=True)

    def action_send_for_approval(self):
        for record in self:

            msg = _(u"""Approval request has been sent by '{0}'!<br/>
                            Reason for approval: '{1}'.
                            """).format(
                self.env.user.name,
                record.reason,
            )
            record.picking_id.message_post(body=msg)
            record.picking_id.approval_state = 'waiting_for_approval'
            notification_ids = []
            users = self.env['res.users'].search(
                [("groups_id", "=", self.env.ref("po_grn_flow_control.group_po_grn_flow_approve").id)])
            for user in users:
                notification_ids.append((0, 0, {
                    'res_partner_id': user.partner_id.id,
                    'notification_type': 'inbox',
                    # 'notification_status': 'exception'
                }))

            mail_content = _('Please approve this receipt: <a href =  # data-oe-model=stock.picking data-oe-id=%d>%s</a>') % (
                record.picking_id.id, record.picking_id.name)

            record.picking_id.message_post(body=mail_content,
                                message_type='notification',
                                subtype_xmlid='mail.mt_comment',
                                notification_ids=notification_ids)

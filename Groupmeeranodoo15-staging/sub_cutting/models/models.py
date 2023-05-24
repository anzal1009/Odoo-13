# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SubCutting(models.Model):
    _name = 'sub.cutting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sub Cutting"
    _order = 'id desc'

    name = fields.Char('Sequence No.', required=True, index=True, copy=False, readonly=True, default=lambda x: _('New'))
    date = fields.Date(string='Date', required=True, index=True, readonly=True, states={'draft': [('readonly', False)]},
                       copy=False, tracking=True, default=fields.Date.context_today)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 store=True, readonly=True, default=lambda self: self.env.company.id)
    user_id = fields.Many2one('res.users', string='User', index=True, tracking=True, default=lambda self: self.env.user,
                              check_company=True)
    location_id = fields.Many2one('stock.location', "Location", check_company=True, readonly=True, required=True,
                                  states={'draft': [('readonly', False)]},
                                  domain="[('usage','=','internal'), '|', ('company_id', '=', company_id), ('company_id', '=', False)]")
    product_id = fields.Many2one('product.product', string='Product', required=True, check_company=True,
                                 domain="[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    tracking = fields.Selection(related='product_id.tracking', readonly=True)
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number', index=True,
        ondelete='restrict', check_company=True,
        domain="[('product_id', '=', product_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    package_id = fields.Many2one(
        'stock.quant.package', 'Package',
        domain="[('location_id', '=', location_id)]",
        help='The package containing this quant', ondelete='restrict', check_company=True)
    quantity = fields.Float('Quantity', readonly=True, digits='Product Unit of Measure', states={'draft': [('readonly', False)]}, required=True, default=1)
    sub_cutting_products_ids = fields.One2many('sub.cutting.products', 'sub_cutting_id', string='Sub Cutting Products',
                                  states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True,
                                  auto_join=True)
    sub_cutting_by_products_ids = fields.One2many('sub.cutting.by.products', 'sub_cutting_id',
       string='Sub Cutting Products', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
       copy=True, auto_join=True)
    check_onhand_lot = fields.Boolean(compute='Check_onhand_lot', string='Lot_onhand')
    operation = fields.Selection([('cutting', 'Cutting'), ('merging', 'Merging')], string='Operation', default='merging', required=True,
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})

    @api.onchange('lot_id')
    def set_quantity_lot_product(self):
        for record in self:
            if record.lot_id:
                record.quantity = 1

    @api.constrains('lot_id', 'quantity')
    def check_quantity(self):
        for record in self:
            if record.lot_id:
                if record.quantity > 1:
                    raise ValidationError(
                        _('Please choose 1 quantity: \n Product: %s, Serial Number: %s') % (
                            record.product_id.display_name, record.lot_id.name))
                stock_quant = self.env['stock.quant'].search([('product_id', '=', record.product_id.id),
                                                              ('location_id', '=', record.location_id.id),
                                                              ('company_id', '=', record.company_id.id),
                                                              ('lot_id', '=', record.lot_id.id)])
                if stock_quant and record.operation == 'merging':
                    raise ValidationError(
                        _('The serial number has already been assigned: \n Product: %s, Serial Number: %s') % (
                        record.product_id.display_name, record.lot_id.name))

                if not stock_quant and record.operation == 'cutting':
                    raise ValidationError(
                        _('Not available: \n Product: %s, Serial Number: %s') % (
                        record.product_id.display_name, record.lot_id.name))
            else:
                stock_quant = self.env['stock.quant'].search([('product_id', '=', record.product_id.id),
                                                              ('location_id', '=', record.location_id.id),
                                                              ('company_id', '=', record.company_id.id)])
                quantity = 0
                for quant in stock_quant:
                    quantity += quant.quantity
                if quantity <= 0 and record.operation == 'cutting':
                    raise ValidationError(
                        _('Not available: \n Product: %s') % (
                            record.product_id.display_name))
                if not stock_quant and record.operation == 'cutting':
                    raise ValidationError(
                        _('Not available: \n Product: %s') % record.product_id.display_name)

    # @api.model
    # def create(self, vals):
    #     company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
    #     # Ensures default picking type and currency are taken from the right company.
    #     self_comp = self.with_company(company_id)
    #     if not vals.get('name') or vals['name'] == _('New'):
    #         vals['name'] = self_comp.env['ir.sequence'].next_by_code('sub.cutting') or _('New')
    #     res = super(SubCutting, self_comp).create(vals)
    #     return res

    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        for record in self:
            if record.state not in ('draft', 'cancel'):
                raise UserError(
                    _('You can not delete a processed sub cutting record.'))

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    def compute_onhand(self, product, location, company, lot):
        onhand = 0
        if lot:
            stock_quant = self.env['stock.quant'].search([('product_id', '=', product),
                                                          ('location_id', '=', location),
                                                          ('company_id', '=', company),
                                                          ('lot_id', '=', lot)])
        else:
            stock_quant = self.env['stock.quant'].search([('product_id', '=', product),
                                                      ('location_id', '=', location),
                                                      ('company_id', '=', company)])
        for quant in stock_quant:
            onhand += quant.quantity
        return onhand

    def action_sub_cutting(self):
        for record in self:
            if record.operation == 'merging' and record.quantity <= 0 and record.sub_cutting_products_ids.filtered(lambda line: line.quantity <= 0):
                raise UserError(
                    _('Please check the quantity of product and components, should be greater than 0'))
            if record.operation == 'cutting' and record.quantity <= 0 and record.sub_cutting_by_products_ids.filtered(lambda line: line.quantity <= 0):
                raise UserError(
                    _('Please check the quantity of product and by products, should be greater than 0'))
            self_comp = record.with_company(record.company_id.id)
            if record.name == _('New'):
                record.name = self_comp.env['ir.sequence'].next_by_code('sub.cutting') or _('New')
            # onhand_new_product = record.compute_onhand(record.product_id.id, record.location_id.id, record.company_id.id, record.lot_id.id)
            main_stock_quant = self.env['stock.quant'].create({
                'product_id': record.product_id.id,
                'location_id': record.location_id.id,
                'lot_id': record.lot_id.id,
                'package_id': record.package_id.id,
                'inventory_quantity': record.quantity if record.operation == 'merging' else -record.quantity,
                'user_id': record.user_id.id
            })
            main_stock_quant.action_apply_inventory()
            for by_products_detail in record.sub_cutting_by_products_ids:
                # onhand_by_product = record.compute_onhand(by_products_detail.product_id.id, by_products_detail.location_id.id,
                #                                            by_products_detail.company_id.id, record.lot_id.id)
                by_products = self.env['stock.quant'].create({
                    'product_id': by_products_detail.product_id.id,
                    'location_id': by_products_detail.location_id.id,
                    'lot_id': by_products_detail.lot_id.id,
                    'package_id': by_products_detail.package_id.id,
                    'inventory_quantity': by_products_detail.quantity,
                    'user_id': by_products_detail.user_id.id
                })
                by_products.action_apply_inventory()
            scrap_products = record.sub_cutting_by_products_ids.filtered(lambda line: line.scrap is True)
            scrap_res = scrap_products.move_to_scrap()
            if record.operation == 'merging':
                for products_detail in record.sub_cutting_products_ids:
                    # onhand_product = record.compute_onhand(products_detail.product_id.id, products_detail.location_id.id,
                    #                                            products_detail.company_id.id, record.lot_id.id)
                    # quant = self.env['stock.quant']._gather(
                    #     products_detail.product_id, products_detail.location_id, lot_id=products_detail.lot_id,
                    #     package_id=products_detail.package_id, owner_id=None, strict=True)
                    sub_cutting_products = self.env['stock.quant'].create({
                        'product_id': products_detail.product_id.id,
                        'location_id': products_detail.location_id.id,
                        'lot_id': products_detail.lot_id.id,
                        'package_id': products_detail.package_id.id,
                        'inventory_quantity': -products_detail.quantity,
                        'user_id': products_detail.user_id.id
                    })
                    # sub_cutting_products.inventory_quantity = sub_cutting_products.quantity-products_detail.quantity if sub_cutting_products.quantity > 0 else 0
                    sub_cutting_products.action_apply_inventory()
            record.state = 'done'


class SubCuttingProducts(models.Model):
    _name = 'sub.cutting.products'
    _description = 'Sub Cutting Products'
    _order = 'sub_cutting_id, id'
    _check_company_auto = True

    sub_cutting_id = fields.Many2one('sub.cutting', string='Sub Cutting Reference', required=True, ondelete='cascade',
                                     index=True, copy=False)
    location_id = fields.Many2one('stock.location', "Location", check_company=True, readonly=True, required=True,
                                  states={'draft': [('readonly', False)]},
                                  domain="[('usage','=','internal'), '|', ('company_id', '=', company_id), ('company_id', '=', False)]")
    company_id = fields.Many2one(related='sub_cutting_id.company_id', string='Company', store=True, index=True)
    product_id = fields.Many2one(
        'product.product', string='Product',
        domain="[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True)
    user_id = fields.Many2one(related='sub_cutting_id.user_id', store=True, string='User')
    state = fields.Selection(
        related='sub_cutting_id.state', string='Sub Cutting Status', copy=False, store=True)
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    product_reference = fields.Char('Product Reference', )
    tracking = fields.Selection(string='Product Tracking', readonly=True, related="product_id.tracking")
    package_id = fields.Many2one(
        'stock.quant.package', 'Package',
        domain="[('location_id', '=', location_id)]",
        help='The package containing this quant', ondelete='restrict', check_company=True)
    quantity = fields.Float('Quantity', readonly=True, digits='Product Unit of Measure',
                            states={'draft': [('readonly', False)]}, required=True, default=1)

    @api.onchange('lot_id')
    def set_quantity_lot_components(self):
        for record in self:
            if record.lot_id:
                record.quantity = 1

    @api.constrains('lot_id', 'quantity')
    def check_quantity(self):
        for record in self:
            if record.lot_id:
                stock_quant = self.env['stock.quant'].search([('product_id', '=', record.product_id.id),
                                                              ('location_id', '=', record.location_id.id),
                                                              ('company_id', '=', record.company_id.id),
                                                              ('lot_id', '=', record.lot_id.id)])
                if not stock_quant:
                    raise ValidationError(
                        _('Not available: \n Product: %s') % (
                            record.product_id.display_name))
                for quant in stock_quant:
                    if quant.quantity <= 0:
                        raise ValidationError(
                            _('Not available: \n Product: %s') % (
                                record.product_id.display_name))

            else:
                stock_quant = self.env['stock.quant'].search([('product_id', '=', record.product_id.id),
                                                              ('location_id', '=', record.location_id.id),
                                                              ('company_id', '=', record.company_id.id),
                                                              ])
                quantity = 0
                for quant in stock_quant:
                    quantity += quant.quantity
                if quantity <= 0:
                    raise ValidationError(
                        _('Not available: \n Product: %s') % (
                            record.product_id.display_name))

                if not stock_quant:
                    raise ValidationError(
                        _('Not available: \n Product: %s') % (
                            record.product_id.display_name))


class SubCuttingByProducts(models.Model):
    _name = 'sub.cutting.by.products'
    _description = 'Sub Cutting by-roducts'
    _order = 'sub_cutting_id, id'
    _check_company_auto = True

    sub_cutting_id = fields.Many2one('sub.cutting', string='Sub Cutting Reference', required=True, ondelete='cascade',
                                     index=True, copy=False)
    location_id = fields.Many2one('stock.location', "Location", check_company=True, readonly=True, required=True,
                                  states={'draft': [('readonly', False)]},
                                  domain="[('usage','=','internal'), '|', ('company_id', '=', company_id), ('company_id', '=', False)]")
    company_id = fields.Many2one(related='sub_cutting_id.company_id', string='Company', store=True, index=True)
    product_id = fields.Many2one(
        'product.product', string='Product',
        domain="[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True)
    user_id = fields.Many2one(related='sub_cutting_id.user_id', store=True, string='User')
    state = fields.Selection(
        related='sub_cutting_id.state', string='Sub Cutting Status', copy=False, store=True)
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    product_reference = fields.Char('Product Reference', )
    tracking = fields.Selection(string='Product Tracking', readonly=True, related="product_id.tracking")
    package_id = fields.Many2one(
        'stock.quant.package', 'Package',
        domain="[('location_id', '=', location_id)]",
        help='The package containing this quant', ondelete='restrict', check_company=True)
    quantity = fields.Float('Quantity', readonly=True, digits='Product Unit of Measure',
                            states={'draft': [('readonly', False)]}, required=True, default=1)
    scrap = fields.Boolean(string='Scrap', default=False)
    scrap_location_id = fields.Many2one('stock.location', "Scrap Location", check_company=True, readonly=True,
                                  states={'draft': [('readonly', False)]},
                                  domain="[('scrap_location','=',True), '|', ('company_id', '=', company_id), ('company_id', '=', False)]")

    @api.onchange('lot_id')
    def set_quantity_lot_by_products(self):
        for record in self:
            if record.lot_id:
                record.quantity = 1

    @api.constrains('lot_id', 'quantity')
    def check_quantity(self):
        for record in self:
            if record.lot_id:
                if record.quantity > 1:
                    raise ValidationError(
                        _('Please choose 1 quantity: \n Product: %s, Serial Number: %s') % (
                            record.product_id.display_name, record.lot_id.name))
                stock_quant = self.env['stock.quant'].search([('product_id', '=', record.product_id.id),
                                                              ('location_id', '=', record.location_id.id),
                                                              ('company_id', '=', record.company_id.id),
                                                              ('lot_id', '=', record.lot_id.id)])
                if stock_quant:
                    raise ValidationError(
                        _('The serial number has already been assigned: \n Product: %s, Serial Number: %s') % (
                            record.product_id.display_name, record.lot_id.name))

    @api.onchange('scrap')
    def load_scrap_location(self):
        for record in self:
            if record.scrap:
                record.scrap_location_id = self.env['stock.location'].search([('scrap_location','=',True), '|',
                                                                              ('company_id', '=', record.company_id.id),
                                                                              ('company_id', '=', False)], limit=1).id

    def move_to_scrap(self):
        for line in self:
            scrap = self.env['stock.scrap'].create({
                'product_id': line.product_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                'scrap_qty': line.quantity,
                'lot_id': line.lot_id.id,
                'location_id': line.location_id.id,
                'scrap_location_id': line.scrap_location_id.id,
                'company_id': line.company_id.id,
                'sub_cutting_id': line.sub_cutting_id.id,
            })
            scrap.action_validate()
        return True


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    sub_cutting_id = fields.Many2one('sub.cutting', string="Sub Cutting", copy=False)


















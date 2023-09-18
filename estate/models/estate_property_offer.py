# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError

class EstatePropertyModel(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "estate.property.offer"
    _description = "Property offers."
    _order = "price desc"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    price = fields.Float()
    status = fields.Selection(selection = [('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", ondelete="cascade")
    property_id = fields.Many2one(comodel_name="estate.property", ondelete="cascade")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute ="_compute_date_deadline", inverse="_compute_validity")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    
    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################
    _sql_constraints= [("check_price_if_positive", "CHECK(price>0)", "Offer price should be positive!")]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            today = fields.Date.context_today(self)
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = today + relativedelta(days=record.validity)

    def _compute_validity(self):
        for record in self:
            today = fields.Date.context_today(self)
            record.validity = (record.date_deadline - today).days

    #########################
    # CRUD method overrides #
    #########################
    @api.model
    def create(self, vals):
        offers = self.env["estate.property.offer"].search([('property_id.id', '=', vals['property_id'])])
        offers_price = offers.mapped("price")

        if offers_price and vals['price'] < max(offers_price):
            raise UserError("Offer price should be higher than previous offers!")
        
        self.env["estate.property"].search([("id", "=",vals["property_id"])]).state = "offer_received"
        return super(EstatePropertyModel, self).create(vals)

    ##################
    # Action methods #
    ##################
    def accept_offer(self):
        offers = self.env["estate.property.offer"]
        for offer in self:
            is_accepted = offers.search([('property_id.id', '=', offer.property_id.id), ('status', '=', 'accepted')])
            if offer.status == "refused" and (not is_accepted):
                raise UserError("Offer is already refused! Contact buyer to make another offer")
            elif offer.status == "refused":
                raise UserError("Offer is already refused!")
            elif is_accepted:
                raise UserError("An offer is already accepted!")
            elif not is_accepted:
                offer.status = "accepted"
                offer.property_id.selling_price = offer.price
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.state = "offer_accepted"
        return True
    
    def reject_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("Offer is already accepted!")
            elif not offer.status:
                offer.status = "refused"
        return True

    ####################
    # Business methods #
    ####################
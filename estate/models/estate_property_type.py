# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "estate.property.type"
    _description = "Property types."
    _order = "sequence, name"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Property Types", required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Property')
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_type_id", string="Offers", required=True)
    offer_count = fields.Integer(string="Number of offers",
                                 compute="_compute_offer_count")

    ##############################
    # Compute and search methods #
    ##############################
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)

    ############################
    # Constrains and onchanges #
    ############################

    _sql_constraints = [("check_type_if_unique", "unique(name)", "Property type should be unique!"),
                        ]

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################

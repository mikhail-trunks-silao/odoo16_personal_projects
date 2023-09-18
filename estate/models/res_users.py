# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "res.users"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    property_ids = fields.One2many(comodel_name="estate.property", 
                                   inverse_name="seller_id",
                                   domain=[("state", "in", ['new', 'offer_received'])],
                                   string="Properties for sale")
    
    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
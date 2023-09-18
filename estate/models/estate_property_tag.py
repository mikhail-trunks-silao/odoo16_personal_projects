# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "estate.property.tag"
    _description = "Property tags."
    _order = "name"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")
    
    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################
    _sql_constraints = [("check_tag_if_unique", "unique(name)", "Property tag should be unique!"),
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
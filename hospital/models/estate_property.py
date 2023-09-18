from odoo import models, fields



class EstateProperty(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "estate.property"
    _description = "Module for selling properties."

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################

    name = fields.Char(string = "Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area  = fields.Integer()
    facade = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
    selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
)



    
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
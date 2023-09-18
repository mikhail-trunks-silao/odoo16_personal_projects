from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "estate.property"
    _description = "Module for selling properties."
    _order = "id desc"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################

    name = fields.Char(string="Title", required=True)
    description = fields.Text("Active")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        copy=False, default=lambda self: self.defaultDate(), string="Available From")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of bedroms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facade = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users", string="Salesman", readonly=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", ondelete="cascade")
    state = fields.Selection(selection=[
        ("new", "New"),
        ("offer_received", "Offer Received", ),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled")
    ], default="new", copy=False)

    # Property Offer fields#
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id", string="Offers")


    total_area = fields.Float(
        string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price")


    ##############################
    # Compute and search methods #
    ##############################
    @api.model
    def defaultDate(self):
        today = fields.Datetime.now()
        three_months_later = today + relativedelta(months=3)
        return three_months_later

    @api.depends("total_area", "living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.onchange("best_price")
    def _compute_best_price(self):
        if self.offer_ids:
            best_price = max(self.offer_ids.mapped("price"))
            self.best_price = best_price
        else:
            self.best_price = 0

    ############################
    # Constrains and onchanges #
    ############################

    _sql_constraints = [("check_excpected_price_if_positive", "CHECK(expected_price >= 0)", "Expected price should be positive"),
                        ("check_selling_price_if_positive", "CHECK(selling_price >= 0)", "Expected price should be positive!")]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        minimum_selling_price = self.expected_price * 0.9
        check_selling_price = float_compare(
            self.selling_price, minimum_selling_price, 2)
        if check_selling_price == 1 or check_selling_price == 0:
            pass
        elif check_selling_price == -1:
            raise ValidationError("Offer price is too low!")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = None

    #########################
    # CRUD method overrides #
    #########################
    @api.ondelete(at_uninstall=False)
    def _unlink_except_offer_ids(self):
        for property in self:
            if property.state not in ["new", "cancelled"]:
                raise UserError("Cannot delete offers for properties in this state!")
            else:
                continue

    ##################
    # Action methods #
    ##################
    def sell_a_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold!")
            elif property.state == "sold":
                raise UserError("Property is already sold!")
            else:
                property.state = "sold"
        return True

    def cancel_a_property(self):
        for property in self:
            if property.state == "sold":
                raise UserError("Sold properties cannnot be cancelled!")
            else:
                property.state = "cancelled"
        return True

    ####################
    # Business methods #
    ####################

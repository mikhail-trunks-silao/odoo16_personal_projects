# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstateProperty(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "estate.property"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################

    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################
    def sell_a_property(self):
        for property in self:
            winning_offer = property.offer_ids.search(
                [("status", "=", "accepted"), ("property_id", "=", property.id)])
            invoice_dict = {
                "move_type": "out_invoice",
                "partner_id": winning_offer.partner_id.id,
                "invoice_line_ids": [
                    (0, 0, {
                    "name": property.name,
                    "quantity": 1,
                    "price_unit": winning_offer.price * 0.06,
                    }),
                    (0, 0, {
                        "name": "Agency Fees",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ],
            }
            self.env["account.move"].create(invoice_dict)

            return super().sell_a_property()

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################

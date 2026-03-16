# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = ["res.partner"]

    membership_category_id = fields.Many2one(
        comodel_name="membership.membership_category",
        string="Target role",
        help="Role for next subscribed membership",
        default=lambda self: self._default_membership_category_id(),
    )

    def _default_membership_category_id(self):
        return self.env["membership.membership_category"].search([], limit=1).id

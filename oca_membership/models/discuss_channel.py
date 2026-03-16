# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

class Channel(models.Model):
    _inherit = ["discuss.channel"]

    is_membership_work_group = fields.Boolean(
        string="Membership Work Group",
        default=False,
        help="Defines this Channel as a Work Group of the association.",
    )

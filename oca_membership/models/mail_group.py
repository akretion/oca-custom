# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

class MailGroup(models.Model):
    _inherit = ["mail.group"]

    is_community = fields.Boolean(
        string="Is a community",
        default=False,
        help="Communities are visible on the website page, on member profile.",
    )

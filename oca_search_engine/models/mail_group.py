# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

class MailGroup(models.Model):
    _inherit = ["mail.group"]

    is_publish = fields.Boolean(
        string="OCA website",
        default=False,
        help="Whether to be visible on the Members page, on the OCA website",
    )

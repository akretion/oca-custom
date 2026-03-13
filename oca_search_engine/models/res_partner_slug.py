# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exceptions, _


class ResPartnerSlug(models.Model):
    _name = "res.partner.slug"
    _description = "Partner slug"

    name = fields.Char(
        string="Slug",
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        ondelete="cascade",
        required=True,
    )

    @api.constrains("name")
    def _constrain_unique(self):
        """Prevent duplicates of `slug`, to avoid website URL redirection issues
        Since we want explicit error message, we don't use `_sql_constrains`
        """
        for slug in self:
            duplicates = self.search([
                ("name", "=", slug.name),
                ("id", "!=", slug.id),
            ])
            if duplicates:
                raise exceptions.ValidationError(_(
                    "The URL key %(slug)s already exists on those "
                    "partner(s): %(partners)s",
                    slug=slug.name,
                    partners=", ".join(duplicates.partner_id.mapped("name")),
                ))
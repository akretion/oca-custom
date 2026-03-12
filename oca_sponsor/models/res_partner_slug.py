# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exception, _


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

    @api.constrains("name", "partner_id")
    def _constrain_unique(self):
        """Prevent duplicates of `slug`, to avoid website URL redirection issues
        Since we want explicit error message, we don't use `_sql_constrains`
        """
        rg_result = self._read_group(
            domain=[("name", "=", self.mapped("name"))],
            groupby=["name"],
            aggregates=["id:array_agg"]
        )
        mapped_names = {name: ids for name, ids in rg_result}
        for slug in self:
            ids = mapped_names.get(slug.name, [])
            if ids != [slug.id]:
                raise exception.ValidationError(_(
                    "The URL key %(slug)s already exists on those "
                    "partner(s): %(partners)s",
                    slug=slug.name,
                    partners="," . join(self.env["res.partner"].browse(ids).mapped("name"))
                ))

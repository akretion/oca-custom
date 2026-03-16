# Copyright 2026 Akretion (https://www.akretion.com).
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, Command

INDEX_COMPANIES = "oca_search_engine.oca_typesense_index_companies"

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "se.indexable.record"]

    is_published = fields.Boolean(tracking=True,)
    can_be_published = fields.Boolean(
        compute="_compute_can_be_published",
        search="_search_can_be_published",
    )
    mail_group_member_ids = fields.One2many(
        comodel_name="mail.group.member",
        inverse_name="partner_id",
    )
    slug_history_ids = fields.One2many(
        comodel_name="res.partner.slug",
        inverse_name="partner_id",
        string="URL Keys",
        help="A URL Key is computed from the partner name and forms the last part of the"
             " partner URL page in the website. Keeping history helps to redirect"
             " former company URL to the new one."
    )
    
    def _add_to_oca_search_engine(self):
        """Add records or update fields in the index"""
        to_synch = self.filtered(lambda x: x._filter_add_to_oca_search_engine())
        to_synch._add_to_index(self.env.ref(INDEX_COMPANIES))

    def _filter_add_to_oca_search_engine(self):
        return self.can_be_published and self.is_published
    
    #====== Compute ======#
    @api.depends("is_integrator", "grade_id", "membership_state")
    def _compute_can_be_published(self):
        """Technical field enabling or not `is_published`, this last being editable by internal users"""
        for partner in self:
            partner.can_be_published = partner._get_can_be_published()
    
    def _get_can_be_published(self):
        """`sponsor_to_review` is prioritary to prevent unreviewed data on the website"""
        return (
            (not self.is_sponsor or not self.sponsor_to_review) and (
                self.is_integrator or
                self.is_sponsor or
                self.membership_state in ["free", "paid"]
            )
        )
    
    @api.model
    def _search_can_be_published(self, operator, value):
        if operator != "=" or not isinstance(value, bool) or not value:
            raise NotImplementedError("Operation not supported.")
        return [
            "|", ("is_sponsor", "=", False), ("sponsor_to_review", "=", False),
            "|", "|",
                ("is_integrator", "=", True),
                ("is_sponsor", "=", True),
                ("membership_state", "in", ["free", "paid"]),
        ]
    
    #====== CRUD ======#
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._autopublish_companies(record)
        return records
    
    def copy(self, default={}):
        records = super().copy(default)
        for record in records:
            record._autopublish_companies(record)
        return records

    def write(self, vals):
        # Slug history
        if "name" in vals and fields.first(self).name != vals["name"]:
            self._add_slug_history()
        
        res = super().write(vals)

        # Remove
        if "is_published" in vals and not vals["is_published"]:
            self._remove_from_index(self.env.ref(INDEX_COMPANIES))
        else:
            self._autopublish_companies(vals)

        return res

    #===== Business logics =====#
    def _autopublish_companies(self, vals):
        """Auto-publish new integrators and new sponsors
        (but not members: because of individual acceptance),
        and remove partner manually set to "unpublished"
        """
        # To add
        if any(x in vals and vals[x] for x in ["grade_id", "is_integrator"]):
            self.filtered(
                lambda x: x.can_be_published and not x.is_published
            ).sudo().is_published = True # 'sudo' to bypass AccessError of 'website.published.multi.mixin'
        
        # Sync (add or update)
        self._add_to_oca_search_engine()

    def _add_slug_history(self):
        companies = self.filtered(lambda x: x.is_sponsor)
        for partner in companies:
            slug = partner._get_slug()
            if slug not in partner.slug_history_ids.mapped("name"):
                partner.slug_history_ids = [Command.create({"name": slug})]
    def _get_slug(self):
        self.ensure_one()
        return self.env['ir.http']._slugify(self.name)
    def _get_avatar_url(self, size):
        self.ensure_one()
        return f'{self.get_base_url()}/web/image/res.partner/{self.id}/avatar_{size}'

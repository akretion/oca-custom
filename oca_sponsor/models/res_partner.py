# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, Command

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "se.indexable.record"]

    # == Website fields for all OCA companies (integrators & sponsors) ==
    is_integrator = fields.Boolean(
        string="Is integrator",
        default=False,
    )
    is_sponsor = fields.Boolean(
        compute="_compute_is_sponsor",
    )
    is_published = fields.Boolean(
        compute='_compute_is_published',
        store=True,
        readonly=False,
        help="Is published. Must be activated so the avatar URL are available externally.",
    )
    slug_history_ids = fields.One2many(
        comodel_name="res.partner.slug",
        inverse="partner_id",
        string="URL Keys",
        help="A URL Key is computed from the partner name and forms the last part of the"
             " partner URL page in the website. Keeping history helps to redirect"
             " former company URL to the new one."
    )
    # == Sponsors custom fields for the website ==
    website_country_ids = fields.Many2many(
        comodel_name="res.country",
        relation="res_partner_country_rel",
        column1="partner_id",
        column2="country_id",
        string="Countries",
        compute="_compute_website_country_ids",
        store=True,
        readonly=False,
    )
    industry_id = fields.Many2one(
        compute="_compute_industry_id",
        store=True,
        readonly=False,
    )
    website_industry_ids = fields.Many2many(
        comodel_name="res.partner.industry",
        relation="res_partner_partner_industry_rel",
        column1="partner_id",
        column2="industry_id",
        string="Industries",
        compute="_compute_website_industry_ids",
        store=True,
        readonly=False,
    )
    website_description_sponsor = fields.Text(
        translate=True,
    )
    website_description_why_oca = fields.Text(translate=True)
    blog_post_ids = fields.One2many(
        comodel_name="blog.post",
        inverse_name="author_id",
    )

    #====== Compute ======#
    @api.depends("grade_id")
    def _compute_is_sponsor(self):
        for partner in self:
            partner.is_sponsor = bool()

    @api.depends("country_id")
    def _compute_website_country_ids(self):
        for partner in self:
            partner.website_country_ids |= partner.country_id
    
    @api.depends("is_integrator")
    def _compute_is_published(self):
        """Native field of `website_partner` to control public partner data exposure like avatar"""
        for partner in self:
            if partner.is_integrator:
                partner.is_published = True
    
    @api.depends("website_industry_ids")
    def _compute_industry_id(self):
        """If empty, set `industry_id` from `website_industry_ids`"""
        for partner in self:
            if not partner.industry_id and partner.website_industry_ids:
                partner.industry_id = fields.first(partner.website_industry_ids)
    @api.depends("industry_id")
    def _compute_website_industry_ids(self):
        """Add `industry_id` in `website_industry_ids`"""
        for partner in self:
            if partner.industry_id and partner.industry_id not in partner.website_industry_ids:
                partner.website_industry_ids |= partner.industry_id

    #====== CRUD ======#
    def write(self, vals):
        if "name" in vals and fields.first(self).name != vals["name"]:
            self._add_slug_history()
        return super().write(vals)

    #===== Business logics =====#
    def _add_slug_history(self):
        companies = self.filtered(lambda x: x.is_sponsor or x.is_integrator)
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

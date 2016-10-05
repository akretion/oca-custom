# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    github_max_try = fields.Char(
        'Github Max Try',
        default='5',
        groups='github_connector.group_github_connector_manager')
    git_code_local_path = fields.Char(
        'Git Source Code Local Path',
        default='/tmp/',
        groups='github_connector.group_github_connector_manager')
    git_partial_commit = fields.Boolean(
        'Git Partial Commit During Analyze',
        default=True,
        groups='github_connector.group_github_connector_manager')

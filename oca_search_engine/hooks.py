# Copyright 2026 AKRETION
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

def post_init_hook(env):
    _init_indexing(env)

def _init_indexing(env):
    models = {"res.partner"}
    for model in models:
        env[model].search([])._add_to_oca_search_engine()

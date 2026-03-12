# Copyright 2026 Akretion (http://www.akretion.com).
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "OCA Sponsors",
    "description": """Add sponsors fields""",
    "version": "18.0.1.0.0",
    "author": "Akretion",
    "website": "https://github.com/oca/oca-custom",
    "license": "AGPL-3",
    "category": "Custom",
    "depends": [
        "website_crm_partner_assign",
        "extendable",
        "search_engine_serializer_pydantic",
    ],
    "data": [
        "views/res_partner_industry.xml",
        "views/res_partner.xml",
    ],
    "installable": True,
    "application": False,
    "development_status": "Alpha",
}

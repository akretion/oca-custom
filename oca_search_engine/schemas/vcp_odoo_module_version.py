# Copyright 2026 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from typing import TypedDict
from extendable_pydantic import StrictExtendableBaseModel


class VcpRepository(TypedDict):
    id: int
    name: str
    description: str


class VcpOdooModuleVersion(StrictExtendableBaseModel):
    name: str
    techname: str
    # TODO WIP
    #    repo: Repo (url du repo, name, description)
    #    category: str # + voir pour avoir un index de category revoir ce que l'on fait
    #    version: str
    #    dependencies: list # des url key
    #    used_by: list # des url key
    #    license: str
    #    summary: str
    #    maturity: str
    #    authors: list (Author) # TODO uniquement une liste de nom en V1
    #    public_url: str
    #    runboat_url: str # a constuire automatiquement
    #    website: str
    #    readme_fragments: list
    #    contributors: list (liste de membre) [name, email, société)
    #                  on va extraire le readme de Contributors pour le structurer
    #    maintainers: list (liste de membre)
    #    url_key: # repo + techname
    #    icon_url: # 80x80

    @classmethod
    def from_record(cls, odoo_rec):
        return cls.model_construct(
            name=odoo_rec.name,
            version=odoo_rec.version,
        )

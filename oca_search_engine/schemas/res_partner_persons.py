# Copyright 2026 AKRETION
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from typing import TypedDict
from .res_partner_companies import Country

from extendable_pydantic import StrictExtendableBaseModel

class Contact(TypedDict):
    email: str | None
    phone: str | None
    address: str | None
    city: str | None
    website: str | None

class Team(TypedDict):
    id: int
    name: str
    description: str | None

class Role(TypedDict):
    id: int
    name: str

class Members(StrictExtendableBaseModel):
    id: int
    name: str
    company_id: int | None
    company: str | None
    contact: Contact
    country: Country
    # role & psc
    roles: list[Role]
    psc: int
    psc_list = list[Team] | None
    work_group_list: list[Team] | None
    # github
    username: str
    avatar_url: str | None
    collaborator_index: int
    modules_maintained: int
    modules_contributions_id: list[int] | None
    # technical website fields
    url_key: str

    @classmethod
    def from_record(cls, record):
        return cls.model_construct(
            id=record.id,
            name=record.name,
            company_id=(
                bool(record.parent_id.is_company) and record.parent_id.id
                or None
            ),
            company=record.commercial_company_name,
            contact=cls._get_contact(record),
            country=cls._get_country(record),
            # role & psc
            roles=cls._get_roles(record),
            psc=0,
            psc_list=cls._get_psc_list(record) or None,
            work_group_list=cls._get_work_group_list(record) or None,
            # github, TODO @sebastienbeau
            username=record.github_username or None,
            avatar_url=record.github_avatar_url or None,
            # github indicators
            translations=0,
            collaborator_index=0,
            modules_maintained=0,
            modules_contributions_id=record.contributor_module_line_ids.ids or None,
            # technical website fields
            url_key=record._get_slug() or None,
        )

    @classmethod
    def _get_contact(cls, record):
        return {
            "email": record.email or None,
            "phone": record.phone or record.mobile or None,
            "website": record.website or None,
            "city": (
                "%(city)s %(state_code)s %(zip)s" %
                (record.city, record.state_id.code, record.zip)
            ).strip() or None,
            "address": (
                "%(street)s\n%(street2)s" %
                (record.street, record.street2)
            ).strip() or None,
        }

    @classmethod
    def _get_country(cls, record):
        return None if not record.country_id else {
            "code": record.country_id.code,
            "label": record.country_id.name,
        }

    @classmethod
    def _get_psc_list(cls, record):
        return [
            {
                "id": x["id"],
                "name": x["name"],
                "description": x["description"],
            } for x in record.github_psc_ids.read(["name", "description"])
        ] or None

    @classmethod
    def _get_roles(cls, record):
        categories = record.membership_category_id._get_with_implied()
        if record.contributor_count: # TODO review with @sebastienbeau correct field name?
            categories |= record.ref("oca_search_engine.membership_category_contributor_oca")
        return [
            {
                "id": x["id"],
                "name": x["name"],
            } for x in categories.sorted("sequence", reverse=True).read(["name"])
        ] or None

    @classmethod
    def _get_work_group_list(cls, record):
        return [
            {
                "id": x["id"],
                "name": x["name"],
                "description": x["description"],
            } for x in record.membership_channel_ids.read(["name", "description"])
        ] or None

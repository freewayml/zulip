from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError

from zerver.lib.management import ZulipBaseCommand


class Command(ZulipBaseCommand):
    """Show the owners and administrators in an organization."""
    help = """Show the owners and administrators in an organization."""

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add arguments to the command."""
        self.add_realm_args(parser, required=True)

    def handle(self, *args: Any, **options: Any) -> None:
        """Handle the command."""
        realm = self.get_realm(options)
        assert realm is not None  # True because of required=True above

        admin_users = realm.get_admin_users_and_bots()
        owner_user_ids = set(realm.get_human_owner_users().values_list("id", flat=True))

        if admin_users:
            print("Administrators:\n")
            for user in admin_users:
                owner_detail = ""
                if user.id in owner_user_ids:
                    owner_detail = " [owner]"
                print(f"  {user.delivery_email} ({user.full_name}){owner_detail}")

        else:
            raise CommandError("There are no admins for this realm!")

        print('\nYou can use the "change_user_role" management command to adjust roles.')

from typing import Any

from django.core.management.base import BaseCommand

from zerver.lib.retention import archive_messages, clean_archived_data


class Command(BaseCommand):
    """
    Django management command for cleaning archived data and archiving messages.
    """
    def handle(self, *args: Any, **options: str) -> None:
        clean_archived_data()
        archive_messages()

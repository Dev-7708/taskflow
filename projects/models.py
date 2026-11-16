from django.conf import settings
from django.db import models


class Project(models.Model):
    """A board that holds tasks and has a team of members."""

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Links a user to a project, and records what they are allowed to do.

    This is an explicit model rather than a plain ManyToManyField because the
    relationship carries data of its own: the role. Every permission check in
    the API reads from this table.
    """

    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        MEMBER = 'member', 'Member'
        VIEWER = 'viewer', 'Viewer'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can hold only one role per project.
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_member',
            )
        ]
        ordering = ['joined_at']

    def __str__(self):
        return f'{self.user} — {self.role} on {self.project}'

    @property
    def can_edit(self):
        """Owners and members may change tasks; viewers are read-only."""
        return self.role in {self.Role.OWNER, self.Role.MEMBER}

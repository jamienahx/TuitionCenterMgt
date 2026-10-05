import json
from pathlib import Path

from django.core.management.base import BaseCommand

from relief.models import (
    ReliefTeacher,
    Subject,
    Level,
    TeacherAvailability,
)


class Command(BaseCommand):
    help = "Seed the database with mock relief teacher data"

    def handle(self, *args, **options):
        file_path = Path(__file__).resolve().parents[2] / "mock_data.json"

        with open(file_path, "r") as file:
            data = json.load(file)

        # Clear existing teacher data
        ReliefTeacher.objects.all().delete()

        for teacher_data in data["teachers"]:

            # Create teacher
            teacher = ReliefTeacher.objects.create(
                name=teacher_data["name"],
                contact_number=teacher_data["contact_number"],
            )

            # Connect subjects
            for subject_name in teacher_data["subjects"]:
                subject, _ = Subject.objects.get_or_create(
                    name=subject_name
                )
                teacher.subjects.add(subject)

            # Connect levels
            for level_name in teacher_data["levels"]:
                level, _ = Level.objects.get_or_create(
                    name=level_name
                )
                teacher.levels.add(level)

            # Create availability
            for availability in teacher_data["availability"]:
                TeacherAvailability.objects.create(
                    teacher=teacher,
                    day_of_week=availability["day_of_week"],
                    start_time=availability["start_time"],
                    end_time=availability["end_time"],
                )

        self.stdout.write(
            self.style.SUCCESS("Mock relief teacher data seeded successfully!")
        )
from django.db import models


class Level(models.IntegerChoices):
    BASE = 0
    ADVANCED = 1
    EXPERT = 2


class Resource(models.Model):
    name = models.CharField(max_length=16)


class Town(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"Town: {self.name}"


class Skill(models.Model):
    attack = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    power = models.PositiveIntegerField()
    knowledge = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Attack: {self.attack} Defense: {self.defense} Power: {self.power} Knowledge: {self.knowledge}"


class Class(models.Model):
    name = models.CharField(max_length=16)
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE)
    

class SecondarySkill(models.Model):
    name = models.CharField(max_length=32)
    level = models.PositiveIntegerField(choices=Level.choices)
    description = models.TextField()


class Spell(models.Model):
    name = models.CharField(max_length=64)
    level = models.PositiveIntegerField(choices=Level.choices)
    description = models.TextField()


class HeroesClass(models.Model):
    name = models.CharField(max_length=16)


class Creatures(models.Model):
    class Upgrade(models.IntegerChoices):
        BASE = 0
        UPGRADE = 1

    name = models.CharField(max_length=64)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    level = models.PositiveIntegerField()
    upgrade = models.PositiveIntegerField(choices=Upgrade.choices)
    attack = models.PositiveIntegerField()
    defence = models.PositiveIntegerField()
    min_damage = models.PositiveIntegerField()
    max_damage = models.PositiveIntegerField()
    hp = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()
    growth = models.PositiveIntegerField()
    ai_value = models.PositiveIntegerField()
    gold = models.PositiveSmallIntegerField()
    wood = models.PositiveSmallIntegerField()
    ore = models.PositiveSmallIntegerField()
    mercury = models.PositiveSmallIntegerField()
    sulfur = models.PositiveSmallIntegerField()
    crystal = models.PositiveIntegerField()
    gems = models.PositiveSmallIntegerField()


class Specialty(models.Model):
    creature = models.ForeignKey(Creatures, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    secondary_skill = models.ForeignKey(SecondarySkill, on_delete=models.CASCADE)


class Heroes(models.Model):
    name = models.CharField(max_length=16)
    hero_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    seondary_skill_first = models.ForeignKey(SecondarySkill, related_name="first_skill", on_delete=models.CASCADE)
    secondary_skill_second = models.ForeignKey(SecondarySkill, related_name="second_skill", on_delete=models.CASCADE)
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)

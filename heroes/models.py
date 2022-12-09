from django.db import models


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


class DescriptionSecondarySkill(models.Model):
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.description


class SecondarySkill(models.Model):
    
    class Level(models.IntegerChoices):
        BASE = 0
        ADVANCED = 1
        EXPERT = 2
        
    name = models.CharField(max_length=32)
    level = models.PositiveIntegerField(choices=Level.choices)


class HeroesClass(models.Model):
    name = models.CharField(max_length=16)


class Heroes(models.Model):
    pass

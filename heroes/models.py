from django.db import models

class Spell(models.Model):
    name = models.CharField(max_length = 255)
    effect = models.CharField(max_length = 255)
    cells = models.CharField(max_length = 255)
    damage_type = models.CharField(max_length = 255)
    damage_formula = models.CharField(max_length = 255)
    level = models.IntegerField()
    description = models.CharField(max_length = 255)
    cost = models.IntegerField()

class Battle(models.Model):
    name = models.CharField(max_length = 60)
    state = models.CharField(max_length = 10)
    creator_pk = models.IntegerField()
    guest_pk = models.CharField(max_length = 255)
    creator_castle = models.CharField(max_length = 20)
    guest_castle = models.CharField(max_length = 20)
    growth = models.IntegerField()
    units = models.CharField(max_length = 20000)
    log = models.CharField(max_length = 20000)
    creator_spell = models.CharField(max_length = 200)
    guest_spell = models.CharField(max_length = 200)
    creator_current_mp = models.IntegerField()
    guest_current_mp = models.IntegerField()

class User(models.Model):
    user_name = models.CharField(max_length = 40)
    email = models.CharField(max_length = 40)
    password = models.CharField(max_length = 40)

class Player(models.Model):
    nick_name = models.CharField(max_length = 40)
    avatar = models.CharField(max_length = 60)
    rating = models.FloatField()
    win_count = models.IntegerField()
    loose_count = models.IntegerField()
    level = models.IntegerField()
    experience = models.IntegerField()
    skills = models.CharField(max_length = 255)
    special = models.CharField(max_length = 255)
    attributes = models.CharField(max_length = 255)
    spells = models.CharField(max_length = 255)

class AuthUser(models.Model):
    token = models.CharField(max_length = 40)

class Unit(models.Model):
    castle = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    attack_skill = models.IntegerField()
    defense_skill = models.IntegerField()
    minimum_damage = models.IntegerField()
    maximum_damage = models.IntegerField()
    health = models.IntegerField()
    speed = models.IntegerField()
    growth = models.IntegerField()
    special = models.CharField(max_length = 255)

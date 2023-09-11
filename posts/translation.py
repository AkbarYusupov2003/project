from modeltranslation.translator import TranslationOptions, register

from posts import models


@register(models.GlobalArea)
class GlobalAreaTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.ProgrammingArea)
class ProgrammingAreaTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.ProgrammingSkill)
class ProgrammingSkillTranslationOptions(TranslationOptions):
    fields = ("name",)

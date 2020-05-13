from django.db import models

# Create your models here.
class Sentences(models.Model):
    sentence = models.TextField()

    def __str__(self):
        return f"{self.id} - {self.sentence}"


class Definitions(models.Model):
    definition = models.TextField()
    dictionarySentence = models.ForeignKey(Sentences, on_delete=models.CASCADE, related_name="dictionarySentence")

    def __str__(self):
        return f"""
        {self.id} - {self.definition}
        """

class Words(models.Model):
    word = models.CharField(max_length=64)
    dictionaryDefinition = models.ManyToManyField(Definitions, blank=True, related_name="dictionaryDefinition")

    def __str__(self):
        return f"""
        {self.id} - {self.word}
        """

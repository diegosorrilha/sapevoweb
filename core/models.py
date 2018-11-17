from django.db import models

class Decisor(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=20)
    decisores = models.ManyToManyField('Decisor', related_name='+')
    # resultado_avaliacao = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Alternativa(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Criterio(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Peso(models.Model):
    codigo = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    valor = models.IntegerField()


class Avaliacao(models.Model):
    AM = 3
    MM = 2
    M = 1
    I = 0
    P = -1
    MP = -2
    AP = -3

    AVALIACAO_CHOICES = (
        (AM, 'Absolutamente Melhor'),
        (MM, 'Muito Melhor'),
        (M, 'Melhor'),
        (I, 'Igual / Equivalente'),
        (P, 'Pior'),
        (MP, 'Muito Pior'),
        (AM, 'Absolutamente Pior'),
    )

    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    decisor = models.ForeignKey('Decisor', on_delete=models.CASCADE)
    alternativa = models.ForeignKey('Alternativa', on_delete=models.CASCADE)
    criterio = models.ForeignKey('Criterio', on_delete=models.CASCADE)
    peso = models.CharField(max_length=5, choices=AVALIACAO_CHOICES, default=AM)

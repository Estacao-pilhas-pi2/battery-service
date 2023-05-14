from rest_framework import serializers
from stdnum.br import cnpj, cpf


class CPFField(serializers.CharField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.cpf_validator)

    def cpf_validator(self, value):
        try:
            cpf.validate(value)
        except cpf.ValidationError:
            raise serializers.ValidationError("CPF inválido.")


class CNPJField(serializers.CharField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.cnpj_validator)

    def cnpj_validator(self, value):
        try:
            cnpj.validate(value)
        except cnpj.ValidationError:
            raise serializers.ValidationError("CNPJ inválido.")

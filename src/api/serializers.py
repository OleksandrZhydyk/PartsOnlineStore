from rest_framework import serializers

from accounts.models import Comment, CustomUser
from catalogue.models import MachineModel, Part
from core.models import Shop


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class MachineModelSerializer(serializers.ModelSerializer):

    machine_type = serializers.SerializerMethodField("get_readable_machine_type")

    def get_readable_machine_type(self, model_object):
        readable_machine_type = model_object.get_machine_type_display()
        return readable_machine_type

    class Meta:
        model = MachineModel
        fields = (
            "id",
            "model",
            "machine_type",
        )


class MachineModelPartsSerializer(MachineModelSerializer):

    available_parts_by_model = serializers.SerializerMethodField("get_available_parts_by_model")

    def get_available_parts_by_model(self, model_object):
        parts = model_object.part.all()
        available_parts_by_model = {}
        for part in parts:
            available_parts_by_model[part.part_number] = {
                "part_name": part.part_name,
                "price": part.price,
                "remark": part.remark,
            }
        return available_parts_by_model

    class Meta:
        model = MachineModel
        fields = ("id", "model", "machine_type", "available_parts_by_model")


class PartSerializer(serializers.ModelSerializer):
    available_shops = ShopSerializer(many=True, read_only=True)
    related_machine_models = MachineModelSerializer(many=True, read_only=True)

    class Meta:
        model = Part
        fields = ("part_number", "part_name", "price", "remark", "available_shops", "related_machine_models")

    # available_shops = serializers.SerializerMethodField('get_available_shops')
    # related_machine_models = serializers.SerializerMethodField('get_related_machine_models')

    # def get_available_shops(self, part_object):
    #     shops = Shop.objects.filter(part=part_object.part_number)
    #     available_shops = {}
    #     for shop in shops:
    #         available_shops[shop.id] = shop.address
    #     return available_shops

    # def get_related_machine_models(self, part_object):
    #     models = MachineModel.objects.filter(part=part_object.part_number)
    #     related_machine_models = {}
    #     for model in models:
    #         related_machine_models[model.id] = {'machine_type': model.get_machine_type_display(),
    #                                             'model': model.model, }
    #     return related_machine_models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

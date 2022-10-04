from rest_framework.generics import UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from api.serializers import CustomUserSerializer, PartSerializer, MachineModelSerializer, MachineModelPartsSerializer
from catalogue.models import Part, MachineModel


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class PartListCreateView(ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class PartDeleteView(DestroyAPIView):
    queryset = Part.objects.all()
    lookup_field = "part_number"
    serializer_class = PartSerializer


class PartUpdateView(UpdateAPIView):
    queryset = Part.objects.all()
    lookup_field = "part_number"
    serializer_class = PartSerializer


class PartRetrieveView(RetrieveAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    lookup_field = 'part_number'


class ModelListCreateView(ListCreateAPIView):
    queryset = MachineModel.objects.all()
    serializer_class = MachineModelSerializer


class ModelDeleteView(DestroyAPIView):
    queryset = MachineModel.objects.all()
    lookup_field = "model"
    serializer_class = MachineModelSerializer


class ModelUpdateView(UpdateAPIView):
    queryset = MachineModel.objects.all()
    lookup_field = "model"
    serializer_class = MachineModelSerializer


class ModelRetrieveView(RetrieveAPIView):
    queryset = MachineModel.objects.all()
    lookup_field = "model"
    serializer_class = MachineModelPartsSerializer




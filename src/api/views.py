from rest_framework.generics import (DestroyAPIView, RetrieveAPIView,
                                     UpdateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from api.serializers import (CustomUserSerializer, MachineModelSerializer,
                             PartDetailSerializer, PartModelSerializer,
                             PartSerializer, ShopSerializer)
from catalogue.models import MachineModel, Part
from core.models import Shop


class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProfileUserView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class PartListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class PartCreateView(CreateAPIView):
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
    permission_classes = [AllowAny]
    queryset = Part.objects.all()
    serializer_class = PartDetailSerializer
    lookup_field = "part_number"


class ModelListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = MachineModel.objects.all()
    serializer_class = MachineModelSerializer


class ModelCreateView(CreateAPIView):
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
    permission_classes = [AllowAny]
    queryset = MachineModel.objects.all()
    lookup_field = "model"
    serializer_class = PartModelSerializer


class ShopListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ShopRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


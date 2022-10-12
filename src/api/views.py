from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from api.permissions import IsOwnerOrAdmin
from api.serializers import (CustomUserSerializer, MachineModelSerializer,
                             OrdersHistorySerializer, PartDetailSerializer,
                             PartModelSerializer, PartSerializer,
                             ShopSerializer)
from cart.models import OrdersHistory
from catalogue.models import MachineModel, Part
from core.models import Shop


class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProfileUserView(RetrieveAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProfileUserUpdateView(UpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class PartListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class PartCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class PartDeleteView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Part.objects.all()
    lookup_field = "part_number"
    serializer_class = PartSerializer


class PartUpdateView(UpdateAPIView):
    permission_classes = [IsAdminUser]
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
    permission_classes = [IsAdminUser]
    queryset = MachineModel.objects.all()
    serializer_class = MachineModelSerializer


class ModelDeleteView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = MachineModel.objects.all()
    lookup_field = "model"
    serializer_class = MachineModelSerializer


class ModelUpdateView(UpdateAPIView):
    permission_classes = [IsAdminUser]
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
    permission_classes = [IsAdminUser]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class OrdersHistoryRetrieveView(RetrieveAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = OrdersHistory.objects.all()
    serializer_class = OrdersHistorySerializer

    def get_object(self):
        return OrdersHistory.objects.get(user__pk=self.kwargs.get("pk"))


class OrdersHistoryListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = OrdersHistory.objects.all()
    serializer_class = OrdersHistorySerializer

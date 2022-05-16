from rest_framework import serializers
from .models import Renter, RenterAd, PictureAdRenter, Vehicle, Buckets, PhoneAd


class PictureAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureAdRenter
        fields = "img_ads",

class RenterSerializer(serializers.ModelSerializer):
    types_of_services = serializers.StringRelatedField(many=True)
    class Meta:
        model = Renter
        fields = "__all__"

class PhoneAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneAd
        fields = "phone_ad_renter",


class BucketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buckets
        exclude = ('vehicle_object', 'id', 'description')


class VehicleSerializer(serializers.ModelSerializer):
    buckets_set = BucketsSerializer(many=True, read_only=True)
    class Meta:
        model = Vehicle
        exclude = ('renter',)
        # fields = "__all__"


class MyRenterAdSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field="title", queryset=Category.objects.all())
    pictureadrenter_set = PictureAdSerializer(many=True, read_only=True)
    abs_url = serializers.SerializerMethodField()
    renter_ad = RenterSerializer(read_only=True)
    vehicle_ad = VehicleSerializer(read_only=True)


    # tags = serializers.ListField(child=serializers.CharField(required=False))  # TODO
    # last_attendance = serializers.SerializerMethodField()

    class Meta:
        model = RenterAd
        fields = '__all__'

    def get_abs_url(self, obj):
        return obj.get_absolute_url()

class RenterDetailViewSerializer(serializers.ModelSerializer):
    pictureadrenter_set = PictureAdSerializer(many=True, read_only=True)
    phonead_set = PhoneAdSerializer(many=True, read_only=True)

    renter_ad = RenterSerializer(read_only=True)
    vehicle_ad = VehicleSerializer(read_only=True)


    class Meta:
        model = RenterAd
        fields = "__all__"

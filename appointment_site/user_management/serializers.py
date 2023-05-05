

from rest_framework import serializers, generics
from .models import Patient, Counsellor, Appointment, User
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name','password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8},
        'id':{'read_only':True}
        
        }

class ExistUserPatientSerializer(serializers.ModelSerializer):
    user_email = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email', source='user')

    class Meta:
        model = Patient
        fields = ['id', 'user_email']
        extra_kwargs = {'id': {'read_only': True}}

class ExistUserCounsellorSerializer(serializers.ModelSerializer):
    user_email = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email', source='user')

    class Meta:
        model = Counsellor
        fields = ['id', 'user_email']
        extra_kwargs = {'id': {'read_only': True}}
  
class  PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Patient
        # fields = ['id',"user_id","is_active","email","name","password"]
        fields = "__all__"
        depth =1

    def create(self, validated_data):
        validated_data = validated_data.pop("user")
        user_email = validated_data['email']
        user_password = validated_data['password']
        user_name = validated_data['name']
        user, created = User.objects.get_or_create(email=user_email, defaults={'password': user_password, 
        'name':user_name})

        patient = Patient.objects.create(user=user)
        return patient
        
    def update(self, instance, validated_data):
        validated_data = validated_data.pop("user")
        user_email = validated_data.get('email',instance.user.email)
        if User.objects.filter(email=user_email).first():
           if not Patient.objects.filter(user__email=user_email).first(): 
                user_obj = User.objects.filter(email=user_email).first()
                instance.user = user_obj
                user.save()
                instance.save()
           else:
                user = instance.user
                user.password = validated_data.get('password',user.password)
                user.name = validated_data.get('name',user.name)
                user.save()
                instance.save()

        else:
            user_obj = User.objects.get(id=instance.user.id)
            instance.user.email = user_email
            instance.user.password = validated_data.get('password',user_obj.password)
            instance.user.name = validated_data.get('name',user_obj.name)
            instance.user.save()
            instance.save()
        return instance    


class CounsellorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Counsellor
        fields = "__all__"
        depth =1

    def create(self, validated_data):
        validated_data = validated_data.pop("user")
        user_email = validated_data['email']
        user_password = validated_data['password']
        user_name = validated_data['name']
        user, created = User.objects.get_or_create(email=user_email, defaults={'password': user_password, 
        'name':user_name})

        patient = Counsellor.objects.create(user=user)
        return patient
        
    def update(self, instance, validated_data):
        validated_data = validated_data.pop("user")
        user_email = validated_data.get('email',instance.user.email)
        if User.objects.filter(email=user_email).first():
           if not Counsellor.objects.filter(user__email=user_email).first(): 
                user_obj = User.objects.filter(email=user_email).first()
                instance.user = user_obj
                user.save()
                instance.save()
           else:
                user = instance.user
                user.password = validated_data.get('password',user.password)
                user.name = validated_data.get('name',user.name)
                user.save()
                instance.save()

        else:
            user_obj = User.objects.get(id=instance.user.id)
            instance.user.email = user_email
            instance.user.password = validated_data.get('password',user_obj.password)
            instance.user.name = validated_data.get('name',user_obj.name)
            instance.user.save()
            instance.save()
        return instance    
        

class AppointmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient')
    counsellor_id = serializers.PrimaryKeyRelatedField(queryset=Counsellor.objects.all(), source='counsellor')
    class Meta:
        model = Appointment
        fields = ['id', 'patient_id', 'counsellor_id', 'appointment_date', 'is_active']


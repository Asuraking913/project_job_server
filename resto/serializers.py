from rest_framework import serializers
from .models import Job, Profile, User, Product, Order, OrderItem

class ApplicationSerializer(serializers.Serializer):

    app_id = serializers.CharField()
    user_id = serializers.CharField()
    status = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Profile
        fields = '__all__'
        REQUIRED_FIELDS = [
        'job_title',
        'experience',
        'hourly_rate', 
        'languages', 
        'bio',
        'skills',
        'education',
        'linkdeln_link',
        ]


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in REQUIRED_FIELDS:
                if field in self.fields:
                    self.fields[field].required = True

class JobApplySerializer(serializers.Serializer):

    user_id = serializers.CharField()
    job_id = serializers.CharField()

class JobSerializer(serializers.ModelSerializer):

    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    company_size_display = serializers.CharField(source='get_company_size_display', read_only=True)

    class Meta:
        model = Job
        fields = [
        'id',
        'job_title', 
        'job_type', 
        'location', 
        'description', 
        'category', 
        'payment_type', 
        'min_budget', 
        'max_budget',
        'company_size',
        'required_skills',
        'special_skills',
        'duration',
        'job_type_display',
        'category_display',
        'payment_type_display',
        'company_size_display',
        ]

        extra_kwargs = {"id" : { "read_only" : True }}

        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {"password" : {"write_only" : True}}
    
    def create(self, validated_data):   
        user = User.objects.create_user(**validated_data)
        return user

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', "price", 'available_stock', "category", 'image']

class OrderItemsListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        order_item = [OrderItem(**items) for items in validated_data] 
        # print(order_item)
        return order_item
    
    def update(self, instance, validated_data):
        print(instance, "instance")
        print(validated_data, 'validated_data')
        return None

    
class OrderItemsSerializer(serializers.Serializer):

    # order = Order()
    # quantity = serializers.IntegerField()
    product = serializers.CharField()
    quantity = serializers.IntegerField()

    class Meta:
        list_serializer_class = OrderItemsListSerializer


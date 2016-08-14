from rest_framework import serializers
from authentication.models import Account
from django.contrib.auth import update_session_auth_hash

class AccountSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)
	confirm_password = serializers.CharField(write_only=True, required=False)



	class Meta:
		model = Account
		fields = ('id', 'email', 'username', 'created_at', 'updated_at',
				'first_name', 'last_name', 'tagline', 'password', 
				'confirm_password')

		read_only_fields = ('created_at', 'updated_at')

	def create(self, validated_data):
		return Account.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.username = validated_data.get('username', instance.username)
		instance.tagline = validated_data.get('tagline', instance.tagline)
		instance.tagline = validated_data.get('first_name', instance.first_name)
		instance.tagline = validated_data.get('last_name', instance.last_name)
		instance.email = validated_data.get('email', instance.email)

		instance.save()

		password = validated_data('password', instance.password)
		confirm_password = validated_data('confirm_password', instance.confirm_password)

		if password and confirm_password and password == confirm_password:
			instance.set_password()
			instance.save()

			update_session_auth_hash(self.content.get['request'], instance)

		return instance



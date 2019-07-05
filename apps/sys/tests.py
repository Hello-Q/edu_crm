from apps.sys.serializers import UserSerializer
from apps.sys.models import User

user = User.objects.all()[0]

serializer = UserSerializer(user)

print(serializer.data)
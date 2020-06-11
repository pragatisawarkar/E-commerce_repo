from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from sample.models import *
from sample.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

def responsedata(status,msg):
    response={"status":status,
              "msg":msg}
    return response

#create user role
class UserRoleCreateAPIView(CreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

#Customer Registration
class CustomerCreateAPIView(APIView):

    def post(self,request):
       if not request.data._mutable:
           request.data._mutable=True

       data=request.data

       if not data.get("password"):
           return Response(responsedata(False,"Password is required"),status=status.HTTP_406_NOT_ACCEPTABLE)

       if not data.get("first_name"):
           return Response(responsedata(False,"First Name is required"),status=status.HTTP_406_NOT_ACCEPTABLE)

       if not data.get("last_name"):
           return Response(responsedata(False,"Last Name is required"),status=status.HTTP_406_NOT_ACCEPTABLE)

       if User.objects.filter(email=data.get("email")).exists():
           return Response(responsedata(False,"Email is already registered with us..."),status=status.HTTP_409_CONFLICT)

       data['role']=UserRole.objects.filter(title='customer')[0].id
       data['password']=make_password(data.get("password"))

       request.data._mutable=False

       seriliazer=UserSerializer(data=data)
       if seriliazer.is_valid(raise_exception=True):
           seriliazer.save()
           token, _ = Token.objects.get_or_create(user=seriliazer.instance)
           return Response(responsedata("Success","Customer Registration done successfully..."))
       else:
           return Response(responsedata(False,"Invalid Serializer"),status=status.HTTP_401_UNAUTHORIZED)

#Vendor Registration
class VendorCreateAPIView(APIView):

    def post(self, request):
        if not request.data._mutable:
            request.data._mutable = True

        data = request.data

        if not data.get("password"):
            return Response(responsedata(False, "Password is required"), status=status.HTTP_406_NOT_ACCEPTABLE)

        if not data.get("first_name"):
            return Response(responsedata(False, "First Name is required"), status=status.HTTP_406_NOT_ACCEPTABLE)

        if not data.get("last_name"):
            return Response(responsedata(False, "Last Name is required"), status=status.HTTP_406_NOT_ACCEPTABLE)

        if User.objects.filter(email=data.get("email")).exists():
            return Response(responsedata(False, "Email is already registered with us..."),
                            status=status.HTTP_409_CONFLICT)

        data['role'] = UserRole.objects.filter(title='vendor')[0].id
        data['password'] = make_password(data.get("password"))

        request.data._mutable = False

        seriliazer = UserSerializer(data=data)
        if seriliazer.is_valid(raise_exception=True):
            seriliazer.save()
            token, _ = Token.objects.get_or_create(user=seriliazer.instance)
            return Response(responsedata("Success", "Vendor Registration done successfully..."))
        else:
            return Response(responsedata(False, "Invalid Serializer"), status=status.HTTP_401_UNAUTHORIZED)

#Customer Login
class CustomerLoginApiView(APIView):

    def post(self,request):
        data=request.data

        if not data.get("email"):
            return Response(responsedata(False,"Email Id is required"),status=status.HTTP_406_NOT_ACCEPTABLE)

        if not data.get("password"):
            return Response(responsedata(False,"Password is required"),status=status.HTTP_406_NOT_ACCEPTABLE)

        if not User.objects.filter(email=data.get("email")):
            return Response(responsedata(False,"User not found with this mail ID"),status=status.HTTP_404_NOT_FOUND)

        if not check_password(data.get("password"),User.objects.filter(email=data.get("email")).values()[0].get("password")):
            return Response(responsedata(False,"Password is incorrect"),status=401)

        userdata=User.objects.filter(email=data.get("email")).values()[0]
        token,_=Token.objects.get_or_create(user=userdata.get('id'))

        return Response({
            "status": True,
            "token": str(token),
            "data": {
                "first_name": userdata.get("first_name"),
                "last_name": userdata.get("last_name"),
                "email": userdata.get("email"),
            },
            "message": "Customer Login Successfully"
        },
            status=status.HTTP_200_OK)

# vendor login
class VendorLoginAPIView(APIView):

    def post(self, request):

        data = request.data

        if not data.get("email"):
            return Response(responsedata(False, "Email ID is required"), status=status.HTTP_406_NOT_ACCEPTABLE)

        if not data.get("password"):
            return Response(responsedata(False, "Password is required"), status=status.HTTP_406_NOT_ACCEPTABLE)

        if not User.objects.filter(email=data.get("email")):
            return Response(responsedata(False, "User not found with this email ID"), status=status.HTTP_404_NOT_FOUND)

        if not check_password(data.get("password"),
                              User.objects.filter(email=data.get("email")).values()[0].get("password")):
            return Response(responsedata(False, "Password is incorrect"), status=401)

        userdata = User.objects.filter(email=data.get("email")).values()[0]
        token, _ = Token.objects.get_or_create(user=userdata.get('id'))

        return Response({
            "status": True,
            "token": str(token),
            "data": {
                "first_name": userdata.get("first_name"),
                "last_name": userdata.get("last_name"),
                "email": userdata.get("email"),
            },
            "message": "Vendor Login Successfully"
        },
            status=status.HTTP_200_OK)

# create product
class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# place order
class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):

        #   Remove immutability
        if not request.data._mutable:
            request.data._mutable = True

        data = request.data
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        customer_id = Token.objects.filter(key=token)[0].user_id
        data['customer'] = customer_id

        product_id = Product.objects.filter(product_name=data['product_name'])[0].id
        data['product'] = product_id

        order_serializer = OrderSerializer(data=data)
        order_item_serializer = OrderItemSerializer(data=data)

        print('order_serializer', order_serializer)
        if order_serializer.is_valid(raise_exception=True):
            order_serializer.save()
            order_id = order_serializer.data['order_id']
            data['order'] = order_id

            if order_item_serializer.is_valid(raise_exception=True):
                order_item_serializer.save()
                return Response(responsedata("Success", f"Order placed successfully."),
                                status=status.HTTP_201_CREATED)
        else:
            return Response(responsedata(False, "Invalid Serializer"), status=status.HTTP_401_UNAUTHORIZED)


# accept order
class AcceptOrderAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        vendor_id = Token.objects.filter(key=token)[0].user_id

        orders = Order.objects.filter(vendor=vendor_id, order_status='placed')

        order_id = []
        for order in orders:
            order.order_status = 'accepted'
            order.save()
            order_id.append(order.order_id)

        if order_id:
            msg = f"{order_id} these Order id accepted successfully."
        else:
            msg = "There are no placed order "

        return Response(responsedata("Success", msg),
                        status=status.HTTP_200_OK)








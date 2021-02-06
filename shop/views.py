from rest_framework import generics, mixins, views
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.response import Response


# class ProductView(generics.GenericAPIView, mixins.ListModelMixin):
#     queryset = Product.objects.all().order_by('-id')
#     serializer_class = ProductSerializers
#     permission_classes = [IsAuthenticated, ]
#     authentication_classes = [TokenAuthentication, ]

#     def get(self, request):
#         return self.list(request)


class ProductView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        query = Product.objects.all()
        serializers = ProductSerializers(query, many=True)
        data = []
        for prod in serializers.data:
            fab_query = Favorit.objects.filter(
                user=user).filter(product_id=prod["id"])
            if fab_query:
                prod['favorit'] = fab_query[0].isFavorit
            else:
                prod['favorit'] = False
            data.append(prod)
        return Response(data)


class FavoritView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        data = request.data["id"]
        # print(data)
        try:
            product_obj = Product.objects.get(id=data)
            # print(data)
            user = request.user
            single_favorit_product = Favorit.objects.filter(
                user=user).filter(product=product_obj).first()
            if single_favorit_product:
                print("single_favorit_product")
                ccc = single_favorit_product.isFavorit
                single_favorit_product.isFavorit = not ccc
                single_favorit_product.save()
            else:
                Favorit.objects.create(
                    product=product_obj, user=user, isFavorit=True)
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class UserView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        user_obj = User.objects.get(username=user.username)
        serializer = UserSerializers(user_obj)
        return Response(serializer.data)


class Register(views.APIView):
    def post(self, request):
        serializers = UserSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error": False, "message": "User was Created!"})
        return Response({"error": True, "message": "User Not Created!"})


class CartView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        cart_obj = Cart.objects.filter(user=user).filter(isCompile=False)
        data = []
        cart_serializer = CartSerializers(cart_obj, many=True)
        for cart in cart_serializer.data:
            cart_product_obj = CartProduct.objects.filter(cart=cart["id"])
            cart_product_obj_serializer = CartProductSerializers(
                cart_product_obj, many=True)
            cart['cartproducts'] = cart_product_obj_serializer.data
            data.append(cart)
        return Response(data)

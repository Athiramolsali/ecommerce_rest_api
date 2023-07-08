from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from datetime import datetime, time
from .serializers import *
from .models import *
from rest_framework import status, generics,viewsets
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response



from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response 

    



#Create Customer
class CreateCustomer(GenericViewSet):

    def create(self,request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            
            name :str = serializer.validated_data.get('name', None)            
            email : str = serializer.validated_data.get('email', None)
            address : str = serializer.validated_data.get('address', None)
            #created_by = u_model.User.objects.get(id=request.user.id)

            candidate_engmnt = Customer.objects.create(name=name,email=email,address=address,created_by_id=request.user.id)
            return Response(data={"detail":"Customer Created Successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"detail":"Customer Creation Failed"}, status=status.HTTP_403_FORBIDDEN)
 #Update Customer Details       
class UpdateCustomer(GenericViewSet):
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(data={"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response(data={"detail": "Customer updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"detail": "Customer update failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   


#Retrieve Single Customer
class SingleGetCustomer(GenericViewSet):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(data={"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
#Delete  Customer
class DeleteCustomer(GenericViewSet):
    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(data={"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(data={"detail": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



#List All Products
class ProductAllList(GenericViewSet):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

#Create Products
class ProductCreate(GenericViewSet):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductDetail(GenericViewSet):
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_product(pk)
        if not product:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk):
        product = self.get_product(pk)
        if not product:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        if not product:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






#Make the product active /inactive. Inactive the product only if it is registered before 2 months.
class ProductUpdateDetail(GenericViewSet):
    def update(self, request, pk):
            product = Product.objects.get(pk=pk)
            if not product:
                return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                registration_date = product.registration_date

                if (timezone.now() - registration_date).days > 60:
                    serializer.validated_data['active'] = False

                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render,redirect,  get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .models import HealthRecord
from .serializers import HealthRecordSerializer
from .blockchain import create_record, grant_access, revoke_access, get_record
import ipfs_api
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
import ipfshttpclient2
import mimetypes

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ipfs_hash = serializer.validated_data['ipfs_hash']
        instance = serializer.save(patient=self.request.user)
        create_record(self.request.user.ethereum_address, instance.record_id, ipfs_hash)

    @action(detail=True, methods=['post'])
    def grant_access(self, request, pk=None):
        record = self.get_object()
        doctor_address = request.data.get('doctor_address')
        if doctor_address:
            tx_receipt = grant_access(request.user.ethereum_address, record.record_id, doctor_address)
            return Response({'message': 'Access granted', 'transaction_hash': tx_receipt.transactionHash.hex()})
        return Response({'error': 'Doctor address is required'}, status=400)

    @action(detail=True, methods=['post'])
    def revoke_access(self, request, pk=None):
        record = self.get_object()
        doctor_address = request.data.get('doctor_address')
        if doctor_address:
            tx_receipt = revoke_access(request.user.ethereum_address, record.record_id, doctor_address)
            return Response({'message': 'Access revoked', 'transaction_hash': tx_receipt.transactionHash.hex()})
        return Response({'error': 'Doctor address is required'}, status=400)

@csrf_exempt
def upload_file(request):
    health_record = HealthRecord()
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = file.name
        file_content = file.read()
        file_record_type = request.POST['records']
        
        # Save the file temporarily
        temp_file_path = f"{settings.MEDIA_ROOT}/temp_{file_name}"
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file_content)
            
        cid = ipfs_api.publish(temp_file_path)
        ipns_key = f"HealthRecord_{file_name}"
        ipfs_api.create_ipns_record(ipns_key)
        ipfs_api.update_ipns_record(ipns_key, temp_file_path)
        import os
        os.remove(temp_file_path)
        health_record = HealthRecord.objects.create(
                patient=request.user,
                record_id=cid,
                ipfs_hash=ipns_key,
            )
        return HttpResponse(f"File uploaded to IPFS. CID: {cid}, IPNS Key: {ipns_key}")
    return render(request, 'upload.html')

def retrieve_file(request, cid):
    try:
        client = ipfshttpclient2.connect()
        file_data = client.cat(cid)
        file_extension = cid.split('.')[-1]
        content_type = mimetypes.guess_type(f"file.{file_extension}")[0] or 'application/octet-stream'
        response = HttpResponse(file_data, content_type=content_type)
        response['Content-Disposition'] = 'inline' 
        return response
    except Exception as e:
        return HttpResponse(f"Error retrieving file: {str(e)}", status=404)
    
    
@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login/')
def record_detail(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk)
    record_content = ipfs_api.cat(record.ipfs_hash)
    access_logs = record.accesslog_set.all()
    return render(request, 'record_detail.html', {
        'record': record,
        'record_content': record_content,
        'access_logs': access_logs
    })

@login_required(login_url='/login/')
def view_records(request):
    records = HealthRecord.objects.filter(patient=request.user)
    return render(request, 'view_records.html', {'records': records})
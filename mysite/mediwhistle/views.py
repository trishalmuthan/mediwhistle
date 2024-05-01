from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .models import Document, Comment, Form
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from .forms import YourForm

def check_user_type(request):
    if not request.user.is_authenticated:
        return HttpResponse("You are an anonymous user.")

    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # This means it's a Django admin without a profile
        return HttpResponse("You are a Django admin.")

    if profile.is_site_admin:
        return HttpResponse("You are a site admin.")
    else:
        return HttpResponse("You are a common user with an account.")

class DocumentCreateView(CreateView):
    model = Document
    fields = ['upload']
    success_url = reverse_lazy('upload_success')  # Make sure this URL name is defined in your urls.py
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user  # Assign the logged-in user to the document
        else:
            form.instance.user = None  # Don't assign a user if no one is logged in
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.all()
        context['documents'] = documents
        return context

def uploadSuccessView(request):
    return render(request, "upload_success.html")

@login_required
def user_document_list(request):
    forms = Form.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'user_document_list.html', {'forms': forms})

@login_required
def admin_document_list(request):
    forms = Form.objects.all().order_by('-uploaded_at')
    return render(request, 'admin_document_list.html', {'forms': forms})

@login_required
def view_document(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    return render(request, 'document_detail.html', {'form': form})

@login_required
def update_document_status(request, form_id):
    # if not request.user.is_superuser:
    #     # Redirect non-admins to a general page or login
    #     return redirect('login')  # Assuming 'login' is the URL name for your login page
    
    form = get_object_or_404(Form, pk=form_id)
    if form.status == "new":
        form.status = 'In Progress'
        form.save()
        # Redirect to a detail view or back to the document list might be more appropriate here
    return render(request, 'document_detail.html', {'form': form})
    #return redirect('admin_document_list')
    # else:
    #     # Handle cases where the document is not new, redirect or show an error as necessary
    #     return redirect('admin_document_list')  # Redirect back to the document list for simplicity
    
    
@login_required
def comment_form(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    if request.method == 'POST':
        # Handle comment submission and status update here if form is submitted
        pass
    else:
        # Render empty form for GET request
        return render(request, 'comment_form.html', {'form': form})

@login_required
def submit_comment(request, form_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        # Assuming you validate the comment and save it...
        new_comment = Comment.objects.create(form_id=form_id, author=request.user, text=comment_text)

        return JsonResponse({
            'success': True,
            'comment': new_comment.text,
            'author': new_comment.author.username
        })
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def mark_as_resolved(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    form.status = 'resolved'
    form.save()
    # Redirect back to the document list or wherever is appropriate
    return redirect('admin_document_list')

def report_form(request):
    if request.method == 'POST':
        form = YourForm(request.POST, request.FILES)
        if form.is_valid():
            if any(form.cleaned_data.values()):
                if request.user.is_authenticated:
                    form.instance.user = request.user  # Assign the logged-in user to the document
                else:
                    form.instance.user = None  # Don't assign a user if no one is logged in

                form.save()
                return redirect('/upload/success')
            else:
                return redirect('/report-form')
    else:
        form = YourForm()

    return render(request, 'report_form.html', {'form': form})

@login_required
def delete_document(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    # Check if the user is the owner of the document or an admin
    if request.user == form.user or request.user.userprofile.is_site_admin:
        form.file.delete()  # This deletes the file from S3
        form.delete()         # This deletes the document record from the database
    
    if request.user == form.user:
        return redirect('user_document_list') 
    else:
        return redirect('admin_document_list') 

@login_required
def login_redirect(request):
    try:
        if request.user.userprofile.is_site_admin:
            return redirect('/all_documents')
    except UserProfile.DoesNotExist:
        pass
    return redirect('/upload')
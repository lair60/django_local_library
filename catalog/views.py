from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Book, Author, BookInstance, Genre, RenewBookModelForm
@login_required
def index(request):
       """
       Función vista para la página inicio del sitio.
       """
       # Genera contadores de algunos de los objetos principales
       num_books=Book.objects.all().count()
       num_instances=BookInstance.objects.all().count()
       # Libros disponibles (status = 'a')
       num_instances_available=BookInstance.objects.filter(status__exact='a').count()
       num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.
	
       num_genre=Genre.objects.all().count()
       search_word='the'
       num_book_search = Book.objects.filter(title__icontains=search_word).count()
	
	   # Number of visits to this view, as counted in the session variable.
       num_visits = request.session.get('num_visits', 1)
       request.session['num_visits'] = num_visits + 1
    
       # Renderiza la plantilla HTML index.html con los datos en la variable contexto
       return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,
		'num_authors':num_authors, 'num_genre': num_genre, 'search_word': search_word,
		'num_book_search': num_book_search, 'num_visits': num_visits},
       )
from catalog.forms import CreateNewUserForm
from django.contrib.auth.models import User
import secrets
from django.core.mail import send_mail



from django.core.mail import EmailMessage
from django.urls import reverse
def createNewUser(request):
    context = {}
    if request.method == 'POST':       
        

        # Create a form instance and populate it with data from the request (binding):
        form = CreateNewUserForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            email_user = form.cleaned_data['email_user']
            if User.objects.filter(email=email_user).count() == 0:
                # redirect to a new URL:
                context = {'email': email_user}                
                password = secrets.token_urlsafe(16)             
                user = User.objects.create_user(email_user, email_user, password)
                if request.is_secure():
                    url= "https://"
                else:
                    url= "http://"
                url= url + request.get_host() + reverse ('login')
				
                message_email_html = (f'<p><b>Hello</b>,</p><br>'
                                       f'<p>As per your request, here are the details of the new user:</p><br>'
                                       f'<p>       <b>Username</b>: {email_user}</p>'
                                       f'<p>       <b>Password</b>: {password}</p><br>'
                                       f"""<p>To log in, visit <a href=\'{url}\' target='_blank'>{url}</a> and enter in your username and password.</p>"""
                                       f'<p>If you have questions or comments please email me anytime at <a href="mailto:lair60@yahoo.es" target="_blank">lair60@yahoo.es</a>.</p>'
                                       f'<p>Thanks!</p>'
                                       f'<p>Luis Inga</p>'
                                       f'<p><a href="https://www.luisingarivera.com" target="_blank">https://www.luisingarivera.com</a></p>')
                msg = EmailMessage('Your new user details', message_email_html, 'lair60@yahoo.es', [email_user])
                """
                send_mail(
                    'User Created',
                    'Username: '+ email_user + ' password: '+ password,
                    'lair60@yahoo.es',
                    [email_user],
                    fail_silently=False,
                )
				"""
                msg.content_subtype = "html"
                msg.send()
            return render(request, 'catalog/user_created.html', context)
    else:
        template_name ='catalog/create_user_form.html'
        form = CreateNewUserForm()
        context = {'form': form}

    return render(request, 'catalog/create_user_form.html', context)
		

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    template_name = 'books/book_list.html'  # Specify your own template name/location
    paginate_by = 2
    def get_queryset(self):
       return Book.objects.all()
       #return Book.objects.filter(title__icontains='wise')[:5] # Get 5 books containing the title war
		
class BookDetailView(generic.DetailView):
    model = Book
	
class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = "author_list"
    template_name = "authors/author_list.html"
    def get_queryset(self):
        return Author.objects.all()

class AuthorDetailView(generic.DetailView):
	model = Author
	
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin		
class LoanedBooksByLibrarianListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

#from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
		#form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			#book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		#form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author

class AuthorCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('authors')
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from words.forms import WordCounterForm

from word_count import search_directory
from .forms import UserRegisterForm


def register(request):
    """
    This view function acts as the post and get of the register page.
    :param request: The HTTP request body, if it's a POST request it should contain the form within
    :return: redirect to a template
    """
    if request.method == 'POST':
        # Assign the form with the request content
        form = UserRegisterForm(request.POST)
        # Verify it and redirect to the login page
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for {}!'.format(username))
            return redirect('login')
    else:
        # retrieve the empty user registration form
        form = UserRegisterForm()
    return render(request, 'words/register.html', {'form': form})


class CountWords(LoginRequiredMixin, View):

    def get(self, request):
        """
        Get the home page with an empty WordCounterForm
        :param request: The HTTP request body
        :return: render the home page
        """

        form = WordCounterForm()
        return render(request, 'words/home.html', {'form': form})

    def post(self, request):
        """
        Post the WordCounterForm, verify it and apply the search on the path given in the form.
        :param request: The HTTP request body containing the form
        :return: if valid render search-word page with the json result, else redirect to home page
        """
        form = WordCounterForm(data=request.POST)

        if form.is_valid():
            form_dict = form.cleaned_data

            data = search_directory(form_dict['directory_path'], form_dict['word'])

            return render(request, 'words/search-word.html', {'data': data})
        else:
            return redirect('home')


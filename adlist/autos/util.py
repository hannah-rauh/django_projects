from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

class AutosListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """

class AutosDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """

class AutosCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the ads to the saved object.
    """

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(AutosCreateView, self).form_valid(form)

class AutosUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(AutosUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class AutosDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(AutosDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView

from catalog.models import Category, Product, Tag, TagGroup
from orders.models import Order

from .forms import LoginForm, ProfileForm, RegisterForm


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get("q", "").strip()
        category_slug = self.request.GET.get("category", "")
        tag_slugs = self.request.GET.getlist("tag")

        products_qs = (
            Product.objects.filter(is_active=True, images__isnull=False)
            .distinct()
            .select_related("category")
            .prefetch_related("images", "tags")
        )
        if q:
            products_qs = products_qs.filter(name__icontains=q)
        if category_slug:
            products_qs = products_qs.filter(category__slug=category_slug)
        for slug in tag_slugs:
            products_qs = products_qs.filter(tags__slug=slug)

        products = []
        for product in products_qs[:12]:
            images = list(product.images.all())
            main_image = next((img for img in images if img.is_main), None)
            product.main_image = main_image or (images[0] if images else None)
            products.append(product)

        active_tag_objects = (
            list(Tag.objects.filter(slug__in=tag_slugs)) if tag_slugs else []
        )

        context.update({
            "products": products,
            "categories": Category.objects.filter(parent=None),
            "tag_groups": TagGroup.objects.prefetch_related("tags").all(),
            "q": q,
            "active_category": category_slug,
            "active_tags": set(tag_slugs),
            "active_tags_list": tag_slugs,
            "active_tag_objects": active_tag_objects,
            "is_filtered": bool(q or category_slug or tag_slugs),
        })
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactsView(TemplateView):
    template_name = "core/contacts.html"


class RegisterView(FormView):
    template_name = "core/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("core:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:profile")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        messages.success(self.request, f"Добро пожаловать, {user.name}!")
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "core/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:profile")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        next_url = self.request.GET.get("next") or self.get_success_url()
        return redirect(next_url)


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect("core:home")


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "core/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("core:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = (
            Order.objects.filter(client=self.request.user)
            .select_related("product")
            .order_by("-created_at")
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлён.")
        return super().form_valid(form)

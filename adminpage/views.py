from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth.models import User
from cart.models import Order
from .forms import CategoryForm, ProductForm


class AddItemsView(View):

    template_name = "admin/add_items.html"

    # -----------------------------------
    # 🔹 Dashboard + Performance Stats
    # -----------------------------------
    def get_dashboard_stats(self):

        total_orders = Order.objects.count()

        pending_orders = Order.objects.filter(
            delivery_status="Pending"
        ).count()

        completed_orders = Order.objects.filter(
            delivery_status="Delivered"
        ).count()

        cancelled_orders = Order.objects.filter(
            delivery_status="Cancelled"
        ).count()

        # 💰 Total Revenue (only completed/ordered)
        total_revenue = Order.objects.filter(
            is_ordered=True
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        # 👥 Total Users
        total_users = User.objects.count()

        # 🆕 Latest Order
        latest_order = Order.objects.order_by("-ordered_date").first()

        return {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
            "total_revenue": total_revenue,
            "total_users": total_users,
            "latest_order": latest_order,
        }

    # -----------------------------------
    # 🔹 GET METHOD
    # -----------------------------------
    def get(self, request):

        category_form = CategoryForm(prefix="cat")
        product_form = ProductForm(prefix="pro")

        # Orders for table
        orders = Order.objects.all().order_by("-ordered_date")

        paginator = Paginator(orders, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "category_form": category_form,
            "product_form": product_form,
            "page_obj": page_obj,
        }

        context.update(self.get_dashboard_stats())

        return render(request, self.template_name, context)

    # -----------------------------------
    # 🔹 POST METHOD
    # -----------------------------------
    def post(self, request):

        category_form = CategoryForm(prefix="cat")
        product_form = ProductForm(prefix="pro")

        if "cat_submit" in request.POST:
            category_form = CategoryForm(request.POST, request.FILES, prefix="cat")

            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Category added successfully ✅")
                return redirect("shop:add_items")

        elif "pro_submit" in request.POST:
            product_form = ProductForm(request.POST, request.FILES, prefix="pro")

            if product_form.is_valid():
                product_form.save()
                messages.success(request, "Product added successfully ✅")
                return redirect("shop:add_items")

        # Reload orders if form invalid
        orders = Order.objects.all().order_by("-ordered_date")
        paginator = Paginator(orders, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "category_form": category_form,
            "product_form": product_form,
            "page_obj": page_obj,
        }

        context.update(self.get_dashboard_stats())

        return render(request, self.template_name, context)

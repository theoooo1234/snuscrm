from django import forms
from django.contrib.auth.models import User, Group
from core.models import Company


class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    # company fields
    company_name  = forms.CharField(max_length=120)
    vat_number    = forms.CharField(max_length=40, required=False)
    register_number = forms.CharField(max_length=40, required=False)
    phone         = forms.CharField(max_length=40, required=False)
    delivery_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password",
                  "company_name", "vat_number", "register_number",
                  "phone", "delivery_address"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False              # pending approval by Sales
        if commit:
            user.save()
            # create company and link
            Company.objects.create(
                name  = self.cleaned_data["company_name"],
                vat_number = self.cleaned_data["vat_number"],
                register_number = self.cleaned_data["register_number"],
                email  = self.cleaned_data["email"],
                phone  = self.cleaned_data["phone"],
                delivery_address = self.cleaned_data["delivery_address"],
                contact_person = user.username,
                owner=user
            )
            Group.objects.get(name="Customer").user_set.add(user)
        return user

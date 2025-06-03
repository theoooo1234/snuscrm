from django import forms
from django.contrib.auth.models import User, Group
from core.models import Company


class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)


    company_name     = forms.CharField(label="Company name", max_length=120)
    vat_number       = forms.CharField(label="VAT number", max_length=40, required=False)
    register_number  = forms.CharField(label="Business register #", max_length=40, required=False)
    phone            = forms.CharField(max_length=40, required=False)
    delivery_address = forms.CharField(widget=forms.Textarea, required=False)
    contact_person   = forms.CharField(max_length=120, required=False)
    country          = forms.CharField(max_length=60, required=False)

    class Meta:
        model  = User
        fields = ["username", "email", "password",
                  "company_name", "vat_number", "register_number",
                  "phone", "delivery_address", "contact_person", "country"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            Group.objects.get(name="Customer").user_set.add(user)

            company, _ = Company.objects.get_or_create(
                name=self.cleaned_data["company_name"].strip(),
                defaults=dict(
                    vat_number       = self.cleaned_data["vat_number"],
                    register_number  = self.cleaned_data["register_number"],
                    email            = self.cleaned_data["email"],
                    phone            = self.cleaned_data["phone"],
                    delivery_address = self.cleaned_data["delivery_address"],
                    contact_person   = self.cleaned_data["contact_person"],
                    country          = self.cleaned_data["country"],
                ),
            )

            if company.owner is None:
                company.owner = user
                company.save(update_fields=["owner"])

        return user

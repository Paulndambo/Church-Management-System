from django.db import models

from apps.users.models import AbstractBaseModel
# Create your models here.
LOAN_PAYMENT_STATUS = [
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Overdue", "Overdue"),
]

class LoanType(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Interest rate as a percentage"
    )
    minimum_amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Minimum loan amount"
    )
    maximum_amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Maximum loan amount"
    )
    duration_in_months = models.PositiveIntegerField(
        help_text="Duration of the loan in months"
    )
    church = models.ForeignKey(
        "core.Church",
        on_delete=models.CASCADE,
        related_name="churchloantypes",
    )

    def __str__(self):
        return self.name


class Loan(AbstractBaseModel):
    borrower = models.ForeignKey(
        "membership.Member",
        on_delete=models.CASCADE,
        related_name="loans",
    )
    loan_type = models.ForeignKey(
        LoanType,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    church = models.ForeignKey(
        "core.Church",
        on_delete=models.CASCADE,
        related_name="churchloans",
    )


    def __str__(self):
        return f"Loan {self.id} for {self.borrower}"
    
class LoanSchedule(AbstractBaseModel):
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    payment_due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")


    def __str__(self):
        return f"Schedule {self.id} for Loan {self.loan.id}"

class LoanPayment(AbstractBaseModel):
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    church = models.ForeignKey(
        "core.Church",
        on_delete=models.CASCADE,
        related_name="churchloanpayments",
    )
    


    def __str__(self):
        return f"Payment {self.id} for Loan {self.loan.id}"
    

class LoanApplication(AbstractBaseModel):
    applicant = models.ForeignKey(
        "membership.Member",
        on_delete=models.CASCADE,
        related_name="loan_applications",
    )
    loan_type = models.ForeignKey(
        LoanType,
        on_delete=models.CASCADE,
        related_name="loan_applications",
    )
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    application_date = models.DateField(auto_now_add=True)
    status_choices = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    status = models.CharField(
        max_length=10, choices=status_choices, default="Pending"
    )
    church = models.ForeignKey(
        "core.Church",
        on_delete=models.CASCADE,
        related_name="churchloanapplications",
    )

    def __str__(self):
        return f"Loan Application {self.id} by {self.applicant}"
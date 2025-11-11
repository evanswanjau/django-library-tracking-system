from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

"""
Define check_overdue_loans that executes daily.
Query all loans where is_returned is False and due_date is past.
Send an email reminder to each member with overdue books.
"""
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def check_overdue_loans(self):
    try:
        # Get loan data
        overdue_loans = Loan.queryset.filter(is_returned=False, due_date__lt=timezone.now().date())
        for loan in overdue_loans:
            send_mail(
                subject='Your Book Loan is Overdue',
                message=f'Hello {loan.member.user.username},\n\nYou loan for "{loan.book.title}" is overdue.\nPlease return it as soon as possible.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[loan.member.user.email],
                fail_silently=False,
            )
    except Exception as exc:
        raise self.retry(exc=exc)

from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
import random

def home(request):
    return render(request,'home.html')

def open(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        aadhar = request.POST.get('aadhar')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        img = request.FILES.get('img')
        address = request.POST.get('address')
        pin = request.POST.get('pin')

        last_account = Account.objects.order_by('id').last()  # Get the last account to increment
        if last_account:
            account_number = f"{int(last_account.account_number) + 1:012d}"
        else:
            account_number = "100000000001"  # First account number if no accounts exist

        encrypted_pin = ''.join(chr(97 + int(digit)) for digit in pin)

        account = Account.objects.create(
            account_number=account_number,
            name=name,
            aadhar=aadhar,
            mobile=mobile,
            email=email,
            img=img,
            address=address,
            pin=encrypted_pin
        )

        context = {
            'account_number': account.account_number,
            'name': account.name,
            'aadhar': account.aadhar,
            'mobile': account.mobile,
            'email': account.email,
            'img' : account.img,
            'address': account.address,
            'pin': encrypted_pin
        }

        try:
            send_mail(
                "Account Details",   # Subject
                f"Dear {name},\n\nYour new account details are as follow:\n\nName: {name}\n\nEmail: {email}\n\nAadhar No: {aadhar}\n\nAccount Number: {account_number}\n\nMobile Number: {mobile}\n\nYou are instructed to generate your PIN for seamless banking operations.\n\nSafe Banking Ahead!\n\nHDFC Bank",
                settings.EMAIL_HOST_USER,
                [f"{email}"],
                fail_silently=False,
            )
            success_message = f"Account created successfully! ✅"

        except Exception as e:
            return HttpResponse(f'Error sending mail: {e}')

    return render(request,'open.html', {'success_message' : success_message})

def transfer(request):
    if request.method == 'POST':
        sender_account_number = request.POST.get('sender_account_number').strip()
        pin = request.POST.get('pin').strip()  # The PIN entered by the user
        transfer_type = request.POST.get('transfer_type')  # 'account', 'mobile', or 'email'
        amount = request.POST.get('amount')
        receiver = request.POST.get('receiver').strip()

        try:
            amount = float(amount)
            
            if amount <= 0:
                return render(request, 'transfer.html', {'error_message': 'Amount must be greater than zero.'})
            
            # Fetch the sender account by account number
            sender_account = Account.objects.filter(account_number=sender_account_number).first()
            if not sender_account:
                return render(request, 'transfer.html', {'error_message': 'Sender account not found.'})

            # Decrypt the stored PIN and check for validity
            encrypted_pin = sender_account.pin
            decrypted_pin = ''.join(str(ord(c) - 97) for c in encrypted_pin)

            if pin != decrypted_pin:
                return render(request, 'transfer.html', {'error_message': 'Incorrect PIN.'})

            # Check for sufficient balance
            if amount > sender_account.balance:
                return render(request, 'transfer.html', {'error_message': 'Insufficient balance.'})

            # Transfer logic for different types
            if transfer_type == 'account':
                # Receiver account number
                receiver_account = Account.objects.filter(account_number=receiver).first()
                if not receiver_account:
                    return render(request, 'transfer.html', {'error_message': 'Receiver account not found.'})

                # Debit the sender and credit the receiver account
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                # Send transaction confirmation email to receiver
                send_mail(
                    "Money Transfer Successful",
                    f"Dear {receiver_account.name},\n\nYou have received ₹{amount} from {sender_account.name}. Your new balance is ₹{receiver_account.balance}.",
                    settings.EMAIL_HOST_USER,
                    [receiver_account.email],
                    fail_silently=False,
                )

                # Success response
                return render(request, 'transfer.html', {
                    'success_message': f'₹{amount} has been successfully transferred to {receiver_account.name}.'
                })

            elif transfer_type == 'mobile':
                # Receiver mobile number (assuming it's stored as a field in the model)
                receiver_account = Account.objects.filter(mobile=receiver).first()
                if not receiver_account:
                    return render(request, 'transfer.html', {'error_message': 'Receiver mobile number not found.'})

                # Debit the sender account and credit the receiver account
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                # Send email to receiver about the transfer
                send_mail(
                    "Money Transfer Successful",
                    f"Dear {receiver_account.name},\n\nYou have received ₹{amount} from {sender_account.name}. Your new balance is ₹{receiver_account.balance}.",
                    settings.EMAIL_HOST_USER,
                    [receiver_account.email],
                    fail_silently=False,
                )

                # Success response
                return render(request, 'transfer.html', {
                    'success_message': f'₹{amount} has been successfully transferred to {receiver_account.name} (Mobile).'
                })

            elif transfer_type == 'email':
                # Receiver Gmail (email address)
                receiver_account = Account.objects.filter(email=receiver).first()
                if not receiver_account:
                    return render(request, 'transfer.html', {'error_message': 'Receiver email not found.'})

                # Debit the sender account and credit the receiver account
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                # Send email to receiver about the transfer
                send_mail(
                    "Money Transfer Successful",
                    f"Dear {receiver_account.name},\n\nYou have received ₹{amount} from {sender_account.name}. Your new balance is ₹{receiver_account.balance}.",
                    settings.EMAIL_HOST_USER,
                    [receiver],
                    fail_silently=False,
                )

                # Success response
                return render(request, 'transfer.html', {
                    'success_message': f'₹{amount} has been successfully transferred to {receiver_account.name} (Email).'
                })

            else:
                return render(request, 'transfer.html', {'error_message': 'Invalid transfer type selected.'})

        except ValueError:
            return render(request, 'transfer.html', {'error_message': 'Please enter a valid amount.'})
        except Exception as e:
            return render(request, 'transfer.html', {'error_message': f'An unexpected error occurred: {e}'})

    return render(request, 'transfer.html')



def credit(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number').strip()
        pin = request.POST.get('pin').strip()  # The PIN entered by the user
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            if amount <= 0:
                return render(request, 'credit.html', {'error_message': 'Deposit amount must be greater than zero.'})

            # Fetch the account by account number
            account = Account.objects.filter(account_number=account_number).first()
            if not account:
                return render(request, 'credit.html', {'error_message': 'Account not found.'})

            encrypted_pin = account.pin
            decrypted_pin = ''.join(str(ord(c) - 97) for c in encrypted_pin)

            if pin != decrypted_pin:
                return render(request, 'credit.html', {'error_message': 'Incorrect PIN.'})

            # Credit the amount to the account balance
            account.balance += amount
            account.save()

            # Send a success email with transaction details
            send_mail(
                "Transaction Successful",  # Subject
                f"Dear {account.name},\n\nYour account has been credited with ₹{amount}. Your new balance is ₹{account.balance}.\n\nHDFC Bank",
                settings.EMAIL_HOST_USER,  # Sender email (configured in settings.py)
                [account.email],  # Recipient email
                fail_silently=False,
            )

            # Return success message
            return render(request, 'credit.html', {
                'success_message': f'₹{amount} has been successfully credited to your account.',
                'account': account
            })

        except ValueError:
            return render(request, 'credit.html', {'error_message': 'Please enter a valid amount.'})
        except Exception as e:
            return render(request, 'credit.html', {'error_message': f'An unexpected error occurred: {e}'})

    return render(request, 'credit.html')

def debit(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number').strip()
        pin = request.POST.get('pin').strip()  # The PIN entered by the user
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            
            # Check for valid amount (must be greater than 0 and less than or equal to the account balance)
            if amount <= 0:
                return render(request, 'debit.html', {'error_message': 'Amount must be greater than zero.'})
            
            # Fetch the account by account number
            account = Account.objects.filter(account_number=account_number).first()
            if not account:
                return render(request, 'debit.html', {'error_message': 'Account not found.'})
            
            # Check if there's sufficient balance
            if amount > account.balance:
                return render(request, 'debit.html', {'error_message': 'Insufficient balance.'})

            # Decrypt the stored PIN
            encrypted_pin = account.pin
            decrypted_pin = ''.join(str(ord(c) - 97) for c in encrypted_pin)

            # Compare the entered PIN with the decrypted PIN
            if pin != decrypted_pin:
                return render(request, 'debit.html', {'error_message': 'Incorrect PIN.'})

            # Debit the amount from the account balance
            account.balance -= amount
            account.save()

            # Send a success email with transaction details
            send_mail(
                "Transaction Successful",  # Subject
                f"Dear {account.name},\n\nYour account has been debited with ₹{amount}. Your new balance is ₹{account.balance}.\n\nHDFC Bank",
                settings.EMAIL_HOST_USER,  # Sender email (configured in settings.py)
                [account.email],  # Recipient email
                fail_silently=False,
            )

            # Return success message
            return render(request, 'debit.html', {
                'success_message': f'₹{amount} has been successfully debited from your account.',
                'account': account
            })

        except ValueError:
            return render(request, 'debit.html', {'error_message': 'Please enter a valid amount.'})
        except Exception as e:
            return render(request, 'debit.html', {'error_message': f'An unexpected error occurred: {e}'})

    return render(request, 'debit.html')


def balance(request):
    balance_info = None
    error_message = None

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        pin = request.POST.get('pin')

        try:
            # Retrieve account details
            account = Account.objects.get(account_number=account_number)

            # Validate PIN
            decrypted_pin = ''.join(str(ord(char) - 97) for char in account.pin)
            if decrypted_pin == pin:
                balance_info = {
                    'account_number': account.account_number,
                    'name': account.name,
                    'balance': account.balance,
                }
            else:
                error_message = "Invalid PIN. Please try again."
        except Account.DoesNotExist:
            error_message = "Account not found. Please check your account number."

    return render(request, 'balance.html', {'balance_info': balance_info, 'error_message': error_message})

def pin(request):
    account_number = None
    message = None

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        otp = request.POST.get('otp')
        new_pin = request.POST.get('new_pin')

        if 'generate_otp' in request.POST:
            # Generate and send OTP
            try:
                account = Account.objects.get(account_number=account_number)
                generated_otp = random.randint(100000, 999999)
                account.otp = generated_otp
                account.save()

                # Send OTP to email
                send_mail(
                    subject="OTP for PIN Generation",
                    message=f"Dear {account.name},\n\nYour OTP for PIN generation is {generated_otp}.\n\nSafe Banking,\nHDFC Bank",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[account.email],
                    fail_silently=False,
                )
                message = "OTP has been sent to your registered email."
            except Account.DoesNotExist:
                message = "Account number not found."

        elif 'set_pin' in request.POST:
            # Validate OTP and update PIN
            try:
                account = Account.objects.get(account_number=account_number, otp=int(otp))
                encrypted_pin = ''.join(chr(97 + int(digit)) for digit in new_pin)
                account.pin = encrypted_pin
                account.otp = None  # Clear OTP after use
                account.save()

                # Send confirmation email
                send_mail(
                    subject="PIN Set Successfully",
                    message=f"Dear {account.name},\n\nYour PIN has been successfully set for your account ending in {account_number[-4:]}.\n\nPlease ensure you keep your PIN secure and confidential.\n\nSafe Banking,\nHDFC Bank",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[account.email],
                    fail_silently=False,
                )
                message = "PIN has been successfully set, and a confirmation email has been sent."
            except Account.DoesNotExist:
                message = "Invalid account number or OTP."

    return render(request, 'pin.html', {'account_number': account_number, 'message': message})

def display(request):
    account = None
    error_message = None

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        pin = request.POST.get('pin')

        try:
            # Convert PIN back from encrypted format
            encrypted_pin = ''.join(chr(97 + int(digit)) for digit in pin)
            account = Account.objects.get(account_number=account_number, pin=encrypted_pin)
            account.aadhar = "**** **** **** " + str(account.aadhar)[-4:]
        except Account.DoesNotExist:
            error_message = "Account not found or incorrect PIN. Please try again."

    return render(request, 'display.html', {'account': account, 'error_message': error_message})
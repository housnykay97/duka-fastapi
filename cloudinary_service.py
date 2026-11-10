import cloudinary
import cloudinary.uploader
from send_email import email

cloud_name="fwbepe6n"
api_key="918136337944573"
secret_key="FT6tFWLnEfC3qD5biw8-iqX6-L0"


# Connecting to cloudinary
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=secret_key
)

def upload_pdf(pdf_file):
    try:
        file_path = f"receipts/{pdf_file}.pdf"
        # upload pdf
        upload = cloudinary.uploader.upload(file_path, resource_type = "raw")
        receipt_url = upload["secure_url"]

        print("successful cloudinary upload")
        print(receipt_url)
        # send email
        email("housnykay97@gmail.com","Payment received",f"Thank you we have received your payment.\n\n"f"Receipt: {receipt_url}")
        return "success"
    
    except Exception as e:
        print(f"upload failed: {e}")
        return "failed"



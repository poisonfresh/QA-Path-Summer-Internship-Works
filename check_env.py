"""
Environment variables kontrol scripti
"""
import os

def check_env():
    print("=== Environment Variables Kontrol ===")
    
    email = os.getenv("AMAZON_EMAIL")
    pwd = os.getenv("AMAZON_PASSWORD")
    
    if email:
        print(f"✓ AMAZON_EMAIL: {email[:3]}***{email[-10:] if len(email) > 13 else '***'}")
    else:
        print("✗ AMAZON_EMAIL: Not set")
    
    if pwd:
        print(f"✓ AMAZON_PASSWORD: {'*' * len(pwd)}")
    else:
        print("✗ AMAZON_PASSWORD: Not set")
    
    if email and pwd:
        print("\n✓ Tüm gerekli environment variables ayarlanmış!")
        return True
    else:
        print("\n✗ Bazı environment variables eksik!")
        print("\nLütfen şu komutları çalıştırın:")
        print("Windows PowerShell:")
        print("  $env:AMAZON_EMAIL='your-email@example.com'")
        print("  $env:AMAZON_PASSWORD='your-password'")
        print("\nVeya .env dosyası oluşturun:")
        print("  AMAZON_EMAIL=your-email@example.com")
        print("  AMAZON_PASSWORD=your-password")
        return False

if __name__ == "__main__":
    check_env() 
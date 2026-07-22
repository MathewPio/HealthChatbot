from app.core.security import hash_password, verify_password


plain_password = "HealthChatbot123"

hashed_password = hash_password(plain_password)

print("Generated hash:", hashed_password)
print(
    "Correct password:",
    verify_password(plain_password, hashed_password),
)
print(
    "Incorrect password:",
    verify_password("WrongPassword", hashed_password),
)
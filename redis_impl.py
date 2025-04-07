import random



import redis

# Connect to Redis Server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def send_otp(mobile):
    otp = generate_otp()
    redis_client.setex(f"otp:{mobile}", 100, otp)  # Store OTP with 5 min expiry
    return {"message": "OTP sent", "otp": otp}  # In real apps, send via SMS

print(send_otp("7736624565"))

def verify_otp(mobile, entered_otp):
    stored_otp = redis_client.get(f"otp:{mobile}")

    if not stored_otp:
        return {"message": "OTP expired or invalid"}, 400

    if stored_otp != entered_otp:
        return {"message": "Incorrect OTP"}, 400

    redis_client.delete(f"otp:{mobile}")  # Delete OTP after verification
    return {"message": "OTP verified successfully"}, 200

print(verify_otp("7736624565", "426599"))
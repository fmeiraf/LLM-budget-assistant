import bcrypt


def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def check_password(user_password, hashed_password):
    return bcrypt.checkpw(
        user_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


if __name__ == "__main__":
    password = "mysecretpassword"
    hashed_password = hash_password(password)

    print(len(hashed_password))
